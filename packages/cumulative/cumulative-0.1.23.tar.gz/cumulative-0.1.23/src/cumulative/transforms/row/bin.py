import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform


def bin_values(values: np.ndarray, num: int, prefix: str) -> dict:
    """
    Given `values`, bin them in `num` equidistant bins`.
    """
    bins = np.linspace(values[0], values[-1], num=num)
    values_hat = bins[np.searchsorted(bins, values)]
    return {f"{prefix}": values_hat}


class Bin(Transform):
    def transform_row(self, row: pd.Series, src: str, kind: str = "y", num: int = 10):
        """
        Simplify curve binning Y values on `num` bins. `kind` control the source
        of the values: "x", "y", or "xy" (both "x" and "y", independently.)
        """

        if kind == "xy":
            x = bin_values(row[f"{src}.x"], num, "x")
            y = bin_values(row[f"{src}.y"], num, "y")
        elif kind == "x":
            x = bin_values(row[f"{src}.x"], num, "x")
            y = {"y": row[f"{src}.y"]}
        elif kind == "y":
            x = {"x": row[f"{src}.x"]}
            y = bin_values(row[f"{src}.y"], num, "y")

        return pd.Series({**x, **y})
