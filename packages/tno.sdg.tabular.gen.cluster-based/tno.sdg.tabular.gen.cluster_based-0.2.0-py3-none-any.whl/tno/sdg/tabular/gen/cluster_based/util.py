"""
This file contains the definition of the DataType enum.
"""

from enum import Enum


class DataType(Enum):
    """
    Enum for the different data types that can be used for binning.
    """

    CONTINUOUS = "Continuous"
    CATEGORICAL = "Categorical"
