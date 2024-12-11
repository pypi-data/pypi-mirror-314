"""
This module provides a simple histogram class, that can be used to sample from.
"""

from __future__ import annotations

import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd

from tno.sdg.tabular.gen.cluster_based.util import DataType

if sys.version_info >= (3, 12):
    from typing import Self, override
else:
    from typing_extensions import Self, override

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HistogramTemplate(ABC):
    """
    A HistogramTemplate is used to create a new histogram.

    The template contains the information needed to create a new histogram,
    such as the limits of the bins for a ContinuousHistogram. This main purpose
    of this class is to allow the user to bring their own histogram template.
    """

    @abstractmethod
    def _validate(self) -> None:
        """
        Check if the histogram template is valid.

        :raises ValueError: If the histogram template is invalid.
        """

    @abstractmethod
    def new(self) -> Histogram:
        """
        Create a new histogram based on the template.

        :return: A new histogram.
        """

    @classmethod
    @abstractmethod
    def from_data(  # pylint: disable=missing-param-doc
        cls,
        data: pd.Series[Any] | npt.NDArray[Any],
        *_args: Any,
        **_kwargs: Any,
    ) -> Self:
        """
        Create a histogram template for a feature directly from data.

        :param data: A feature for which we get a histogram.
        :return: A histogram for the feature.
        """


class Histogram(ABC):
    """
    The Histogram class represents a histogram for a feature.

    The histogram has a definition of bins (implementation depending on data
    type) and keeps track of the frequencies, i.e. the number of values in each
    bin. The histogram can be sampled to generate new values.

    At the very minimum, a histogram must be initialized with the limits of the
    bins. The frequencies can be set during initialization or at a later point through
    `Histogram.add_data`.
    """

    def __init__(self, frequencies: npt.NDArray[np.int_]) -> None:
        self.frequencies = frequencies

    @abstractmethod
    def sample(self, n: int) -> npt.NDArray[Any]:
        """
        Sample n values from a histogram, by iteratively sampling a bin and
        then a uniform sample from that bin.

        :param n:  size.
        :return: sampled values
        """

    def is_empty(self) -> bool:
        """
        Check if the histogram is empty.

        :return: True if the histogram is empty, False otherwise.
        """
        return bool(np.sum(self.frequencies) == 0)

    @abstractmethod
    def copy(self, clear: bool = False) -> Self:
        """
        Create a copy of the histogram.

        :param clear: If True, the frequencies are set to zero.
        :return: A copy of the histogram.
        """

    @abstractmethod
    def add_data(self, data: npt.NDArray[np.float64]) -> None:
        """
        Add data to the histogram.

        The existing frequencies are updated.
        This method requires that the histogram has already been initialized.

        :param data: The data to add to the histogram.
        """

    @classmethod
    @abstractmethod
    def from_data(  # pylint: disable=missing-param-doc
        cls,
        data: npt.NDArray[Any],
        *_args: Any,
        **_kwargs: Any,
    ) -> Histogram:
        """
        Create a histogram for a feature directly from data.

        This method will return a fully initialized histogram with both
        the limits and frequencies set based on the data.

        The provided data type is used to determine the type of histogram to
        create.

        :param data: A feature for which to create a histogram.
        :return: A histogram for the feature.
        """


@dataclass(frozen=True)
class ContinuousHistogramTemplate(HistogramTemplate):
    """
    A ContinuousHistogramTemplate describes a template for creating
    ContinuousHistograms. The description contains the limits of the bins.
    """

    lims: npt.NDArray[np.float64] | npt.NDArray[np.int_]
    precision: int = 2
    dtype: np.dtype[Any] | None = None

    @override
    def _validate(self) -> None:
        """
        Check if the histogram template is valid.

        :return: True if the histogram template is valid, False otherwise.
        """
        if len(self.lims) < 2:
            raise ValueError(
                "At least one bin must provided, defined by a starting and ending limit."
            )
        if any(start >= end for (start, end) in zip(self.lims[:-1], self.lims[1:])):
            raise ValueError(
                "The limits must be in increasing order, i.e., "
                "the first limit of a bin must be smaller than the second."
            )
        if self.precision < 0:
            raise ValueError("Precision must be larger than or equal to zero.")

    @override
    def new(self) -> Histogram:
        """
        Create a new histogram based on the template.

        :return: A new histogram.
        """
        return ContinuousHistogram(
            self.lims, precision=self.precision, dtype=self.dtype
        )

    @classmethod
    def from_data(  # pylint: disable=missing-param-doc
        cls,
        data: pd.Series[Any] | npt.NDArray[Any],
        *_args: Any,
        bins: str | int | npt.NDArray[Any] = "auto",
        **_kwargs: Any,
    ) -> Self:
        """
        Create a histogram for a continuous feature directly from data.

        This method will return a fully initialized histogram with both
        the limits and frequencies set based on the data.

        :param data: A feature for which we get a histogram.
        :param bins: Choose the binning method used in numpy
            histogram. It can either be a string that defines the method or an
            integer that defines the number of bins. For options, see
            https://numpy.org/doc/stable/reference/generated/numpy.histogram.html.
        :raises ValueError: If the binning method is unknown.
        :return: A histogram for the continuous feature.
        """
        h = ContinuousHistogram.from_data(data, bins=bins)
        return cls(h.lims, precision=h.precision, dtype=h.dtype)


