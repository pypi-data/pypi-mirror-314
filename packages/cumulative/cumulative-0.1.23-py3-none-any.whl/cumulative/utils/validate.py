import numpy as np

from cumulative.utils.warnings import warn


class ValidationWarning(UserWarning):
    pass


class Validate:
    def __init__(self, c):
        self.c = c

    def check(self, prefix: str = None, deep=True):  # noqa: C901
        """
        Verify that linked cumulative data frame doesn't countain nans or infs,
        that there are both rows and columns.
        If `deep` is True, also arrays within cells are checked.
        If issues are detected, a warning is generated, with `prefix` string.
        """

        df = self.c.df

        if prefix:
            prefix = "[" + prefix + "] "
        else:
            prefix = ""

        # Check for invalid values (nans, infs)
        count_rows = len(df)
        count_invalid_rows = df.isin([np.inf, -np.inf, np.nan]).any(axis=1).sum()
        if count_invalid_rows > 0:
            warn(
                f"{prefix}Invalid rows (nans or infs): "
                f"{count_invalid_rows} ({count_invalid_rows / count_rows * 100:.0f}%)",
                category=ValidationWarning,
                stacklevel=1,
            )

        if deep and len(df) > 0:
            # Check arrays inside cells
            count_cols = 0
            count_cells = 0
            count_invalid_cols = 0
            invalid_cols = []
            count_invalid_cells = 0
            example_idx = None
            for col in df.columns:
                if isinstance(df.iloc[0][col], np.ndarray):
                    count_cols += 1
                    invalid = 0
                    for idx, row in df.iterrows():
                        count_cells += 1
                        if not np.all(np.isfinite(row[col])):
                            invalid += 1
                            if not example_idx:
                                example_idx = idx
                    if invalid > 0:
                        count_invalid_cells += invalid
                        count_invalid_cols += 1
                        invalid_cols.append(col)

            if count_invalid_cols > 0:
                warn(
                    f"{prefix}Invalid cells (nans or infs) in {count_invalid_cols} columns {invalid_cols}: "
                    f"{count_invalid_cells} ({count_invalid_cells / count_cells * 100:.0f}%), "
                    "sample idx: {example_idx}",
                    category=ValidationWarning,
                    stacklevel=1,
                )

        # Check for duplicate column names
        if len(set(df.columns)) != len(df.columns):
            warn(f"{prefix}Duplicate column names", category=ValidationWarning, stacklevel=1)

        if len(df.columns) == 0:
            warn(f"{prefix}No columns", category=ValidationWarning, stacklevel=1)

        if len(df) == 0:
            warn(f"{prefix}No rows", category=ValidationWarning, stacklevel=1)
