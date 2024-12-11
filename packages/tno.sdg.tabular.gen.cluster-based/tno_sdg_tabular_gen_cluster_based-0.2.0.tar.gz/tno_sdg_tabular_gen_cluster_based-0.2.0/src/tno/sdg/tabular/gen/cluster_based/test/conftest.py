"""
Fixtures for tests.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tno.sdg.tabular.gen.cluster_based import (
    CategoricalHistogram,
    ContinuousHistogram,
    DataType,
    Histogram,
)


@pytest.fixture
def data() -> pd.DataFrame:
    """
    Fixture with categorical and continuous data.

    :return: Dataframe with categorical and continuous data.
    """
    return pd.DataFrame(
        {
            "feature1": ["a", "b", "c", "a", "b", "e", "a"],
            "feature2": [1, 2, 2, 1, 3, 4, 1],
            "feature3": [3.0, 3.5, 4.0, 4.5, 6.25, 5.1, 7.0],
        },
    )


@pytest.fixture
def data_types() -> list[DataType]:
    """
    Fixture with data types for the data fixture.

    :return: List with data types.
    """
    return [DataType.CATEGORICAL, DataType.CONTINUOUS, DataType.CONTINUOUS]


@pytest.fixture
def histograms(
    data: pd.DataFrame,  # pylint: disable=redefined-outer-name
) -> dict[str, Histogram]:
    """
    Fixture with histograms to describe a cluster.

    :param data: Dataframe with categorical and continuous data.
    :return: Dictionary with histograms, mapping feature names to histograms.
    """
    return {
        "feature1": CategoricalHistogram.from_data(np.array(data["feature1"])),
        "feature2": ContinuousHistogram.from_data(np.array(data["feature2"])),
        "feature3": ContinuousHistogram.from_data(np.array(data["feature3"])),
    }
