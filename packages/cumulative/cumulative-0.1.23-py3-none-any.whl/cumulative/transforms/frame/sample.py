import pandas as pd

from cumulative.transforms.transform import Transform


class Sample(Transform):
    def apply(self, src: str, n: int = None, m: int = None, frac: float = None) -> pd.DataFrame:
        """
        Sample dataset, either with a fixed number `n` of rows, or a
        percentage `frac`. If `m` is provided, up to `m` rows are considered.
        """

        if m:
            n = min(m, len(self.c.df))

        self.c.df = self.c.df.sample(frac=frac, n=n).sort_index()
