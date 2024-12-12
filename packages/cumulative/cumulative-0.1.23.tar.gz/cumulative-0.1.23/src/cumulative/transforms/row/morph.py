import logging

import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform

log = logging.getLogger(__name__)


def morph(a: np.ndarray, b: np.ndarray, pct: float, name: str) -> dict:
    """
    Morph `a` to `b` by a percentage `pct` with `prefix` prefix.
    """

    return {name: a * (1 - pct) + b * pct}


class Morph(Transform):
    def transform_row(self, row: pd.Series, src: str, src2: str, pct: float = 0.5) -> pd.Series:
        """
        Morph `src` to `src2` by a percentage. Series length must be equal.
        """

        x = morph(row[f"{src}.x"], row[f"{src2}.x"], pct, "x")
        y = morph(row[f"{src}.y"], row[f"{src2}.y"], pct, "y")

        return pd.Series({**x, **y})
