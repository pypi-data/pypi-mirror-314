from typing import Optional

import numpy as np

from cumulative.cumulative import Cumulative
from cumulative.opts import options


def get_minmax(c: Cumulative, src: Optional[str] = None, expand: float = 0):
    """
    Get min, max values for X/Y dimensions. `expand` is added as
    a percentage increase to increase the covered area.
    """

    src = options().get("transforms.src", prefer=src)

    x_min = c.df[f"{src}.x"].apply(lambda a: np.min(a)).min()
    x_max = c.df[f"{src}.x"].apply(lambda a: np.max(a)).max()
    y_min = c.df[f"{src}.y"].apply(lambda a: np.min(a)).min()
    y_max = c.df[f"{src}.y"].apply(lambda a: np.max(a)).max()

    x_min -= (x_max - x_min) * expand
    x_max += (x_max - x_min) * expand
    y_min -= (y_max - y_min) * expand
    y_max += (y_max - y_min) * expand

    return {"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max}
