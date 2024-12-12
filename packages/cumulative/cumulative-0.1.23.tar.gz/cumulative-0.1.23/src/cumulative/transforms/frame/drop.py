from cumulative.transforms.transform import Transform
from cumulative.utils.frames import drop_cols_with_prefix


class Drop(Transform):
    def apply(self, src: str):
        """
        Drop columns with prefix `src`
        """
        self.c.df = drop_cols_with_prefix(self.c.df, src)
