from typing import Optional

import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform
from cumulative.utils.frames import rows_with_prefix


class RowApply(Transform):
    def transform_row(self, row: pd.Series, src: str, func: callable = None, **kwargs) -> pd.Series:
        """
        Apply `func` to `row`, with `src` column prefix omitted to increase reusability.
        """

        row = row[rows_with_prefix(row, src)]
        row.index = [col.removeprefix(f"{src}.") for col in row.index]

        return pd.Series(func(row, **kwargs))


def mid_points(row, pct: float = 0.5, rand: Optional[float] = None) -> pd.Series:

    if rand is not None:
        pct += np.random.random() * rand

    length = row["x"].shape[0]
    i = int(np.clip(row["x"].shape[0] / 2 - row["x"].shape[0] * pct / 2, min=0, max=length + 1))
    j = int(np.clip(row["x"].shape[0] / 2 + row["x"].shape[0] * pct / 2, min=0, max=length + 1))
    return pd.Series({"x": row["x"][i:j], "y": row["y"][i:j]})


def start_zero(row: pd.Series) -> pd.Series:
    """
    Insert [0,0] as first pair for series x,y
    """

    row["x"] = np.insert(row["x"], 0, 0)
    row["y"] = np.insert(row["y"], 0, 0)
    return row


def last_x_nonzero_y(row: pd.Series, col: str = "value") -> pd.Series:
    """
    Sets `col` to the last value in x with a nonzero value on y,
    useful to trim ending zeros on y.
    """

    row[col] = row["x"][np.flatnonzero(row["y"])[-1]]
    return row


def limit_region(
    row: pd.Series, x_min: float = None, x_max: float = None, y_min: float = None, y_max: float = None
) -> pd.Series:
    """
    Limit x,y to a region [x_min,x_max] and [y_min,y_max]
    """

    if isinstance(x_min, str):
        x_min = row[x_min]
    if isinstance(x_max, str):
        x_max = row[x_max]
    if isinstance(y_min, str):
        y_min = row[y_min]
    if isinstance(y_max, str):
        y_max = row[y_max]

    m = np.ones_like(row["x"], dtype=bool)

    if x_min:
        m &= row["x"] >= x_min

    if x_max:
        m &= row["x"] <= x_max

    if y_min:
        m &= row["y"] >= y_min

    if y_max:
        m &= row["y"] <= y_max

    row["x"] = row["x"][m]
    row["y"] = row["y"][m]

    return row
