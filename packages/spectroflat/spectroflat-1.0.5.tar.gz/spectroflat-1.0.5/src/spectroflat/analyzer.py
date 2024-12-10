from __future__ import annotations

import os
from datetime import datetime

from .base import Logging
from .base.config import Config
from .inspection.flat_field_report import *
from .inspection.offset_map import plt_map
from .sensor.artificial_flat import ArtificialFlat
from .sensor.c2c_comp import extract_c2c_comp
from .sensor.flat import Flat
from .shift.img_rotation import RotationCorrection, RotationAnalysis
from .smile import OffsetMap, SmileInterpolator, SmileMapGenerator, StateAligner
from .smile.smoothing import *
from .utils.line_detection import find_line_cores
from .utils.processing import MP

log = Logging.get_logger()


class Analyser:
    """
    The Analyzer is the smile detection library entry point.
    This class will generate the offset map and gain table that can be used to correct science frames.

    If a report dir is given, a PDF report with detailed information on the generated offset map and gain
    table is created.
    """

    def __init__(self, cube: np.array, config: Config, report_dir: str = None):
        self._report = None
        self._out_dir = report_dir
        self._config = config
        self._orig = cube
        self._input = cube.copy()
        self._rotation = 0
        #: The smile-corrected data cube
        self.desmiled = cube
        #: The created pre flat (Sensor Flat)
        self.pre_flat = np.empty(cube.shape)
        #: The column 2 column pattern
        self.c2c_pattern = None
        #: The created gain table
        self.gain_table = np.empty(cube.shape)
        #: The detected offset map of the smile
        self.offset_map = OffsetMap()

    def run(self) -> Analyser:
        """Perform the smile analysis on the given dataset"""
        try:
            self._start()
            self._plt_input()
            self._remove_c2c_comp()
            self._apply_sensor_flat()
            self._analyse()
            self._create_gain_table()
            self._plt_applied_flat()
            return self
        finally:
            self._cleanup()

    def _apply_sensor_flat(self):
        if not self._config.apply_sensor_flat:
            log.info('Sensor flat skipped....')
            return

        log.info('Generating and applying pre-flat.')
        flats = self._gen_pre_flat()
        self._apply_pre_flat(flats)
        self._report_pre_flat()

    def _remove_c2c_comp(self):
        if not self._config.sensor_flat.average_column_response_map:
            return

        log.info('Removing column-2-column response pattern...')
        roi = self._config.roi
        if roi is None:
            self.c2c_pattern = extract_c2c_comp(self._orig, (self._orig.shape[1], self._orig.shape[2]))
        else:
            img = np.array([self._orig[s][roi] for s in range(self._orig.shape[0])])
            self.c2c_pattern = extract_c2c_comp(img, (self._orig.shape[1], self._orig.shape[2]))
        self._orig = self._orig * self.c2c_pattern

    def _gen_pre_flat(self) -> list:
        states = self._orig.shape[0]
        return [Flat.from_frame(self._orig[i], self._config.sensor_flat) for i in range(states)]

    def _apply_pre_flat(self, flats: list):
        states = self._orig.shape[0]
        self._orig = np.array([flats[i].correct(self._orig[i]) for i in range(states)])
        self.desmiled = self._orig
        self.pre_flat = np.array([f.flat for f in flats])

    def _report_pre_flat(self):
        if not self._report:
            return

        m, s = self.pre_flat.mean(), 3 * self.pre_flat.std()
        plt_state_imgs(self.pre_flat, title='Pre Flats (3-sigma)', pdf=self._report, clim=[m - s, m + s])

    def _analyse(self):
        self._derotate()
        self._plt_lines()
        self._compute_offsets()
        self._desmile()
        self._align()
        self._plt_image_results()

    def _derotate(self):
        if self._config.smile.rotation_correction is None:
            self._config.smile.rotation_correction = self._rotation
            return

        if self._config.smile.rotation_correction in ['h', 'horizontal', 'horizontally']:
            log.info('Detecting rotation according to horizontal lines')
            rot = [RotationAnalysis.detect_horizontal_rotation(self._input[s]) for s in range(self._input.shape[0])]
            self._rotation = np.mean(rot)
        elif self._config.smile.rotation_correction in ['v', 'vertical', 'vertically']:
            log.info('Detecting rotation according to vertical lines')
            rot = [RotationAnalysis.detect_vertical_rotation(self._input[s]) for s in range(self._input.shape[0])]
            self._rotation = np.mean(rot)
        else:
            self._rotation = float(self._config.smile.rotation_correction)

        log.info('Using rotation correction with %.4f [deg]', self._rotation)
        img = [RotationCorrection(self.desmiled[s], self._rotation).bicubic() for s in range(self._input.shape[0])]
        self._config.smile.rotation_correction = self._rotation
        self.desmiled = np.array(img)

    def _plt_lines(self):
        if self._report is None:
            return

        if self._config.roi is None:
            center = self._orig.shape[1] // 2
            row = np.average(self._orig[0, center - 3: center + 3], axis=0)
        else:
            roi = self._orig[0][self._config.roi]
            center = roi.shape[0] // 2
            row = np.average(roi[center - 3: center + 3], axis=0)

        _, lines = find_line_cores(row, self._config.smile)
        lines = [v for v in lines if v is not None]
        plt_selected_lines(row, lines, self._report)

    def _compute_offsets(self) -> None:
        smg = SmileMapGenerator(self._config.smile, self.desmiled).run()
        self.offset_map = smg.omap
        if not self._config.smile.state_aware:
            log.info('Enforcing same offset correction on all mod states')
            self.offset_map.enforce_same_offsets_on_all_states()
        self._append_offset_plots_to_report(smg)

    def _append_offset_plots_to_report(self, smg: SmileMapGenerator):
        if not self._report:
            return

        # plt_deviation_from_straight(smg, pdf=self._report)
        if self._config.roi is None:
            offset = 0
            total_rows = smg.omap.map.shape[1]
        else:
            offset = self._config.roi[0].start
            total_rows = self._config.roi[0].stop - self._config.roi[0].start
        rows = [total_rows // 10,
                total_rows // 4,
                total_rows // 2,
                total_rows - total_rows // 4,
                total_rows - total_rows // 10]
        rows = tuple([r + offset for r in rows])
        plt_map(self.offset_map, pdf=self._report, rows=rows, state_aware=self._config.smile.state_aware)

    def _desmile(self):
        log.info('Applying smile correction...')
        args = [(self.offset_map, self._orig[s], s) for s in range(self._orig.shape[0])]
        result = dict(MP.simultaneous(SmileInterpolator.desmile_state, args))
        self.desmiled = np.array([result[s] for s in range(self._orig.shape[0])])

    def _align(self):
        if not self._config.smile.align_states:
            return

        log.info('Aligning mod states...')
        self._align_state_offsets()
        self._desmile()

    def _align_state_offsets(self):
        sta = StateAligner(self.desmiled, self.offset_map, self._config.smile).run()
        self.offset_map = sta.omap

        if not self._report:
            return

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=A4_LANDSCAPE)
        fig.suptitle('Differential line positions compared to state 0')
        for i in range(1, len(sta.deltas)):
            ax.plot(sta.deltas[i]['x'], sta.deltas[i]['y'], label=f'State {i}')
        ax.set_xlabel('Line pos. [px]')
        ax.set_ylabel('Delta [px]')
        ax.legend()
        fig.tight_layout()
        self._report.savefig()
        plt.close()

    def _start(self):
        if self._out_dir:
            os.makedirs(self._out_dir, exist_ok=True)
            fname = f'offset_analysis_report_{datetime.now().strftime("%y%m%d_%H%M%S")}.pdf'
            self._report = PdfPages(os.path.join(self._out_dir, fname))

    def _create_gain_table(self):
        log.info('Creating gain table...')
        self._artificial_flat()
        self._remove_lines()
        self._interpolate_line_residuals()

    def _refine_hard_flat(self) -> float:
        input_img = self._input * self.c2c_pattern if self.c2c_pattern is not None else self._input
        if self._config.roi is None:
            af = ArtificialFlat(self.desmiled).create().resmile(self.offset_map)
            hard_flat = af.remove(input_img)
            hard_flat = hard_flat / hard_flat.mean()
        else:
            roi = (slice(None, None), self._config.roi[0], self._config.roi[1])
            af = ArtificialFlat(self.desmiled, roi=roi).create().resmile(self.offset_map).pad(self._input.shape)
            hard_flat = af.remove(input_img)
            temp = np.ones(input_img.shape)
            for state in range(temp.shape[0]):
                hf = hard_flat[state][self._config.roi]
                temp[state][self._config.roi] = hf / hf.mean()
            hard_flat = temp
        std = np.std(hard_flat / hard_flat.mean() - self.pre_flat / self.pre_flat.mean())
        log.info('\tSTD of normalized diff of consecutive flats: %e', std)
        # hard_flat[hard_flat <= 0] = 1
        self.pre_flat = hard_flat
        return float(std)

    def _correct_original(self) -> None:
        flat = self.pre_flat / self.c2c_pattern if self.c2c_pattern is not None else self.pre_flat
        flat = Flat(flat)
        current = flat.correct(self._input)
        args = [(self.offset_map, current[s], s) for s in range(current.shape[0])]
        result = dict(MP.simultaneous(SmileInterpolator.desmile_state, args, workers=4))
        self.desmiled = np.array([result[s] for s in range(current.shape[0])])

    def _refine_results(self) -> float:
        # Refines the hard flat and applies the correction to create a new
        # de-smiled image.
        # Returns the standard deviation of the difference of two consecutive hard flats.
        std = self._refine_hard_flat()
        self._correct_original()
        return std

    def _artificial_flat(self):
        log.info('iterating hard flat')
        first_order = self.desmiled
        stds = [self._refine_results() for _ in range(self._config.sensor_flat_iterations)]
        self._apply_c2c_pattern()
        self._plot_refined_results(stds, first_order)

    def _apply_c2c_pattern(self):
        if self.c2c_pattern is None:
            return

        self.pre_flat = self.pre_flat / self.c2c_pattern
        img = Flat(self.pre_flat).correct(self._input)
        if self._config.roi is not None:
            img = np.array([img[s][self._config.roi] for s in range(img.shape[0])])
        c2c_pattern = extract_c2c_comp(img, (self._orig.shape[1], self._orig.shape[2]))
        self.pre_flat = self.pre_flat / c2c_pattern

    def _plot_refined_results(self, stds: list, first_order: np.array):
        if not self._report:
            return

        plt_std_of_consecutive_hard_flats(stds, self._report)
        m = self.pre_flat.mean()
        s = 3 * self.pre_flat.std()
        plt_state_imgs(self.pre_flat, title='New iterated hard flat (3-sigma)', pdf=self._report, clim=[m - s, m + s])
        plt_state_imgs(self.desmiled, title='Desmiled corrected input', pdf=self._report)
        if self._config.roi is None:
            roi = (0, first_order.shape[1] // 2)
        else:
            roi = (0, (self._config.roi[0].stop - self._config.roi[0].start) // 2, self._config.roi[1])
        self._plt_cuts((first_order[roi], "Old"), (self.desmiled[roi], "New"))
        plt_spatial_comparison(self._input, self.desmiled, pdf=self._report, roi=self._config.roi)

    def _plt_cuts(self, a: tuple, b: tuple):
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=A4_LANDSCAPE)
        fig.suptitle('State 0 spectra before and after correction')
        ax[0].plot(a[0], label=a[1])
        ax[0].plot(b[0], label=b[1])
        n = len(a[0]) // 2
        ax[1].plot(range(n - n // 4, n + n // 4), a[0][n - n // 4:n + n // 4])
        ax[1].plot(range(n - n // 4, n + n // 4), b[0][n - n // 4:n + n // 4])
        fig.legend()
        fig.tight_layout()
        self._report.savefig()
        plt.close()

    def _remove_lines(self):
        log.info('Removing vertical lines')
        if self._config.roi is None:
            self._remove_lines_full()
        else:
            self._remove_lines_roi()
        self._plt_line_removal()

    def _remove_lines_roi(self):
        roi = (slice(None, None), self._config.roi[0], self._config.roi[1])
        lr = LineRemover(self.desmiled[roi]).run()
        temp = np.array([lr.result[s] / lr.result[s].mean() for s in range(lr.result.shape[0])])
        self.gain_table = np.ones(self._input.shape)
        for state in range(self._input.shape[0]):
            self.gain_table[roi] = temp

    def _remove_lines_full(self):
        lr = LineRemover(self.desmiled).run()
        self.gain_table = np.array([lr.result[s] / lr.result[s].mean() for s in range(lr.result.shape[0])])

    def _plt_line_removal(self):
        if not self._report:
            return

        m = self.gain_table.mean()
        s = 3 * self.gain_table.std()
        plt_state_imgs(self.gain_table, title='Gain table after removing vertical lines (3-Sigma)',
                       pdf=self._report, clim=[m - s, m + s])

    def _interpolate_line_residuals(self):
        if not self._config.smile.smooth:
            return

        log.info('Smoothing residuals')
        if self._config.roi is None:
            self._interpolate_full()
        else:
            self._interpolate_roi()
        self._plt_smoothing_result()

    def _interpolate_full(self):
        for s in range(self.gain_table.shape[0]):
            self.gain_table[s] = ResidualsRemover(self.gain_table[s]).run().img
            self.gain_table[s] = GaussianBlur(self.gain_table[s]).run().gain

    def _interpolate_roi(self):
        roi = self._config.roi
        for s in range(self.gain_table.shape[0]):
            self.gain_table[s][roi] = ResidualsRemover(self.gain_table[s][roi]).run().img
            self.gain_table[s][roi] = GaussianBlur(self.gain_table[s][roi]).run().gain

    def _cleanup(self):
        if self._report:
            self._report.close()

    def _plt_image_results(self):
        if self._report is None:
            return
        plt_adjustment_comparison(self._orig[0], self.desmiled[0], self._report, roi=self._config.roi)
        inp = np.average(self._input, axis=0)
        plt_img(inp, title='Averaged input image', pdf=self._report, roi=self._config.roi)
        plt_img(np.average(self.desmiled, axis=0), title='Averaged input image after de-smiling',
                pdf=self._report, clim=[inp.min(), inp.max()])

    def _plt_smoothing_result(self):
        if not self._report:
            return

        m = self.gain_table.mean()
        s = 3 * self.gain_table.std()
        plt_state_imgs(self.gain_table, title='Gain table after smoothing (3-Sigma)',
                       pdf=self._report, clim=[m - s, m + s])

    def _plt_applied_flat(self):
        if not self._report:
            return

        corrected = np.true_divide(self.desmiled.astype('float32'), self.gain_table.astype('float32'),
                                   out=self.desmiled.astype('float32'), where=self.gain_table != 0,
                                   dtype='float64')
        plt_state_imgs(corrected, title='Flat fielded input image', pdf=self._report)
        plt_spatial_comparison(self._input, corrected, pdf=self._report, roi=self._config.roi)
        corrected[0] = self.desmiled[0] / np.mean(self.desmiled[0])
        for i in range(1, corrected.shape[0]):
            corrected[i] = (self.desmiled[i] / self.desmiled[i].mean()) - corrected[0]
        corrected[0] = np.zeros(corrected[0].shape)
        m, s = corrected[1:].mean(), 3 * corrected[1:].std()
        plt_state_imgs(corrected,
                       title='Mod state 0 subtracted from the other de-smiled images (Normalized, 3-Sigma)',
                       clim=[m - s, m + s], pdf=self._report)
        self._plt_diff_cuts(corrected)

    def _plt_diff_cuts(self, img: np.array):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=A4_LANDSCAPE)
        for s in range(1, img.shape[0]):
            ax.plot(img[s, img.shape[1] // 2], label=f'<#{s}> - <#0>')
        ax.grid(True)
        fig.suptitle("Spectral cuts of delta images")
        ax.legend()
        ax.set_ylim([-0.015, 0.015])
        ax.set_xlim([0, img.shape[2]])
        ax.set_xlabel(r'$\lambda$ [px]')
        fig.tight_layout()
        self._report.savefig()
        plt.close()

    def _plt_input(self):
        if not self._report:
            return

        plt_state_imgs(self._orig, title='Input data', pdf=self._report)
