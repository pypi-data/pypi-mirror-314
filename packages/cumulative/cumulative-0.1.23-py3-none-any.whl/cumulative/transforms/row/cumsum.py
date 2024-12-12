import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform


def cumsum(values: np.ndarray, prefix: str) -> dict:
    """
    Return dictionary with cumulative sum of `values`, nested in key `prefix`.
    """
    return {f"{prefix}": np.cumsum(values)}


class CumSum(Transform):
    def transform_row(self, row: pd.Series, src: str, kind: str = "y") -> pd.Series:
        """
        Apply cumulative sum to `kind` dimension(s) ("x", "y", or "xy") from
        prefix `src`.
        """

        if kind == "xy":
            x = cumsum(row[f"{src}.x"], "x")
            y = cumsum(row[f"{src}.y"], "y")
        elif kind == "x":
            x = cumsum(row[f"{src}.x"], "x")
            y = {"y": row[f"{src}.y"]}
        elif kind == "y":
            x = {"x": row[f"{src}.x"]}
            y = cumsum(row[f"{src}.y"], "y")

        return pd.Series({**x, **y})
