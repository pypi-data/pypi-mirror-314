import pandas as pd

from cumulative.transforms.transform import Transform
from cumulative.utils.frames import columns_with_prefix, drop_prefix


class Copy(Transform):
    def apply(self, src: str) -> pd.DataFrame:
        """
        Copy columns with `src` prefix (destination handled in transforms.py)
        """
        cols = columns_with_prefix(self.c.df, src)
        df = self.c.df[cols].copy()
        df.columns = drop_prefix(src, cols)
        return df
