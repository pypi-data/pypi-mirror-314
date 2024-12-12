from cumulative.transforms.transform import Transform


class Sort(Transform):
    def apply(self, src, by: str, ascending: bool = True) -> None:
        """
        Sort rows in data frame based on column `by`, honoring
        `ascending` option. The order of the rows is affected.
        No new columns are created.
        """
        self.c.df = self.c.df.sort_values(by=by, ascending=ascending)
