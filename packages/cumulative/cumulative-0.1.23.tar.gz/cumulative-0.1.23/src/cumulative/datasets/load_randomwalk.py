import numpy as np
import pandas as pd

from cumulative import Cumulative


def load_randomwalk(n=20, m=10) -> Cumulative:

    x = np.linspace(0, 1, m)
    rows = []
    for _ in range(n):
        rows.append({"base.x": x, "base.y": np.random.rand(m)})
    return Cumulative(pd.DataFrame(rows))
