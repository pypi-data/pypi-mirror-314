from typing import Optional

import numpy as np
import pandas as pd

from cumulative import Cumulative
from cumulative.transforms.row.template import normalized_tunable_sigmoid


def load_sigmoid(n=20, m=100, k=0.5, gaussian_noise: Optional[float] = None) -> Cumulative:

    df = pd.DataFrame(index=range(n))
    df["base.x"] = [np.linspace(0, 1, m) for _ in range(n)]
    df["base.y"] = df["base.x"].apply(lambda x: normalized_tunable_sigmoid(x, k=k))

    if gaussian_noise is not None:
        df["base.y"] = df["base.y"].apply(lambda y: np.diff(y, prepend=0))
        df["base.y"] = df["base.y"].apply(lambda y: y + np.abs(np.random.normal(scale=gaussian_noise, size=m)))
        df["base.y"] = df["base.y"].apply(lambda y: np.cumsum(y))

    c = Cumulative(df)

    c.scale()

    return c
