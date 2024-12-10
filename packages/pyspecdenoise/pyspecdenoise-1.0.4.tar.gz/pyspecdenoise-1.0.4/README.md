# pyspecdenoise documentation

![GitHub Release](https://img.shields.io/github/v/release/GabrielF98/pyspecdenoise?color=teal)

Python library for removing noise from supernova spectra using a Fourier method. Implemented by Gabriel Finneran at University College Dublin, Ireland.

Here is an example showing the input and result for a spectrum of SN2004gq (spectrum taken from [WISeREP](https://www.wiserep.org/object/8340)).

<img width="600" alt="Noise removal result" src="https://github.com/user-attachments/assets/322e6994-17e9-47e0-9ebe-910b3a4935d9">

A full description of the tool is given here. Further information may be found in [Finneran et al. (2024)](https://arxiv.org/abs/2411.12574) (see below for details on how to cite this work!).

This algorithm is based on the procedure presented in [Liu et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...827...90L/abstract) (see their Appendix B). This is the first publicly available implementation of this algorithm written in Python.  

An [IDL version of this code](https://github.com/metal-sn/SESNspectraLib/blob/master/SNspecFFTsmooth.pro) is available from the original developers.

This package can be installed from [PyPI](https://pypi.org/project/pyspecdenoise/) using pip:

```
pip install pyspecdenoise
```

Full documentation is available [here](https://pyspecdenoise.readthedocs.io/en/stable/).
 
Issues can be logged [here](https://github.com/GabrielF98/fouriersmooth/issues).

You can also contact me via [email](mailto:gabfin15@gmail.com).

## Basic description

1. Rebin the spectrum on a log-wavelength axis.
2. Resample spectrum into equal-width bins. Uses the smallest dispersion as the bin width.
3. Take the FFT of the flux.
4. Define the range of wavenumbers/velocities for spectral features (see notes); the FFT indices are determined using `k_low` and `k_high`.
5. Fit the magnitude (M) spectrum with a power law between `k_low` and `k_high`.
6. Compute `MEAN(M)`.
7. `k_noise` is the point of intersection between the power law fit and `MEAN(M)`.
8. Set `M = 0` for `k > k_noise`.
9. Invert FFT.
10. Resample spectrum to the original linear grid.

Here is an example image showing the procedure used to determine `k_noise` (using the same spectrum of SN2004gq from WISeREP):

<img width="600" alt="Noise removal procedure" src="https://github.com/user-attachments/assets/0cbf69fe-86be-480c-9187-0e2f1c2bbe63">

**Notes:**

- `k` is related to the velocity of spectral features in the SN spectrum by `k = c/v`.
- `k` can be chosen to exclude high and low velocity features that are likely not due to the SN.
- The default values of `k` are `k=300` (3000 km/s) and `k=3` (100000 km/s) (Liu et al. 2016).

## How to cite this code in your work

If you use `pyspecdenoise` in your work, please consider citing [Finneran et al. (2024)](https://arxiv.org/abs/2411.12574) (see below for bibtex).  

I would also appreciate it if you could add an acknowledgment such as:

```
To remove noise from supernova spectra, this work has made use of \texttt{pyspecdenoise},
implemented by Gabriel Finneran and available at: \url{https://github.com/GabrielF98/fouriersmooth}.
```

```
@ARTICLE{2024arXiv241112574F,
      author = {{Finneran}, Gabriel and {Martin-Carrillo}, Antonio},
      title = "{Measuring the expansion velocities of broad-line Ic supernovae: An investigation of neglected sources of error in two popular methods}",
      journal = {arXiv e-prints},
      keywords = {Astrophysics - High Energy Astrophysical Phenomena},
      year = 2024,
      month = nov,
      eid = {arXiv:2411.12574},
      pages = {arXiv:2411.12574},
      doi = {10.48550/arXiv.2411.12574},
      archivePrefix = {arXiv},
      eprint = {2411.12574},
      primaryClass = {astro-ph.HE},
      adsurl = {https://ui.adsabs.harvard.edu/abs/2024arXiv241112574F},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
