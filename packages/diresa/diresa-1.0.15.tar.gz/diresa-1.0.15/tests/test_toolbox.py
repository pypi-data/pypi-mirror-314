#!/usr/bin/env python3
"""
:Author:  Geert De Paepe
:Email:   geert.de.paepe@vub.be
:License: MIT License
"""

from math import isclose
import tensorflow as tf
from diresa.toolbox import covariance, r2_score
import numpy as np


def test_covariance():
    # test data
    data = tf.constant([[2.1, 2.5, 3.6], [3.4, 4.1, 5.2], [4.5, 5.6, 6.7]], dtype=tf.float32)
    # numpy: np.cov(data, bias=True, rowvar=False)
    cov = covariance(data)
    expected_cov = [[0.96222230, 1.24111112, 1.24111112],
                    [1.24111112, 1.60222212, 1.60222212],
                    [1.24111112, 1.60222212, 1.60222212]]
    assert isclose(tf.reduce_sum(cov), sum(map(sum, expected_cov)), abs_tol=1e-5), f"Expected {cov}, but got {expected_cov}"


def test_r2_score():
    # test data
    y_true = tf.constant([[3, -0.5, 2, 7], [2, 0, 0, 1]], dtype=tf.float32)
    y_pred = tf.constant([[2.5, 0.0, 2, 8], [2, 0.5, 0, 1]], dtype=tf.float32)
    # scikit-learn: r2_score(y_true, y_pred, multioutput='variance_weighted')
    r2 = r2_score(y_true, y_pred)
    expected_r2 = 0.9151515
    assert isclose(r2, expected_r2, abs_tol=1e-5), f"Expected {expected_r2}, but got {r2.numpy()}"


if __name__ == "__main__":
    test_r2_score()
