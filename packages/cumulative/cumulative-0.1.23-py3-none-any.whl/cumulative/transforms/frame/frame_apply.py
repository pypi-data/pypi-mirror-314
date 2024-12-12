from cumulative.transforms.transform import Transform


class FrameApply(Transform):
    def apply(self, src: str, func: callable):
        """
        Apply `func` to the frame.
        """

        self.c.df = func(self.c.df)
