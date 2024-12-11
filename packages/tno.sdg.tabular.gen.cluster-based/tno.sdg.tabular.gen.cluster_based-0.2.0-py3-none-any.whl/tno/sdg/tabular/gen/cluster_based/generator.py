"""
This module contains the ClusterBasedGenerator class, which is used to generate
synthetic tabular data based on a clustering approach.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.cluster import KMeans
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from tno.sdg.tabular.gen.cluster_based.histogram import (
    HISTOGRAM_TEMPLATES,
    CategoricalHistogram,
    ContinuousHistogram,
    Histogram,
    HistogramTemplate,
)
from tno.sdg.tabular.gen.cluster_based.util import DataType

logger = logging.getLogger(__name__)


def empty_histogram_warning(
    histogram: Histogram, column: str, cluster: int, data_in_cluster: pd.DataFrame
) -> None:
    """
    Log a warning that a histogram is empty. When the logger level is set
    to DEBUG, additional information is logged.

    :param histogram: The empty histogram.
    :param column: The column for which the histogram is empty.
    :param cluster: The cluster for which the histogram is empty.
    :param data_in_cluster: The data that is in the cluster.
    """
    logger.warning(f"Empty histogram for column {column} in cluster {cluster}.")
    if logger.getEffectiveLevel() > logging.DEBUG:
        logger.warning("Set logger level to DEBUG to see more information.")

    if isinstance(histogram, ContinuousHistogram):
        logger.debug(
            f"...ContinuousHistogram.lims for column '{column}': \n{histogram.lims}."
        )
    if isinstance(histogram, CategoricalHistogram):
        logger.debug(
            f"...CategoricalHistogram.categories for column '{column}': \n{histogram.values}."
        )
    logger.debug(f"...data in cluster {cluster}: \n{data_in_cluster}")


def default_preprocessor(
    data: pd.DataFrame, data_types: Iterable[DataType]
) -> BaseEstimator:
    """
    Returns a generic data preprocessor. The continuous features are
    transformed using the StandardScaler, the categorical features are
    transformed using the OneHotEncoder.

    :param data: The data to base the preprocessing on. The preprocessing is
        not yet performed on this data. The data may instead be used to derive the
        necessary information for the preprocessing, such as the labels of
        a categorical feature.
    :param data_types: Indicate data types per variable. The size should be
        equal to the number of variables in data.
    :return: A generic data preprocessor.
    """
    data_types_: npt.NDArray[np.bytes_] = np.array(data_types)
    continuous = data.columns[data_types_ == DataType.CONTINUOUS]
    categorical = data.columns[data_types_ == DataType.CATEGORICAL]

    preprocesser: BaseEstimator = make_column_transformer(
        (StandardScaler(), continuous),
        (OneHotEncoder(), categorical),
        verbose=True,
        verbose_feature_names_out=True,
    )

    return preprocesser


_default_clusterer = KMeans(n_clusters=8, init="random", n_init="auto")


@dataclass
class ClusterDescription:
    """
    This class is used to describe a cluster of individuals, using
    histograms. For each feature, the cluster holds a histogram that holds the
    distribution of that feature. These histograms can be used to sample new
    synthetic individuals.
    """

    histograms: dict[str, Histogram] = field(default_factory=dict)

    def set_histogram(self, feature: str, histogram: Histogram) -> None:
        """
        Set the histogram for a feature.

        :param feature: Name of the feature.
        :param histogram: Histogram to add.
        """
        self.histograms[feature] = histogram

    def sample(self, sample_size: int) -> pd.DataFrame:
        """
        Draw samples from the cluster. A value is drawn from each of the
        histograms.

        :param sample_size: Number of samples that are drawn.
        :return: A dataframe with the sampled data. Each row is a sample, each
            column is a feature.
        """
        # for every variable we sample n values.
        sampled_data = []
        dtypes = []
        for histogram in self.histograms.values():
            sample = histogram.sample(sample_size)
            sampled_data.append(sample)
            dtypes.append(sample.dtype)

        sampled_data_cols = np.vstack(sampled_data).T
        df = pd.DataFrame(sampled_data_cols, columns=list(self.histograms.keys()))
        df = df.astype(dict(zip(df.columns, dtypes)))
        return df


class ClusterBasedGenerator:
    """
    This class is used to generate synthetic tabular data based on a clustering
    approach. The data is first clustered, then for each cluster a histogram is
    created for each feature. When sampling, a cluster is sampled first, then
    for each feature a value is sampled from the corresponding histogram.

    The model is captured by the following attributes:
    - clusters: list of clusters, each cluster containing a histogram for each feature.
    - cluster_probs: probability of sampling each cluster.
    """

    def __init__(
        self,
        preprocessor: BaseEstimator | None = None,
        clusterer: BaseEstimator | None = None,
        histogram_templates: dict[str, HistogramTemplate] | None = None,
    ) -> None:
        """
        Instantiate the cluster based synthetic tabular data generator.

        To use the model, first fit it to the data using the
        `ClusterBasedGenerator.fit` method, then sample synthetic data using
        the `ClusterBasedGenerator.sample` method.

        :param preprocessor: Preprocessor to use. If None, a default preprocessor
            is used.
        :param clusterer: Clusterer to use. If None, a default clusterer is used.
        :param histogram_templates: Optional dictionary of histogram templates,
            keyed by the feature name. If you wish to predefine the template of
            a histogram (such as which categories a feature has) instead of
            deriving the template from the data directly, you can provide the
            histogram templates here. It is not required to provide a template
            for each feature.
        """

        self.preprocessor = preprocessor
        self.clusterer = clusterer
        self.histogram_templates = histogram_templates or {}

        for col, template in self.histogram_templates.items():
            if not isinstance(template, HistogramTemplate):
                raise TypeError(
                    f"Expected a HistogramTemplate for column '{col}', "
                    f"but got {type(template)}."
                )
            template._validate()

        # Following the convention set by scikit-learn, we use a trailing
        # underscore for attributes that are set during fitting.

        self.columns_: list[str] = []
        """
        The columns of the data that was used to fit the model. This information is used
        to reconstruct a dataframe as output of the `ClusterBasedGenerator.sample` method.
        """
        self.dtypes_: npt.NDArray[np.generic] = np.array([])
        """
        The data types of the columns of the data that was used to fit the model. This
        information is used to reconstruct a dataframe as output of the
        `ClusterBasedGenerator.sample` method.
        """

        self.cluster_probs_: npt.NDArray[np.float64] = np.array([])
        """
        The probability of sampling a cluster, where the `i`'th element
        indicates the probability of sampling the `i`'th cluster.
        """
        self.clustering_ = np.array([])
        """
        The cluster that each input record (original, non-synthetic data)
        belongs to.
        """
        self.clusters_: list[ClusterDescription] = []
        """
        The cluster descriptions that were learned from the data, each
        describing the data of a specific cluster.
        """

        # The following attributes are meant for testing purposes, and set
        # after each call to `ClusterBasedGenerator.sample`.

        self._sampled_clusters: npt.NDArray[np.int_] | None = None
        """
        The cluster that was sampled for each synthetic record produced. This
        attribute is set when the `ClusterBasedGenerator.sample` method is
        called.
        """

    def fit(self, data: pd.DataFrame, data_types: Iterable[DataType]) -> None:
        """
        Learn a model of the provided data, to be used for generating synthetic
        data.

        The following steps are performed:
        1. Preprocess the data using `self.preprocessor`
        2. Cluster the data using `self.clusterer`
        3. For each cluster, create a histogram for each feature.

        This model is described by `self.clusters_` and `self.cluster_probs_`.

        :param data: The data to learn from.
        :param data_types: Indicate data types per variable. The size should be
            equal to the number of variables in data.
        """
        self.dtypes_ = data.dtypes.to_numpy()
        self.columns_ = data.columns.to_list()

        preprocessor = self.preprocessor or default_preprocessor(data, data_types)
        clusterer = self.clusterer or _default_clusterer

        self.clustering_ = Pipeline(
            [
                ("preprocesser", preprocessor),
                ("clusterer", clusterer),
            ]
        ).fit_predict(data)

        # Derive histogram templates from the data if they are not provided.
        histogram_templates: dict[str, HistogramTemplate] = {}
        for data_type, column in zip(data_types, data.columns):
            if column not in self.histogram_templates:
                histogram_templates[column] = HISTOGRAM_TEMPLATES[data_type].from_data(
                    data[column]
                )
            else:
                histogram_templates[column] = self.histogram_templates[column]

        # Then we create the histograms for each cluster.
        size_of_cluster = []
        self.clusters_.clear()
        for cluster in np.unique(self.clustering_):
            data_in_cluster = data.iloc[self.clustering_ == cluster]
            size_of_cluster.append(data_in_cluster.shape[0])

            cluster_description = ClusterDescription()
            for column, template_histogram in histogram_templates.items():
                histogram: Histogram = template_histogram.new()
                histogram.add_data(data_in_cluster[column].to_numpy())
                if histogram.is_empty():
                    empty_histogram_warning(histogram, column, cluster, data_in_cluster)
                cluster_description.set_histogram(column, histogram)
            self.clusters_.append(cluster_description)
        self.cluster_probs_ = np.array(size_of_cluster) / np.sum(size_of_cluster)

    def sample(self, n: int = -1, shuffle: bool = True) -> pd.DataFrame:
        """
        Sample synthetic data from the fitted model.

        :param n: The number of samples to draw. By default, the number of
            nodes generated is equal to the number of nodes in the original data.
        :param shuffle: Whether the data need to be shuffled after they have been generated.
        :return: Array with the samples. Every row is a sampled record, the columns indicate
            the different features.
        """
        if n == -1:
            n = len(self.clustering_)

        # we sample a cluster for every synthetic record.
        # the probability of sampling a cluster is proportional to the size of the cluster.
        sampled_clusters = np.random.choice(
            len(self.clusters_), size=n, p=self.cluster_probs_
        )
        unique_sampled_clusters, sampled_cluster_count = np.unique(
            sampled_clusters, return_counts=True
        )

        # list to store the data
        sampled_data_list = []
        for cluster, count in zip(unique_sampled_clusters, sampled_cluster_count):
            sampled_data_list.append(self.clusters_[cluster].sample(sample_size=count))

        sampled_data = np.vstack(sampled_data_list)
        order = np.arange(sampled_data.shape[0])

        if shuffle:
            np.random.shuffle(order)

        self._sampled_clusters = np.sort(sampled_clusters)[order]
        sampled_data = sampled_data[order]

        return pd.DataFrame(sampled_data, columns=self.columns_).astype(
            dict(zip(self.columns_, self.dtypes_))
        )
