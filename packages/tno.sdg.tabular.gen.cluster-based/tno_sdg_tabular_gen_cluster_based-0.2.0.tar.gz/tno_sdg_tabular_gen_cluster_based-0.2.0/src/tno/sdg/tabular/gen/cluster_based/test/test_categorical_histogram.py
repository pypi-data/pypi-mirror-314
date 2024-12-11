"""
Unit tests for the CategoricalHistogram class.
"""

import pathlib

import numpy as np
import pandas as pd
import pytest

from tno.sdg.tabular.gen.cluster_based import CategoricalHistogram

adult_path = pathlib.Path(__file__).parent / "data" / "adult.data"


def test_histogram_init_values_empty() -> None:
    """
    Test that the values array must have at least one element.
    """
    with pytest.raises(ValueError):
        CategoricalHistogram(
            np.zeros(0, dtype=np.float64), np.zeros(0, dtype=np.float64)
        )


def test_histogram_init_values_not_unique() -> None:
    """
    Test that the values array must have unique elements.
    """
    with pytest.raises(ValueError):
        CategoricalHistogram(np.array(["a", "a", "b"]), np.array([0.3, 0.4, 0.3]))


def test_histogram_init_densities_dimension_fail() -> None:
    """
    Test that the densities array must have the same dimension as the values
    array.
    """
    with pytest.raises(ValueError):
        CategoricalHistogram(np.array(["a", "b"]), np.zeros(3, dtype=np.int_))


@pytest.mark.parametrize("n_samples", [1, 10, 100])
def test_histogram_sample(n_samples: int) -> None:
    """
    Test that sampling produces the correct number of samples.

    :param n_samples: The number of samples to draw.
    """
    df_adult = pd.read_csv(adult_path)
    hist = CategoricalHistogram.from_data(df_adult["education"])
    samples = hist.sample(n_samples)
    assert len(samples) == n_samples


@pytest.mark.parametrize("n_samples", [-1, 0, 0.5])
def test_histogram_sample_invalid(n_samples: int) -> None:
    """
    Test that sampling with an invalid number of samples raises an error.

    :param n_samples: The number of samples to draw.
    """
    df_adult = pd.read_csv(adult_path)
    hist = CategoricalHistogram.from_data(df_adult["education"])
    with pytest.raises((ValueError, TypeError)):
        hist.sample(n_samples)
