import logging

import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform

log = logging.getLogger(__name__)


def diagonal(row, src):
    length = row[f"{src}.x"].shape[0]
    x0 = row[f"{src}.x"][0]
    x1 = row[f"{src}.x"][-1]
    y0 = row[f"{src}.y"][0]
    y1 = row[f"{src}.y"][-1]

    x = {"x": np.linspace(x0, x1, length)}
    y = {"y": np.linspace(y0, y1, length)}

    return x, y


def horizon(row, src):
    length = row[f"{src}.x"].shape[0]
    x0 = row[f"{src}.x"][0]
    x1 = row[f"{src}.x"][-1]
    y0 = row[f"{src}.y"][0]
    y1 = row[f"{src}.y"][-1]
    y2 = (y0 + y1) / 2

    x = {"x": np.linspace(x0, x1, length)}
    y = {"y": np.linspace(y2, y2, length)}

    return x, y


def gravity(row, src):
    length = row[f"{src}.x"].shape[0]
    x0 = row[f"{src}.x"][0]
    x1 = row[f"{src}.x"][-1]
    x2 = (x0 + x1) / 2
    y0 = row[f"{src}.y"][0]
    y1 = row[f"{src}.y"][-1]

    x = {"x": np.linspace(x2, x2, length)}
    y = {"y": np.linspace(y0, y1, length)}

    return x, y


def center(row, src):
    length = row[f"{src}.x"].shape[0]
    x0 = row[f"{src}.x"][0]
    x1 = row[f"{src}.x"][-1]
    x2 = (x0 + x1) / 2
    y0 = row[f"{src}.y"][0]
    y1 = row[f"{src}.y"][-1]
    y2 = (y0 + y1) / 2

    x = {"x": np.linspace(x2, x2, length)}
    y = {"y": np.linspace(y2, y2, length)}

    return x, y


def normalized_tunable_sigmoid(x, k=0.5):
    """
    Normalized tunable sigmoid function, with k in [-1,1].
    https://dhemery.github.io/DHE-Modules/technical/sigmoid/
    """

    k = min(k, 1 - 1e-5)
    y = (1 - k) * (2 * x + -1) / (k - 2 * k * np.abs(2 * x + -1) + 1) * 0.5 + 0.5
    return y


def const(row, src, x_value=None, y_value=None):
    length = row[f"{src}.x"].shape[0]

    if x_value:
        x = {"x": np.linspace(x_value, x_value, length)}
    else:
        x = {"x": row[f"{src}.x"]}
    if y_value:
        y = {"y": np.linspace(y_value, y_value, length)}
    else:
        y = {"y": row[f"{src}.y"]}

    return x, y


def sigmoid(row, src, k=0.5):
    length = row[f"{src}.x"].shape[0]
    x0 = row[f"{src}.x"][0]
    x1 = row[f"{src}.x"][-1]

    x = {"x": np.linspace(x0, x1, length)}
    y = {"y": normalized_tunable_sigmoid(x["x"], k=k)}

    return x, y


def randomness(row, src, k=1):
    length = row[f"{src}.x"].shape[0]
    x = {"x": row[f"{src}.x"]}
    y = {"y": np.random.rand(length) * k}

    return x, y


def zeros(row, src, length=10):
    x = {"x": np.linspace(0, 1, length)}
    y = {"y": np.zeros(length)}

    return x, y


class Template(Transform):
    def transform_row(self, row: pd.Series, src: str, method: str = "diagonal", **kwargs) -> pd.Series:
        """
        Construct a templated series of type `name` from `src`.
        """

        if method == "diagonal":
            x, y = diagonal(row, src, **kwargs)
        elif method == "horizon":
            x, y = horizon(row, src, **kwargs)
        elif method == "gravity":
            x, y = gravity(row, src, **kwargs)
        elif method == "center":
            x, y = center(row, src, **kwargs)
        elif method == "sigmoid":
            x, y = sigmoid(row, src, **kwargs)
        elif method == "const":
            x, y = const(row, src, **kwargs)
        elif method == "random":
            x, y = randomness(row, src, **kwargs)
        elif method == "zeros":
            x, y = zeros(row, src, **kwargs)

        return pd.Series({**x, **y})
