from __future__ import annotations

import logging

import pandas as pd
from mltraq.utils.exceptions import FatalError
from tqdm.auto import tqdm

from cumulative.opts import options
from cumulative.utils.frames import drop_cols_with_prefix

log = logging.getLogger(__name__)


def process_row(func, row, **kwargs):
    return func(row, **kwargs)


class Transform:
    """
    Abstraction of transforms.
    """

    def __init__(self, c, name: str = None):
        """
        Link transform to Cumulative class and set its name.
        """

        self.c = c
        self.name = self.__class__.__name__ if not name else name

    def transform_row(self, row: pd.Series) -> pd.Series:
        """
        Transformations can be applied either on rows or columns.
        For rows, the `transform_row` method is overloaded and it
        returns a series with the new columns to add.
        """
        return pd.Series()

    def __call__(self, **kwargs):
        """
        Handles transform requests.
        """
        tqdm.pandas(desc=self.name, **options().get("tqdm"))

        # Ensure src and dst of operation is set
        kwargs["src"] = options().get("transforms.src", prefer=kwargs.pop("src", None))
        kwargs["dst"] = options().get("transforms.dst", prefer=kwargs.pop("dst", None))
        kwargs["drop"] = options().get("transforms.drop", prefer=kwargs.pop("drop", None))

        # Apply transform and obtain new columns
        kwargs_apply = kwargs.copy()
        dst = kwargs_apply.pop("dst")
        kwargs_apply.pop("drop")
        # dst, drop parameters are removed before executing .apply, as they are handled
        # transparently in this method.
        df = self.apply(**kwargs_apply)

        # Log operation
        self.c.lineage.track(self.name, dst, kwargs)

        if df is None:
            # No change (e.g., sorting)
            return self.c
        elif isinstance(df, pd.DataFrame):
            # Multiple columns added from processing entire data frame
            df.columns = [f"{kwargs['dst']}.{col}" if col != "idx" else col for col in df.columns]
        elif isinstance(df, pd.Series):
            # Multiple columns added from processing single row
            df = pd.DataFrame({kwargs["dst"]: df})
        else:
            raise FatalError("Invalid transform result; expected None, pandas.Series or pandas.DataFrame")

        if kwargs["drop"]:
            # If drop specified, clean up prefix `dst` before adding the new columns.
            # This ensures that we don't mix up results of different transforms in the same prefix.
            self.c.df = drop_cols_with_prefix(self.c.df, kwargs["dst"])

        self.c.df = pd.concat(
            [self.c.df, df],
            axis=1,
        )
        return self.c

    def apply(self, **kwargs):
        """
        Transformations can be applied either on rows or columns.
        For columns, the `apply` method is overloaded and it
        returns a data frame with the new columns to add.

        By default, it handles row transforms.
        """
        return self.c.df.progress_apply(lambda row: self.transform_row(row, **kwargs), axis=1)
