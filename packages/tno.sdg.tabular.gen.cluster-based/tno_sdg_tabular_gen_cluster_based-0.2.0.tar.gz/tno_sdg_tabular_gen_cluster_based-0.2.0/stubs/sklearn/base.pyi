from __future__ import annotations

import sys

import numpy as np
from numpy.typing import ArrayLike, NDArray

if sys.version_info <= (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

class BaseEstimator:
    def fit(self, X: ArrayLike, y: ArrayLike | None = None) -> Self: ...
    def predict(self, X: ArrayLike) -> NDArray[np.int_]: ...
    def fit_predict(
        self, X: ArrayLike, y: ArrayLike | None = None
    ) -> NDArray[np.int_]: ...

class TransformerMixin: ...
