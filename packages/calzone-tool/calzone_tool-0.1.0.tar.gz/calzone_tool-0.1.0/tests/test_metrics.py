"""
This module contains test functions for calibration metrics.

The main test function generates synthetic data and tests the CalibrationMetrics class.
"""

import numpy as np
from calzone.metrics import CalibrationMetrics

def run_test_metrics():
    """
    Test function for calibration metrics.
    
    Generates synthetic binary classification data and tests the CalibrationMetrics class.
    The test includes:
    - Generating random binary labels using binomial distribution
    - Creating probability predictions using beta distribution
    - Testing the CalibrationMetrics class with the generated data
    Notice that the test is not exhaustive and doesn't test for correctness of the metrics.
    Returns:
        None
    
    Raises:
        AssertionError: If the results from CalibrationMetrics are not in dictionary format
    """
    # Generate sample data
    np.random.seed(123)
    n_samples = 1000
    y_true = np.random.binomial(1, 0.3, n_samples)
    y_proba = np.zeros((n_samples,2))
    y_proba[:, 1] = np.random.beta(0.5, 0.5, (n_samples, ))
    y_proba[:, 0] = 1 - y_proba[:, 1]  # Ensure probabilities sum to 1

    # Test CalibrationMetrics class
    metrics = CalibrationMetrics(class_to_calculate=1)
    results = metrics.calculate_metrics(y_true, y_proba, metrics='all')
    assert isinstance(results, dict)