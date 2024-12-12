import numpy as np
import pandas as pd

from cumulative.transforms.transform import Transform
from cumulative.utils.frames import drop_prefix


class ExceptionInvalidMethod(Exception):
    pass


class Score(Transform):
    def apply(self, src: str, func: callable = None, method: str = "value", reverse: bool = False) -> pd.DataFrame:
        """
        Extract a score from `src` column using `method`.
        Useful for sorting and setting colors.
        """

        if func:
            df = self.c.frame(src)
            df.columns = drop_prefix(src, df.columns)
            values = df.apply(func, axis=1)
        else:
            values = self.c.df[src].copy()
        if method == "value":
            values -= values.min()
            values /= values.max()
        elif method == "noscale":
            pass
        elif method == "argsort":
            values = np.argsort(values) / (values.shape[0] - 1)
        elif method == "index":
            values = np.linspace(0, 1, num=values.shape[0])
        else:
            raise ExceptionInvalidMethod(f"No valid method: '{method}'")

        if reverse:
            values = values[::-1]

        return pd.DataFrame({"value": values})
