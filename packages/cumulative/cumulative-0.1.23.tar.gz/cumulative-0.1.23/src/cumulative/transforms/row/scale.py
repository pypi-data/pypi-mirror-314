import logging

import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform

log = logging.getLogger(__name__)


def scale(values: np.ndarray, prefix: str) -> dict:
    """
    Scale `values` to [0,1] range with `prefix` keys.
    """

    v_min = np.min(values)
    v_max = np.max(values)

    if v_min == v_max:  # minmax scaling not defined, defaulting to 1
        V = np.full(values.shape[0], 1.0)
    else:
        V = (values - v_min) / (v_max - v_min)
    return {f"{prefix}": V, f"{prefix}.min": v_min, f"{prefix}.max": v_max}


class Scale(Transform):
    def transform_row(self, row: pd.Series, src: str, kind: str = "y") -> pd.Series:
        """
        Apply minmax normalization to range [0,1] for `kind` dimensions ("x", "y" or "xy").
        """

        if kind == "xy":
            x = scale(row[f"{src}.x"], "x")
            y = scale(row[f"{src}.y"], "y")
        elif kind == "x":
            x = scale(row[f"{src}.x"], "x")
            y = {"y": row[f"{src}.y"]}
        elif kind == "y":
            x = {"x": row[f"{src}.x"]}
            y = scale(row[f"{src}.y"], "y")

        return pd.Series({**x, **y})