class ContinuousHistogram(Histogram):
    """
    The ContinuousHistogram class implements a histogram for continuous data.
    """

    def __init__(
        self,
        lims: npt.NDArray[np.float64] | npt.NDArray[np.int_],
        frequencies: npt.NDArray[np.int_] | None = None,
        precision: int = 2,
        dtype: np.dtype[Any] | None = None,
    ) -> None:
        """
        Create a histogram for a feature.

        :param lims: Numpy array where the elements indicate where the bins
            begin and end. For example, np.array([0,1,2]), would mean that
            there is a bin from 0-1 and a bin from 1-2, i.e., lims has one more
            element than the number of bins. The limits of the bins can be
            added to enforce these limits when the bin is created based on the
            data or to define a histogram using limits and frequencies without
            specifying a dataset. See `ContinuousHistogram.from_data` for
            automatically setting the limits based on the data.
        :param frequencies: Numpy array that indicates the "height", i.e.,
            density, of each bin.
        """
        ContinuousHistogramTemplate(lims, precision, dtype)._validate()

        if frequencies is not None and len(lims) != len(frequencies) + 1:
            raise ValueError(
                "The number of limits must be one more than the number of frequencies."
            )

        super().__init__(
            frequencies=(
                frequencies
                if frequencies is not None
                else np.zeros(len(lims) - 1, dtype=np.int_)
            )
        )

        self.lims = lims
        self.precision = precision
        self.dtype = dtype or lims.dtype

        self.sampled_bins_: npt.NDArray[Any] | None = None
        """
        Keeps track of the bins that were sampled from. Can be used to deduct
        statistical tests. Set each time when `Histogram.sample` is called.
        """

    @override
    def add_data(self, data: npt.NDArray[np.float64]) -> None:
        frequencies, _ = np.histogram(data, bins=self.lims, density=False)
        self.frequencies += frequencies

    @override
    def copy(self, clear: bool = False) -> Self:
        """
        Create a copy of the histogram.

        :param clear: If True, the frequencies are set to zero.
        :return: A copy of the histogram.
        """
        if clear:
            return type(self)(self.lims)
        frequencies = self.frequencies.copy() if self.frequencies is not None else None
        return type(self)(self.lims, frequencies=frequencies)

    @override
    def sample(self, n: int) -> npt.NDArray[Any]:
        """
        Sample n values from a histogram, by iteratively sampling a bin and
        then a uniform sample from that bin.

        :param n: number of samples.
        :raises ValueError: If n is smaller than or equal to zero.
        :return: sampled values.
        """
        if n <= 0:
            raise ValueError(f"n must be larger than zero, not {n}")
        if self.is_empty():
            raise ValueError("Cannot sample from an empty histogram.")

        samples = np.zeros(n, dtype=np.float64)
        n_bins = len(self.frequencies)
        bin_probs = self.frequencies / np.sum(self.frequencies)

        sampled_bins = np.random.choice(np.arange(n_bins), n, p=bin_probs)
        unique_sampled_bin = np.unique(sampled_bins)
        for bin_i in unique_sampled_bin:
            is_in_b = sampled_bins == bin_i
            samples[is_in_b] = np.random.uniform(
                self.lims[bin_i], self.lims[bin_i + 1], np.sum(is_in_b)
            )
        samples = np.round(samples, self.precision)

        self.sampled_bins_ = sampled_bins
        return samples.astype(self.dtype)

    @classmethod
    def from_data(  # pylint: disable=missing-param-doc
        cls,
        data: pd.Series[float | int] | npt.NDArray[np.float64] | npt.NDArray[np.int_],
        *_args: Any,
        bins: str | int | npt.NDArray[Any] = "auto",
        **_kwargs: Any,
    ) -> Self:
        """
        Create a histogram for a continuous feature directly from data.

        This method will return a fully initialized histogram with both
        the limits and frequencies set based on the data.

        :param data: A feature for which we get a histogram.
        :param bins: Choose the binning method used in numpy
            histogram. It can either be a string that defines the method or an
            integer that defines the number of bins. For options, see
            https://numpy.org/doc/stable/reference/generated/numpy.histogram.html.
        :raises ValueError: If the binning method is unknown.
        :return: A histogram for the continuous feature.
        """
        if isinstance(bins, str) and bins != "auto":
            raise ValueError(f"Unknown binning method {bins}")

        frequencies, lims = np.histogram(data, bins=bins, density=False)

        precision = Decimal(str(data[0])).as_tuple().exponent
        if not isinstance(precision, int):
            raise ValueError(f"Precision is not an integer: {precision}")
        precision = abs(precision)

        if not isinstance(data.dtype, np.dtype):
            raise ValueError(f"Data type is not a numpy data type: {data.dtype}")
        return cls(lims, frequencies=frequencies, precision=precision, dtype=data.dtype)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.lims}, {self.frequencies})"


