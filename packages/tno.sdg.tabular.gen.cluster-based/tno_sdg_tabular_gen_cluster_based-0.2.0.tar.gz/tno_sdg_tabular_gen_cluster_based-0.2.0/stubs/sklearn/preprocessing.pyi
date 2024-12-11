from sklearn.base import BaseEstimator, TransformerMixin

class _BaseEncoder(TransformerMixin, BaseEstimator): ...

class StandardScaler(_BaseEncoder):
    def __init__(
        self,
        copy: bool = True,
        with_mean: bool = True,
        with_std: bool = True,
    ) -> None: ...

class OneHotEncoder(_BaseEncoder): ...
