from typing import Any

from sklearn.base import BaseEstimator

def make_column_transformer(
    *args: tuple[BaseEstimator, Any],
    verbose: bool = False,
    verbose_feature_names_out: bool = False,
) -> BaseEstimator: ...
