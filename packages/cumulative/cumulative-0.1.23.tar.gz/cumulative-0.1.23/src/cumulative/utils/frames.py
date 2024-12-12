import pandas as pd
from mltraq.utils.exceptions import ExceptionWithMessage


class NoMatchingColumns(ExceptionWithMessage):
    pass


def columns_with_prefix(df: pd.DataFrame, prefix: str, errors: str = "ignore") -> list[str]:
    """
    Return list of columns in `df` dataframe with `prefix`. If no matches and errors == "raise",
    raise NoMatchingColumns exception.
    """

    cols = [col for col in df.columns if col.startswith(f"{prefix}.") or col == prefix]
    if errors == "raise" and len(cols) == 0:
        raise NoMatchingColumns(f"No columns with prefix {prefix}")
    return cols


def drop_prefix(src, cols: list[str]) -> list[str]:
    return [col.removeprefix(f"{src}.") for col in cols]


def rows_with_prefix(s: pd.Series, prefix: str, errors="ignore") -> list[str]:
    """
    Return list of index values in `s` series with `prefix`. If no matches and errors == "raise",
    raise NoMatchingColumns exception.
    """

    cols = [col for col in s.index if col.startswith(f"{prefix}.") or col == prefix]
    if errors == "raise" and len(cols) == 0:
        raise NoMatchingColumns(f"No columns with prefix {prefix}")
    return cols


def drop_cols_with_prefix(df: pd.DataFrame, prefix: str, errors="ignore") -> pd.DataFrame:
    """
    Drop columns with `prefix` from `df` dataframe and return it.
    If no matches and errors == "raise", NoMatchingColumns is raised.
    """
    cols = columns_with_prefix(df, prefix, errors=errors)
    return df.drop(columns=cols)
