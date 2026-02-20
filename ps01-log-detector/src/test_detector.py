import pytest
import pandas as pd
import os
from .detector import train_advanced_detector

DATA_PATH = 'data/system_logs.csv'

@pytest.fixture
def detection_results():
    """
    Fixture to run the detector once for all tests.
    """
    if not os.path.exists(DATA_PATH):
        pytest.skip("Dataset missing. Run log_generator.py first.")
    
    results, model, features = train_advanced_detector(DATA_PATH)
    return results

def test_anomaly_detection_rate(detection_results):
    """
    Ensure the detector is actually flagging anomalies (approx 2% based on contamination).
    """
    anomalies = detection_results[detection_results['is_detected'] == 1]
    # We expect roughly 40 anomalies out of 2040 logs
    assert 30 <= len(anomalies) <= 60, f"Expected ~40 anomalies, found {len(anomalies)}"

def test_high_risk_correlation(detection_results):
    """
    Behavioral Test: Are 'Admin' logins at 'Night' from 'Unknown Locations' flagged?
    """
    # Filter for the specific 'Attacker' profile we generated
    high_risk_events = detection_results[
        (detection_results['hour'] < 5) & 
        (detection_results['is_admin'] == 1) & 
        (detection_results['location_idx'] > 10)
    ]
    
    # In a robust model, 100% of these extreme outliers should be flagged
    detection_rate = high_risk_events['is_detected'].mean()
    assert detection_rate == 1.0, f"High-risk profile detection failed. Rate: {detection_rate}"

def test_feature_integrity(detection_results):
    """
    Ensure all 6 features are present in the results dataframe.
    """
    expected_cols = ['hour', 'failed_attempts', 'data_transfer_mb', 'location_idx', 'is_admin', 'session_sec']
    for col in expected_cols:
        assert col in detection_results.columns