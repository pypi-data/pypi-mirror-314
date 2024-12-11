"""
Unit tests for the ContinuousHistogram class.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd
import pytest

from tno.sdg.tabular.gen.cluster_based import ContinuousHistogram

ADULT_PATH = pathlib.Path(__file__).parent / "data" / "adult.data"


@pytest.mark.parametrize("length", [0, 1])
def test_histogram_init_lims_too_small_fail(length: int) -> None:
    """
    Test that the lims array must have at least two elements.

    :param length: The length of the lims array.
    """
    with pytest.raises(ValueError):
        ContinuousHistogram(np.zeros(length, dtype=np.float64))


@pytest.mark.parametrize(
    "lims", [[0.0, 0.0], [1.0, 1.0], [1, 1], [1, 2, 2], [1, 1, 2], [1, 2, 2, 3]]
)
def test_histogram_init_lims_width_zero_fail(lims: list[int | float]) -> None:
    """
    Test that bins must have a width greater than zero.

    :param lims: Different lims arrays with bins of width zero.
    """
    with pytest.raises(ValueError):
        ContinuousHistogram(np.array(lims))


def test_histogram_init_lims_decreasing_fail() -> None:
    """
    Test that the bin limits must be strictly increasing.
    """
    with pytest.raises(ValueError):
        ContinuousHistogram(np.array([2, 1]))


def test_histogram_init_densities_dimension_fail() -> None:
    """
    Test that the densities array must have the same dimension as the lims
    array.
    """
    with pytest.raises(ValueError):
        ContinuousHistogram(np.array([1, 2]), np.zeros(2, dtype=np.int_))


@pytest.mark.parametrize("n_samples", [1, 10, 100])
def test_histogram_sample(n_samples: int) -> None:
    """
    Test that sampling produces the correct number of samples.

    :param n_samples: The number of samples to draw.
    """
    df_adult = pd.read_csv(ADULT_PATH)
    hist = ContinuousHistogram.from_data(df_adult["age"].to_numpy())
    samples = hist.sample(n_samples)
    assert len(samples) == n_samples


@pytest.mark.parametrize("n_samples", [-1, 0, 0.5])
def test_histogram_sample_invalid(n_samples: int) -> None:
    """
    Test that sampling with an invalid number of samples raises an error.

    :param n_samples: The number of samples to draw.
    """
    df_adult = pd.read_csv(ADULT_PATH)
    hist = ContinuousHistogram.from_data(df_adult["age"].to_numpy())
    with pytest.raises((ValueError, TypeError)):
        hist.sample(n_samples)
