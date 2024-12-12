import numpy as np
import pandas as pd

from cumulative import Cumulative


def load_zeros(n: int = 100, m: int = 100) -> Cumulative:
    """
    Load a dataset of `n` sries of length `m`, filled with zeros.
    """

    df = pd.DataFrame(index=range(n))
    df["base.x"] = [np.zeros(m) for _ in range(len(df))]
    df["base.y"] = [np.zeros(m) for _ in range(len(df))]

    c = Cumulative(df)

    c.lineage.track("load_zeros")

    return c
