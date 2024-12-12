import re

import numpy as np
import pandas as pd

from cumulative.opts import options


def melt(
    df: pd.DataFrame,
    group: str,
    pattern: str = "^t(.*)$",
    x_dtype: type = None,
    y_dtype: type = None,
    attributes: list[str] | None = None,
) -> pd.DataFrame:
    """
    Unpivot dataframe `dt` from wide to long format. Similar to Pandas.melt, but more flexible.
    `pattern` controls which columns provide numerical values, and instructs how to extract them.
    `attributes` lists the columns to be retained as attributes of the series (not necessarily numeric).
    """

    if attributes is None:
        attributes = []

    if x_dtype is None:
        x_dtype = np.dtype("float64")

    if y_dtype is None:
        y_dtype = np.dtype("float64")

    # example: df has columns ['id', 'category', 't1', 't2', 't3', 't4', 't5']
    # extract list of pairs (col_name, matching_substring) from all columns with at least one match
    matches = [
        (cm[0], cm[1].group(1)) for cm in [(c, re.search(pattern, c, re.IGNORECASE)) for c in df.columns] if cm[1]
    ]

    def f(row: pd.Series) -> pd.Series:
        # Extract a series form a row, with arrays representing the values and the attributes.
        # Order of columns is important. eg., V[5] comes after V[4].
        C = [match[0] for match in matches]  # example: "t2"
        T = [match[1] for match in matches]  # example: 2
        V = [row[match[0]] for match in matches]  # example: 12.44
        return pd.Series(
            {"c": C, "x": T, "y": V} | {"name": row[group]} | {f"attr.{attr}": row[attr] for attr in attributes}
        )

    df = df.apply(f, axis=1).explode(["c", "x", "y"])

    df["x"] = df["x"].astype(x_dtype)
    df["y"] = df["y"].astype(y_dtype)

    # example: {'col': 't1', 'time': 1, 'value': 5, 'category: 'A'
    return df


def nest(df: pd.DataFrame, dst=None) -> pd.DataFrame:
    """
    Transform series in long format to nested format. Expected columns:
    - "name": name of the series
    - "c": value of the columns representing x
    - "x": extracted x value from "c"
    - "y": value at position "x"
    - "attr.*": attributes associated to the series (optional)
    """

    dst = options().get("transforms.dst", prefer=dst)

    attributes = [c for c in df.columns if c.startswith("attr.")]

    df = df.groupby("name").agg({"c": list, "x": list, "y": list} | {attr: "first" for attr in attributes})
    df["x"] = df["x"].apply(lambda V: np.array(V))
    df["y"] = df["y"].apply(lambda V: np.array(V))

    df = df.reset_index(names="name")
    df = df.rename(
        columns={"name": f"{dst}.name", "c": f"{dst}.c", "x": f"{dst}.x", "y": f"{dst}.y"}
        | {attr: f"{dst}.{attr}" for attr in attributes}
    )

    return df


def nest_xy(df: pd.DataFrame, name: str = "name", y: str = "y") -> pd.DataFrame:
    """
    Transform series in long format to nested format. Expected columns:
    - `name`: name of the series
    - `y`: value at a certain offset

    The X column will be deduced by the offset of Y.
    """

    df = df[[name, y]].rename(columns={name: "name", y: "base.y"})
    df["base.x"] = df.groupby("name").cumcount()
    df = df.groupby("name").agg({"base.x": list, "base.y": list}).reset_index()
    df["base.x"] = df["base.x"].apply(lambda a: np.array(a))
    df["base.y"] = df["base.y"].apply(lambda a: np.array(a))
    df = df[["name", "base.x", "base.y"]]
    return df
