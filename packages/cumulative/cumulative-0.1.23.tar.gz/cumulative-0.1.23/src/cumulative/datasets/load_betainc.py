import itertools

import numpy as np
import pandas as pd
from scipy.special import betainc

from cumulative import Cumulative
from cumulative.opts import options
from cumulative.utils.lineage import get_kwargs


def betainc_record(a: float, b: float, num: int, dst: str) -> dict:
    """
    Generate a new record representing the betainc series with parameters `a` and `b`
    using `num` equidistant points between 0 and 1, with `dst` key prefix.
    """

    x = np.linspace(0, 1, num)
    y = betainc(a, b, x)
    return {f"{dst}.a.a": a, f"{dst}.a.b": b, f"{dst}.x": x, f"{dst}.y": y}


def load_betainc(a_min=0.1, a_max=10, b_min=0.1, b_max=10, size=10, num=100, dst=None) -> Cumulative:
    """
    Load a synthetic dataset of `size` betainc curves with a and b parameters ranging within
    intervals [`a_min`, `a_max`] and [`b_min`, `b_max`], represented by `num` points each.
    """

    a = np.linspace(a_min, a_max, size)
    b = np.linspace(b_min, b_max, size)

    dst = options().get("transforms.dst", prefer=dst)

    records = []
    for ab in itertools.product(a, b):
        record = betainc_record(ab[0], ab[1], num, dst)
        records.append(record)

    df = pd.DataFrame(records)
    c = Cumulative(df)

    c.lineage.track("load_betainc", dst, get_kwargs())

    return c
