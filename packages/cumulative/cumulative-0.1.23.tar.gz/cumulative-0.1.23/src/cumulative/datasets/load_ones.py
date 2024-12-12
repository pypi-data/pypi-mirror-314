import numpy as np
import pandas as pd

from cumulative import Cumulative


def load_ones(n: int = 100, m: int = 100) -> Cumulative:
    """
    Load a dataset of `n` sries of length `m`, filled with ones.
    """

    df = pd.DataFrame(index=range(n))
    df["base.x"] = [np.ones(m) for _ in range(len(df))]
    df["base.y"] = [np.ones(m) for _ in range(len(df))]

    c = Cumulative(df)

    c.lineage.track("load_ones")

    return c
