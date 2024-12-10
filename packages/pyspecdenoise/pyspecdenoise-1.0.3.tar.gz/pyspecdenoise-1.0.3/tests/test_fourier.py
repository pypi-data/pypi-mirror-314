import numpy as np
import pytest
from numpy.testing import assert_allclose

from pyspecdenoise.fourier import fourier_smoothing

TEST_FILE = (
    "tests/SN2004gq_2004-12-12_07-12-00_FLWO-1.5m_FAST_CfA-Stripped.flm"
)
CHECK_FILE = "tests/smoothed.txt"


@pytest.fixture
def load_input_spec():
    wave, flux = np.loadtxt(TEST_FILE, usecols=range(2), unpack=True)

    return wave, flux


@pytest.fixture
def load_comparison_spec():
    wave, flux, flux_smooth = np.loadtxt(CHECK_FILE, unpack=True)
    return wave, flux, flux_smooth


def test_fourier_smoothing(load_input_spec, load_comparison_spec):
    input_wavelength, input_flux = load_input_spec

    wlen, new_flux = fourier_smoothing(
        input_wavelength / (1 + 0.0065), input_flux / np.mean(input_flux)
    )  # Divide by the mean so that all spectra are "normalised".

    wave, flux, flux_smooth = load_comparison_spec

    assert_allclose(wlen, wave)
    assert_allclose(input_flux, flux)
    assert_allclose(new_flux, flux_smooth)
