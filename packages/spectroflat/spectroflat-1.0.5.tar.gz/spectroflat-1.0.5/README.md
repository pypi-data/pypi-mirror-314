# spectroflat
Python based library to flat field spectro-polarimetric data.

When using this library to reduce your data, please cite:

Hoelken et al. "Spectroflat: A generic spectrum and flat-field calibration library for spectro-polarimetric data" 
([DOI: 10.1051/0004-6361/202348877](https://doi.org/10.1051/0004-6361/202348877))

## Theoretical Background 
Generally this is intended to be an extension of the
"[Precise reduction of solar spectra obtained with large CCD arrays](https://www.aanda.org/articles/aa/pdf/2002/42/aa2154.pdf)"
method by Wöhl et al. (2002) to spectro-polarimetric instruments covering a large spectral field of view with many lines.

The spectroflat algorithm is described and evaluated in 
Hölken et al. (2023) "Spectroflat: A generic calibration library for spectro-polarimetric data". [in preparation] 

## Input data 
The input data must be calibrated for the camera zero-input response (dark current and bias level) and 
relevant non-linearity effects. If each modulation state is to be corrected with its own set of calibration data 
an average of all frames from the flat field recording belonging to each modulation state has to be provided. 

Input data shall be provided as a `numpy` Array with dimensions modulation state, spatial location 
along the spectrograph slit and wavelength position. 

## Extracted Data

### Dust-Flat
The dust-flat is a combination of the sensor and slit flat that 
contains most of the "hard" flat field features.
Most prominently the following is corrected:
- Sensor features (e.g. column-to-column response patterns, dust on the sensor itself)
- Slit features (e.g. dust on the slit resulting in line features in the spectral direction)
- Fixed optical fringes and illumination impurities.

The dust flat might be split in Sensor Flat and Slit Flat by the mean profile method applied along 
the spectrograph slit dimension. 

### Smile offset map
spectroflat characterizes the smile distortion by tracking the change of every spectral absorption or emission 
line with respect to the reference profile generated from the central rows. The map list the offset each pixel 
has, compared to that reference, with sub-pixel precision.  

### Illumination pattern
Typically, the illumination patterns are in the 10−6 range and are not used.  
This result is kept for compatibility with the approach of Wöhl et al. (2002).

### PDF Report
A report summary with relevant plots to inspect the quality of the extracted products. 

## Technical Documentation

**NOTE** This library expects the spacial domain on the vertical-axis and
the spectral domain on the horizontal axis. 
spectroflat does not include any file reading/writing routines and expects `numpy` arrays as input. 

Please refer to the  [API Documentation](https://hoelken.pages.gwdg.de/spectroflat/doc/spectroflat/) for 
implementation details. 
Especially the entries on available 
[Configuration](https://hoelken.pages.gwdg.de/spectroflat/doc/spectroflat/base/config.html) values 
are of general interest. 

The [`example.py`](example.py) script provides an usage example. 

## Contact
This code is developed and maintained at the Max Planck Institute for 
Solar System Research (MPS) Göttingen.

### Maintainer 
- Johannes Hoelken ([hoelken@mps.mpg.de](mailto:hoelken@mps.mpg.de))

### Contributions
- Alex Feller 
- Francisco Iglesias

## License
BSD clause-2, see [LICENSE](LICENSE)