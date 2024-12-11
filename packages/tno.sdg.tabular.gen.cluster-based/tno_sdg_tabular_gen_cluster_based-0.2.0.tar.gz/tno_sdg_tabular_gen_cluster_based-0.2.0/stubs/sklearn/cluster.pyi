from typing import Any, Union

from sklearn.base import BaseEstimator

class KMeans(BaseEstimator):
    def __init__(
        self,
        n_clusters: int,
        *args: Any,
        init: str = "k-means++",
        n_init: Union[int, str] = "warn",
        max_iter: int = 300,
        tol: float = 1e-4,
        verbose: int = 0,
        random_state: Any = None,
        copy_x: bool = True,
        algorithm: str = "lloyd",
    ) -> None: ...
