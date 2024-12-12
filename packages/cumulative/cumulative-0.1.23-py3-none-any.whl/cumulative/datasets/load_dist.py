import numpy as np
import pandas as pd
from scipy.stats import rv_continuous

from cumulative import Cumulative
from cumulative.opts import options
from cumulative.utils.lineage import get_kwargs


class ExceptionInvalidKind(Exception):
    pass


def dist_record_cdf(dist: rv_continuous, num: int, dst: str) -> dict:
    """
    Generate a new record representing the `dist` distribution CDF
    with `num` points and `dst` key prefix.
    """

    x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), num)
    y = dist.cdf(x)
    return {f"{dst}.x": x, f"{dst}.y": y}


def dist_record_pdf(dist: rv_continuous, num: int, dst: str) -> dict:
    """
    Generate a new record representing the `dist` distribution PDF
    with `num` points and `dst` key prefix.
    """

    x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), num)
    y = dist.pdf(x)
    return {f"{dst}.x": x, f"{dst}.y": y}


def dist_record_rvs(dist: rv_continuous, num: int, dst: str) -> dict:
    """
    Generate a new record representing the `dist` distribution
    random samples with `num` points and `dst` key prefix.
    Points are sorted by ascending order.
    """

    x = np.linspace(0, 1, num)
    y = np.sort(dist.rvs(size=num))
    return {f"{dst}.x": x, f"{dst}.y": y}


def load_dist(dists: list[rv_continuous], kind: str = "cdf", num: int = 100, dst: str = None) -> Cumulative:
    """
    Load a synthetic dataset representing `dists` curves, with CDF (kind="cdf") or random samples
    (kind="rvs"), each with `num` points, with prefix `dst`.
    """

    dst = options().get("transforms.dst", prefer=dst)

    records = []
    if kind == "cdf":
        for dist in dists:
            records.append(dist_record_cdf(dist, num, dst))
    elif kind == "rvs":
        for dist in dists:
            records.append(dist_record_rvs(dist, num, dst))
    elif kind == "pdf":
        for dist in dists:
            records.append(dist_record_pdf(dist, num, dst))
    else:
        raise ExceptionInvalidKind(f"No valid kind: '{kind}'")

    df = pd.DataFrame(records)
    c = Cumulative(df)

    c.lineage.track("load_dist", dst, get_kwargs())

    return c
