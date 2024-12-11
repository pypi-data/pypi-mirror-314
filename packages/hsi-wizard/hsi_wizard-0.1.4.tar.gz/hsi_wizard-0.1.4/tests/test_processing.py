import pytest
import numpy as np
from scipy.signal import savgol_filter, butter, filtfilt

# Importing the functions to be tested
from wizard._processing.spectral import (
    smooth_savgol,
    smooth_moving_average,
    smooth_butter_lowpass,
    spec_baseline_als,
    calculate_modified_z_score,
    get_ratio_two_specs,
    get_sub_tow_specs,
    signal_to_noise,
    del_leading_zeros,
    del_last_zeros
)

# Create sample data for testing
@pytest.fixture
def sample_spectrum():
    return np.array(range(100))

@pytest.fixture
def sample_baseline_spectrum():
    return np.array(range(100))

@pytest.fixture
def sample_wavelengths():
    return np.linspace(400, 800, 10)



def test_smooth_savgol(sample_spectrum):
    smoothed = smooth_savgol(sample_spectrum, window_length=5, polyorder=2)
    assert len(smoothed) == len(sample_spectrum)


def test_smooth_moving_average(sample_spectrum):
    smoothed = smooth_moving_average(sample_spectrum, window_size=3)
    assert len(smoothed) == len(sample_spectrum) - 2, "Length of moving average should be adjusted based on window size."


def test_smooth_butter_lowpass(sample_spectrum):
    filtered = smooth_butter_lowpass(sample_spectrum, cutoff=0.1, fs=1, order=3)
    assert len(filtered) == len(sample_spectrum), "Length of filtered spectrum should match input length."


def test_calculate_modified_z_score(sample_spectrum):
    modified_z = calculate_modified_z_score(sample_spectrum)
    assert modified_z.shape[0] == sample_spectrum.shape[0] - 1
    assert modified_z.shape[1:] == sample_spectrum.shape[1:]


def test_get_ratio_two_specs(sample_spectrum, sample_wavelengths):
    # Generate test data with random values and fixed wavelengths
    ratio = get_ratio_two_specs(sample_spectrum, sample_wavelengths, wave_1=450, wave_2=650)
    assert ratio != -1, "Ratio should be valid for given wavelengths within the range."
    assert ratio >= 0, "Ratio should be non-negative."


def test_get_sub_tow_specs(sample_spectrum, sample_wavelengths):
    # Generate test data with random values and fixed wavelengths
    diff = get_sub_tow_specs(sample_spectrum, sample_wavelengths, wave_1=450, wave_2=650)
    assert diff != -1, "Difference should be valid for given wavelengths within the range."


def test_signal_to_noise(sample_spectrum):
    snr = signal_to_noise(sample_spectrum)
    assert snr >= 0, "Signal-to-noise ratio should be non-negative."


def test_del_leading_zeros():
    spectrum = np.array([0, 0, 0, 5, 6, 7])
    result = del_leading_zeros(spectrum, auto_offset=0)
    assert result[0] == 5, "Leading zeros should be removed."


def test_del_last_zeros():
    spectrum = np.array([5, 6, 7, 0, 0, 0])
    result = del_last_zeros(spectrum, auto_offset=0)
    print(result)
    assert result[-1] == 7, "Trailing zeros should be removed."


# Additional test case for edge cases and boundary conditions
def test_smooth_savgol_invalid_input():
    with pytest.raises(ValueError):
        smooth_savgol(np.array([1, 2, 3]), window_length=4, polyorder=2)  # Window length must be odd


def test_signal_to_noise_zero_std():
    spectrum = np.array([1, 1, 1, 1])
    snr = signal_to_noise(spectrum)
    assert snr == 0, "SNR should be zero when the standard deviation is zero."
