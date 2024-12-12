import inspect

from cumulative.opts import options


def get_kwargs() -> dict:
    """
    Return kwargs passed to funcion calling get_kwargs().
    """

    frame = inspect.currentframe().f_back
    keys, _, _, values = inspect.getargvalues(frame)
    kwargs = {}
    for key in keys:
        if key != "self":
            kwargs[key] = values[key]
    return kwargs


class Lineage:
    """
    Handling of lineage of operations.
    """

    def __init__(self):
        self.steps = []

    def track(self, name: str, dst: str | None = None, kwargs: dict | None = None):
        """
        Track transform call `name` to `dst` with `kwargs`.
        """

        if kwargs is None:
            kwargs = {}

        kwargs = kwargs.copy()
        src = options().get("transforms.src", prefer=kwargs.pop("src", None))
        dst = options().get("transforms.dst", prefer=kwargs.pop("dst", dst))
        drop = options().get("transforms.drop", prefer=kwargs.pop("drop", None))

        self.steps.append({"name": name, "src": src, "dst": dst, "drop": drop, "kwargs": kwargs})

    def clear(self):
        """
        Clear the currently tracked history.
        """

        self.steps = []

    def explain(self, max_len: int = 40, reverse: bool = False):
        """
        Print operations applied to data frame.
        """

        steps = list(enumerate(self.steps))

        if reverse:
            steps = steps[::-1]

        for idx, transform in steps:
            name = transform["name"]

            def stringify(v, string_delim: bool = False):
                if isinstance(v, str) and string_delim:
                    v = f'"{v}"'
                elif callable(v):
                    v = f"{v.__name__}"
                v = str(v)
                if len(v) > max_len:
                    v = v[:max_len] + ".."
                return v

            d = "" if transform["drop"] else "(no drop)"

            kwargs = ", ".join([f"{k}={stringify(v,string_delim=True)}" for k, v in transform["kwargs"].items()])
            if idx > 0:
                srcdst = f"{stringify(transform['src'])} -> {stringify(transform['dst'])} {d}"
            else:
                srcdst = f"-> {stringify(transform['dst'])} {d}"

            print(f"[{idx}] {name}({kwargs}): {srcdst}")
