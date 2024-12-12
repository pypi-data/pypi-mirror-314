import logging

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

from cumulative.opts import options
from cumulative.transforms.transform import Transform
from cumulative.utils.warnings import warn

log = logging.getLogger(__name__)


class InterpolationWarning(UserWarning):
    pass


class ExceptionInvalidMethod(Exception):
    pass


def interpolate_interp(x: np.ndarray, y: np.ndarray, k: int = 2) -> tuple[callable, dict]:
    """
    Interpolate x,y curve with `k` equidistant points using one-dimensional linear
    interpolation for monotonically increasing sample points.
    """

    # Percentile-based Linear Interpolation (PLI)
    xp = np.linspace(x[0], x[-1], num=k)
    yp = np.interp(xp, x, y)

    def m(x):
        return np.interp(x, xp, yp)

    attrs = {"model.name": "interp", "model.params": (xp, yp), "model.size": k * 2}

    return m, attrs


def interpolate_pchip(x: np.ndarray, y: np.ndarray) -> tuple[callable, dict]:
    """
    PCHIP 1-D monotonic cubic interpolation on x,y curve.
    The resulting interpolation passed thru all x,y points.
    """

    # possible source of warnings for PCHIP:
    # https://stackoverflow.com/questions/14461346/python-pchip-warnings

    # Seed the random number generator for reproducibility
    np.random.seed(options().get("reproducibility.random_seed"))

    m = PchipInterpolator(x, y)
    attrs = {"model.name": "pchip", "model.size": len(x) * 2}
    return m, attrs


def interpolate_pchipp(x: np.ndarray, y: np.ndarray, k: int = 2, p: np.ndarray | None = None) -> tuple[callable, dict]:
    """
    PCHIP 1-D monotonic cubic interpolation on `k` equi-distant (or `p`) percentiles.
    1. First, we fit a PCHIP model with all data points (x,y).
    2. We then extract the (x_hat,y_hat) pairs at percentiles x_hat (with k: equi-distant).
    3. We fit a new PCHIP model on (x_hat,y_hat), and return it.
    """

    # Seed the random number generator for reproducibility
    np.random.seed(options().get("reproducibility.random_seed"))

    m = PchipInterpolator(x, y)
    if p is None:
        p = np.linspace(0, 1, k)
    x = x[0] + (x[-1] - x[0]) * p
    xp = x[0] + (x[-1] - x[0]) * p
    yp = m(xp)

    m = PchipInterpolator(xp, yp)
    attrs = {"model.name": "pchipp", "model.params.x": xp, "model.params.y": yp, "model.size": len(xp) * 2}

    return m, attrs


def interpolate(x: np.ndarray, y: np.ndarray, method: str = "interp", **method_kwargs) -> tuple[callable, dict]:
    """
    Interpolate x,y curve using `method` and its key arguments, returning a callable
    to generate Y values from an X array, and interpolation properties. In case of errors,
    an "error" key is also added, with an error message.
    """

    try:
        if method == "interp":
            m, attrs = interpolate_interp(x, y, **method_kwargs)
        elif method == "pchip":
            m, attrs = interpolate_pchip(x, y, **method_kwargs)
        elif method == "pchipp":
            m, attrs = interpolate_pchipp(x, y, **method_kwargs)
        else:
            raise ExceptionInvalidMethod(f"No valid method: '{method}'")
    except (RuntimeError, TypeError, ValueError) as e:
        error = f"{__name__}: {e.__class__.__name__}: {e}"
        warn(error, category=InterpolationWarning, stacklevel=1)
        attrs = {"model.name": method, "error": error}

        def m(x):
            return np.full(x.shape, np.nan)

    return m, attrs


class Interpolate(Transform):
    def transform_row(
        self, row: pd.Series, src: str, method: str = "interp", num: int = 1000, **method_kwargs
    ) -> pd.Series:
        """
        Interpolate  x,y arrays with prefix `src` using `method` and `num` data points.
        """
        func, attrs = interpolate(row[f"{src}.x"], row[f"{src}.y"], method, **method_kwargs)
        x = np.linspace(row[f"{src}.x"][0], row[f"{src}.x"][-1], num=num)
        y = func(x)
        z = func(row[f"{src}.x"])
        return pd.Series({"x": x, "y": y, "z": z} | attrs)
