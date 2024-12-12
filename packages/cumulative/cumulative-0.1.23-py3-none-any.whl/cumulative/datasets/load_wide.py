import pandas as pd

from cumulative import Cumulative
from cumulative.loaders.preprocess import melt, nest


def load_wide() -> Cumulative:
    """
    Load a dataset of time series in wide format with numerical and categorical columns.
    """

    df = pd.DataFrame(
        {
            "id": ["S1", "S2", "S3"],
            "category": ["A", "A", "B"],
            "t1": [5, 10, 5],
            "t2": [10, 15, 10],
            "t3": [30, 35, 15],
            "t4": [50, 55, 20],
            "t5": [20, 60, 25],
            "rate": [5, 2, 8],
        }
    )

    df = melt(df, group="id", attributes=["category", "rate"])
    df = nest(df)

    c = Cumulative(df)

    c.lineage.track("load_wide")

    return c
