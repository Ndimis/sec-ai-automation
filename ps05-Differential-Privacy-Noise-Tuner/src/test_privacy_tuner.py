import pytest
import numpy as np
from privacy_tuner import PrivacyTuner

def test_epsilon_inverse_relationship():
    """Ensure that smaller epsilon results in larger noise (higher error)."""
    tuner = PrivacyTuner()
    data = np.random.rand(1000)
    
    error_high_privacy = tuner.calculate_accuracy_loss(data, epsilon=0.1)
    error_low_privacy = tuner.calculate_accuracy_loss(data, epsilon=10.0)
    
    assert error_high_privacy > error_low_privacy

def test_noise_distribution():
    """Verify that generated noise follows a Laplace-like distribution (centered at 0)."""
    tuner = PrivacyTuner()
    noise = tuner.generate_noise(epsilon=1.0, size=5000)
    
    assert -0.5 < np.mean(noise) < 0.5

def test_sensitivity_impact():
    """Ensure higher sensitivity data requires more noise for the same epsilon."""
    tuner_low = PrivacyTuner(sensitivity=1.0)
    tuner_high = PrivacyTuner(sensitivity=10.0)
    
    noise_low = np.std(tuner_low.generate_noise(epsilon=1.0))
    noise_high = np.std(tuner_high.generate_noise(epsilon=1.0))
    
    assert noise_high > noise_low