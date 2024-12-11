"""
Unit tests for the generator module.
"""

from __future__ import annotations

from typing import cast

import numpy as np
import pandas as pd
import pytest
from sklearn.cluster import KMeans

from tno.sdg.tabular.gen.cluster_based import (
    ClusterBasedGenerator,
    ClusterDescription,
    DataType,
    Histogram,
)
from tno.sdg.tabular.gen.cluster_based.histogram import (
    CategoricalHistogram,
    CategoricalHistogramTemplate,
    ContinuousHistogramTemplate,
)


def test_cluster_sample(histograms: dict[str, Histogram]) -> None:
    """
    Test the sample method of the ClusterDescription class.

    :param histograms: Fixture with histograms to fill the cluster with.
    """
    cluster = ClusterDescription(histograms)

    sample_size = 1000
    samples = cluster.sample(sample_size)

    # Test the shape of the samples
    assert samples.shape == (sample_size, len(histograms))

    assert np.all(
        np.unique(samples["feature1"])
        == cast(CategoricalHistogram, histograms["feature1"]).values
    )

    feature2_lims = cast(ContinuousHistogramTemplate, histograms["feature2"]).lims
    feature3_lims = cast(ContinuousHistogramTemplate, histograms["feature3"]).lims

    # Test the range of the samples
    assert samples["feature2"].dtype == np.int_
    assert np.all(samples.iloc[:, 1] >= feature2_lims[0])
    assert np.all(samples.iloc[:, 1] <= feature2_lims[-1])
    assert samples["feature3"].dtype == np.float64
    assert np.all(samples.iloc[:, 2] >= feature3_lims[0])
    assert np.all(samples.iloc[:, 2] <= feature3_lims[-1])


def test_fit(data: pd.DataFrame, data_types: list[DataType]) -> None:
    """
    Test the fit method of the ClusterBasedGenerator class.

    :param data: Fixture with data to fit the generator on.
    :param data_types: Fixture with data types of the data.
    """
    generator = ClusterBasedGenerator(
        clusterer=KMeans(n_clusters=2, n_init="auto", init="random")
    )
    generator.fit(data, data_types)

    # Test whether the generator fits the correct number of clusters
    assert len(generator.clusters_) == 2
    assert len(generator.cluster_probs_) == 2


def test_sample(data: pd.DataFrame, data_types: list[DataType]) -> None:
    """
    Test the sample method of the ClusterBasedGenerator class.

    :param data: Fixture with data to fit the generator on.
    :param data_types: Fixture with data types of the data.
    """
    generator = ClusterBasedGenerator(
        clusterer=KMeans(n_clusters=2, n_init="auto", init="random")
    )
    generator.fit(data, data_types)

    samples = generator.sample(10)

    # Test the shape of the samples
    assert samples.shape == (10, len(data.columns))


def test_sample_custom_categorical_template_narrow(
    data: pd.DataFrame, data_types: list[DataType]
) -> None:
    """
    Test the sample method of the ClusterBasedGenerator class with a custom
    categorical histogram template for feature1, where the template specifies
    a subset of the values that is contained in the data.

    :param data: Fixture with data to fit the generator on.
    :param data_types: Fixture with data types of the data.
    """
    # "feature1": ["a", "b", "c", "a", "b", "e", "a"],
    feature1_template = CategoricalHistogramTemplate(values=np.array(["a", "f"]))

    generator = ClusterBasedGenerator(
        clusterer=KMeans(n_clusters=1, n_init="auto", init="random"),
        histogram_templates={"feature1": feature1_template},
    )
    generator.fit(data, data_types)
    samples = generator.sample(10)

    assert "a" in samples["feature1"].unique()
    assert ["b", "c", "d", "e", "f"] not in samples["feature1"].unique()


def test_sample_custom_categorical_template_misaligned(
    data: pd.DataFrame, data_types: list[DataType]
) -> None:
    """
    Test the sample method of the ClusterBasedGenerator class with a custom
    categorical histogram template for feature1, where the template specifies
    a set of values not contained in the data.

    :param data: Fixture with data to fit the generator on.
    :param data_types: Fixture with data types of the data.
    """
    # "feature1": ["a", "b", "c", "a", "b", "e", "a"],
    feature1_template = CategoricalHistogramTemplate(values=np.array(["f"]))

    generator = ClusterBasedGenerator(
        clusterer=KMeans(n_clusters=2, n_init="auto", init="random"),
        histogram_templates={"feature1": feature1_template},
    )
    generator.fit(data, data_types)
    with pytest.raises(ValueError):
        generator.sample(10)


def test_sample_custom_continuous_template_narrow(
    data: pd.DataFrame, data_types: list[DataType]
) -> None:
    """
    Test the sample method of the ClusterBasedGenerator class with a custom
    continuous histogram template for feature2, where the template specifies
    a range of values partly narrower than the range of values in the data.

    :param data: Fixture with data to fit the generator on.
    :param data_types: Fixture with data types of the data.
    """
    # "feature3": [3.0, 3.5, 4.0, 4.5, 6.25, 5.1, 7.0],
    feature3_template = ContinuousHistogramTemplate(lims=np.array([4, 6, 11]))

    generator = ClusterBasedGenerator(
        clusterer=KMeans(n_clusters=2, n_init="auto", init="random"),
        histogram_templates={"feature3": feature3_template},
    )
    generator.fit(data, data_types)
    samples = generator.sample(10)

    assert np.all(samples["feature3"] >= 4)
    assert np.all(samples["feature3"] <= 11)


def test_sample_custom_continuous_template_misaligned(
    data: pd.DataFrame, data_types: list[DataType]
) -> None:
    """
    Test the sample method of the ClusterBasedGenerator class with a custom
    continuous histogram template for feature2, where the template specifies
    a range of values not contained in the data.

    :param data: Fixture with data to fit the generator on.
    :param data_types: Fixture with data types of the data.
    """
    # "feature3": [3.0, 3.5, 4.0, 4.5, 6.25, 5.1, 7.0],
    feature3_template = ContinuousHistogramTemplate(lims=np.array([100, 1000]))

    generator = ClusterBasedGenerator(
        clusterer=KMeans(n_clusters=2, n_init="auto", init="random"),
        histogram_templates={"feature3": feature3_template},
    )
    generator.fit(data, data_types)
    with pytest.raises(ValueError):
        generator.sample(10)