@dataclass(frozen=True)
class CategoricalHistogramTemplate(HistogramTemplate):
    """
    A CategoricalHistogramTemplate describes a template for creating
    CategoricalHistograms. The description contains the categories (values)
    that the categorical value can take on.
    """

    values: npt.NDArray[Any]
    dtype: np.dtype[Any] | None = None

    @override
    def _validate(self) -> None:
        """
        Check if the histogram template is valid.

        :raises ValueError: If the histogram template is invalid.
        """
        if len(self.values) < 1:
            raise ValueError("At least one value must be provided.")
        if len(self.values) != len(np.unique(self.values)):
            raise ValueError("Values must be unique.")

    @override
    def new(self) -> Histogram:
        """
        Create a new histogram based on the template.

        :return: A new histogram.
        """
        return CategoricalHistogram(self.values, dtype=self.dtype)

    @classmethod
    def from_data(  # pylint: disable=missing-param-doc
        cls,
        data: pd.Series[int | str] | npt.NDArray[np.int_] | npt.NDArray[np.str_],
        *_args: Any,
        dtype: np.dtype[Any] | None = None,
        **_kwargs: Any,
    ) -> Self:
        """
        Create a histogram for a categorical feature directly from data.

        This method will return a fully initialized histogram with both
        the values and frequencies set based on the data.

        :param data: A feature for which we get a histogram.
        :return: A histogram for the categorical feature.
        """
        values = np.unique(data, return_counts=False)
        return cls(values=values, dtype=dtype)


class CategoricalHistogram(Histogram):
    """
    The CategoricalHistogram class implements a histogram for categorical data.
    """

    def __init__(
        self,
        values: npt.NDArray[Any],
        frequencies: npt.NDArray[np.int_] | None = None,
        dtype: Any | None = None,
    ) -> None:
        super().__init__(
            frequencies=(
                frequencies
                if frequencies is not None
                else np.zeros_like(values, dtype=np.int_)
            )
        )

        self.dtype = dtype or values.dtype
        self.values = values

        CategoricalHistogramTemplate(values, dtype)._validate()
        if len(values) != len(self.frequencies):
            raise ValueError("Values and frequencies must have the same length.")

    @override
    def sample(self, n: int) -> npt.NDArray[Any]:
        """
        Sample n values from a histogram, by iteratively sampling a bin and
        then a uniform sample from that bin.

        :param n: number of samples.
        :raises ValueError: If n is smaller than or equal to zero.
        :return: sampled values.
        """
        if n <= 0:
            raise ValueError(f"n must be larger than zero, not {n}")
        if self.frequencies is None:
            raise ValueError("Frequencies must be set before sampling.")
        if self.is_empty():
            raise ValueError("Cannot sample from an empty histogram.")

        densities = self.frequencies / np.sum(self.frequencies).astype(np.float64)
        return np.random.choice(self.values, n, p=densities).astype(self.dtype)

    @override
    def copy(self, clear: bool = False) -> Self:
        """
        Create a copy of the histogram.

        :param clear: If True, the frequencies are set to zero.
        :return: A copy of the histogram.
        """
        if clear:
            return type(self)(self.values)
        frequencies = self.frequencies.copy() if self.frequencies is not None else None
        return type(self)(self.values, frequencies=frequencies)

    @override
    def add_data(self, data: npt.NDArray[Any] | pd.Series[Any]) -> None:
        if self.frequencies is None:
            raise ValueError("Frequencies must be set before adding data.")

        values, counts = np.unique(data, return_counts=True)
        for value, count in zip(values, counts):
            self.frequencies[np.where(self.values == value)] += count

    @classmethod
    def from_data(  # pylint: disable=missing-param-doc
        cls,
        data: pd.Series[int | str] | npt.NDArray[np.int_] | npt.NDArray[np.str_],
        *_args: Any,
        **_kwargs: Any,
    ) -> CategoricalHistogram:
        """
        Create a histogram for a categorical feature directly from data.

        This method will return a fully initialized histogram with both
        the values and frequencies set based on the data.

        :param data: A feature for which we get a histogram.
        :return: A histogram for the categorical feature.
        """
        values, counts = np.unique(data, return_counts=True)
        return CategoricalHistogram(values, frequencies=counts)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.values}, {self.frequencies})"


HISTOGRAM_TEMPLATES: dict[DataType, type[HistogramTemplate]] = {
    DataType.CATEGORICAL: CategoricalHistogramTemplate,
    DataType.CONTINUOUS: ContinuousHistogramTemplate,
}

HISTOGRAMS: dict[DataType, type[Histogram]] = {
    DataType.CATEGORICAL: CategoricalHistogram,
    DataType.CONTINUOUS: ContinuousHistogram,
}
