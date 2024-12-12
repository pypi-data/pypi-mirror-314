import numpy as np
import pandas as pd

from cumulative import Cumulative


def load_xy(n: int = 100, m: int = 100) -> Cumulative:
    """
    Load a dataset of `n` series of length `m`, x=y in the interval [0,1].
    """

    df = pd.DataFrame(index=range(n))
    df["base.x"] = [np.linspace(0, 1, m) for _ in range(n)]
    df["base.y"] = [np.linspace(0, 1, m) for _ in range(n)]

    c = Cumulative(df)

    c.lineage.track("load_xy")

    return c
