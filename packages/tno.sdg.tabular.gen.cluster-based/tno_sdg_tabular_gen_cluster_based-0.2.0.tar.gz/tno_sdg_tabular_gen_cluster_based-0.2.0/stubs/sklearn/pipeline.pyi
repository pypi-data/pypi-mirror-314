from __future__ import annotations

from typing import Any

from sklearn.base import BaseEstimator

class Pipeline(BaseEstimator):
    def __init__(self, steps: Any) -> None: ...
