import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

from cumulative import Cumulative


def load_sklearn(func: callable = load_iris) -> Cumulative:
    """
    Load a scikit-learn dataset by passing the loading function `func`.
    """

    data, target = func(return_X_y=True)
    df = pd.DataFrame(data).apply(
        lambda row: pd.Series({"base.x": np.arange(row.values.shape[0]), "base.y": row.values}), axis=1
    )
    df["base.z"] = target
    c = Cumulative(df)
    c.meta.name = func.__name__

    return c
