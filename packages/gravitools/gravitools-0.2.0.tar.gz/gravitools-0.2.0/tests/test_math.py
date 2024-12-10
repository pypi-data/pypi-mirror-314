import numpy as np

from gravitools.math import weighted_mean


def test_weighted_mean():
    mu, std, sem = weighted_mean(np.array([1, 2, 3]), np.array([1, 1, 1]))
    assert (mu, round(std, 6), round(sem, 6)) == (2.0, 0.816497, 0.471405)

    mu, std, sem = weighted_mean(np.array([1]), np.array([1]))
    assert (mu, round(std, 6), round(sem, 6)) == (1, 1, 1)

    mu, std, sem = weighted_mean(np.array([1, 2, 3]), np.array([3, 2, 1]))
    assert (round(mu, 6), round(std, 6), round(sem, 6)) == (2.653061, 0.62437, 0.475578)

    mu, std, sem = weighted_mean(np.array([1, float("nan"), 3]), np.array([3, 2, 1]))
    assert (round(mu, 6), round(std, 6), round(sem, 6)) == (2.8, 0.6, 0.543323)
