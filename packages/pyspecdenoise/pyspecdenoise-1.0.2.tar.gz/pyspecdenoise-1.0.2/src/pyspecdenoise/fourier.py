"""
A python module to perform Fourier denoising of spectra.
"""

import numpy as np
import pandas as pd
from numpy.fft import fft, ifft
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


def power_law(x, a, b):
    """Power law fit."""
    return a * (x**b)


def create_stddev_arr(flux, smooth_flux, wave, width):
    """
    - Produces the "residual" array: difference between the input spectrum and the smoothed spectrum.
    - Computes the standard deviation of the residual array within a symmetric window at each pixel.
    - Returns this standard deviation array.

    :param flux: Spectrum flux array.
    :type flux: numpy.ndarray
    :param smooth_flux: Smoothed spectrum flux array.
    :type smooth_flux: numpy.ndarray
    :param wave: Spectrum wavelength array.
    :type wave: numpy.ndarray
    :param width: Width of the moving window. Measured in Angstroms.
    :type width: float
    :return: Standard deviations of the bins centered on each wavelength in the input spectrum.
    :rtype: numpy.ndarray
    """
    f_resid = flux - smooth_flux  # compute residual array.
    f = pd.Series(f_resid)
    bin_size = int(
        width / (wave[1] - wave[0]) + 1
    )  # compute (integer) number of samples per width.
    g = (
        f.rolling(bin_size).std().to_numpy()
    )  # Take rolling average standard deviation.
    return g


def fourier_smoothing(wlen, flux, k_high: int = 300, k_low: int = 3):
    # pylint: disable=R0914
    """

    **Procedure:**\n
    - Rebin the spectrum on a log-wavelength axis.
    - Resample spectrum into equal-width bins. Uses the smallest dispersion as the bin width.
    - Take the FFT of the flux.
    - Define the range of wavenumbers/velocities for spectral features (see note); the FT indices are determined using k_low and k_high.
    - Fit the magnitude (M) spectrum with a power law between k_low and k_high.
    - Compute MEAN(M).
    - k_noise is the point of intersection between the power law fit an MEAN(M).
    - Set M = 0 for k>k_noise.
    - Invert FFT.
    - Resample spectrum to the original linear grid.


    **Notes:** \n
    - k is related to the velocity of spectral features in the SN spectrum by k = c/v.
    - k can be chosen to exclude high and low velocity features that are likely not due to the SN.
    - The default values of k are k=300 (3000 km/s) and k=3 (100000 km/s) (Liu et al. 2016).

    :param wlen: Wavelength array of the spectrum.
    :type wlen: numpy.ndarray
    :param flux: Array of spectral flux.
    :type flux: numpy.ndarray
    :param k_high: Upper k value for smoothing.
    :type k_high: int
    :param k_low: Lower k value for smoothing.
    :type k_low: int
    """

    # Convert to log wavelength space
    # 1 - Convert the wavelength array to an evenly spaced array in log wavelength space.
    log_wlen = np.log(wlen)
    bin_width = min(np.diff(log_wlen))  # Smallest 'dispersion' in the spectrum
    rs_log_wlen = np.arange(log_wlen[0], log_wlen[-1], bin_width)

    # 2 - Resample the flux on the new wavelength scale
    rs_flux = interp1d(log_wlen, flux)(rs_log_wlen)

    # Compute the Fourier transform
    # 1 - Perform an FFT on the resampled flux
    flux_fft = fft(rs_flux)
    flux_fft_abs = np.abs(flux_fft)
    num_samples = len(flux_fft_abs)
    f_samp = 1 / bin_width
    k = np.fft.fftfreq(len(rs_flux), 1 / f_samp)

    max_index = 0
    if num_samples % 2 == 0:
        max_index = num_samples // 2
    else:
        max_index = num_samples // 2 + 1

    # Find out the indices where k_low<k<k_high
    k_high_index = max(np.where(k[:max_index] < k_high)[0])
    k_low_index = min(np.where(k[:max_index] > k_low)[0])

    # Compute the mean magnitude for k_low<k<k_high
    mean_mag = np.mean(flux_fft_abs[k_low_index : k_high_index + 1])

    # Power law fit to the array where k>3
    popt, *_ = curve_fit(
        power_law,
        k[k_low_index:max_index],
        flux_fft_abs[k_low_index:max_index],
    )

    # Determine k_noise
    k_noise_idx = np.where(power_law(k[1:max_index], *popt) < mean_mag)[0][0]

    # Print some useful info
    print("---------------------------------------------------------")
    print(f"The mean FFT magnitude is: {mean_mag}")
    print(f"k_noise is: {k[k_noise_idx]}")
    print("---------------------------------------------------------")

    # Set the noise FFT coefficients to 0
    flux_fft[k_noise_idx:-k_noise_idx] = 0

    # # Compute the iFFT
    new_signal = np.real(ifft(flux_fft))

    # Rebin on the original wavelength scale
    new_flux = interp1d(rs_log_wlen, new_signal, fill_value="extrapolate")(
        log_wlen
    )

    return wlen, new_flux
