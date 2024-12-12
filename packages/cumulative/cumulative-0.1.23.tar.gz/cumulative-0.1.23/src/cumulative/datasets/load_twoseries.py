import pandas as pd

from cumulative import Cumulative


def load_twoseries() -> Cumulative:
    """
    Load a dataset of two time series.
    """

    df = pd.DataFrame(
        {
            "base.x": [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3]],
            "base.y": [[10, 20, 30, 40, 50, 60], [5, 25, 15, 5]],
        }
    )

    c = Cumulative(df)

    c.lineage.track("load_twoseries")

    return c
