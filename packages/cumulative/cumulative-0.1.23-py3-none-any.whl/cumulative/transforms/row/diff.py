import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform


def diff(values: np.ndarray, prefix: str) -> dict:
    """
    Return dictionary with diff of `values`, nested in key `prefix`.
    Inverse of .cumsum().
    """
    return {f"{prefix}": np.diff(values, prepend=0)}


class Diff(Transform):
    def transform_row(self, row: pd.Series, src: str, kind: str = "y") -> pd.Series:
        """
        Apply diff to `kind` dimensions in prefix `src`.
        """

        if kind == "xy":
            x = diff(row[f"{src}.x"], "x")
            y = diff(row[f"{src}.y"], "y")
        elif kind == "x":
            x = diff(row[f"{src}.x"], "x")
            y = {"y": row[f"{src}.y"]}
        elif kind == "y":
            x = {"x": row[f"{src}.x"]}
            y = diff(row[f"{src}.y"], "y")

        return pd.Series({**x, **y})
