import random

import pandas as pd
from mltraq.opts import options as mltraq_options

from cumulative import Cumulative
from cumulative.animation import Animation
from cumulative.datasets.load_sigmoid import load_sigmoid
from cumulative.opts import options
from cumulative.utils.aggregates import get_minmax


def limit_random(row, m):
    new_m = random.randint(2, m)  # noqa: S311
    row["base.x"] = row["base.x"][:new_m]
    row["base.y"] = row["base.y"][:new_m]
    return row


def animate(c: Cumulative):

    c.df = c.df.apply(lambda row: limit_random(row, 10), axis=1)

    c.interpolate(method="pchip", num=100)

    a = Animation()
    limits = get_minmax(c, expand=0.01)
    n = len(c.df)
    steps = list(range(1, n + 1))
    for i in steps:

        def func(i):
            with a.plot_ctx(
                show_axes=False,
                **limits,
            ) as ax:
                c2 = Cumulative(c.df[:i])
                c2.plot.draw(ax=ax, style="-", lw=1, color="black", alpha=0.4)

                c3 = Cumulative(c2.df[-1:])
                c3.plot.draw(ax=ax, style="-", lw=4, color="white", alpha=1)
                c3.plot.draw(ax=ax, style="-", lw=2, color="red", alpha=1)
                row = c3.df.iloc[0]
                pd.Series(row["base.y"][-1:], index=row["base.x"][-1:]).plot(ax=ax, color="red", style=".", ms=10)

                return ax

        a.add_frame_func(func, i)
    return a


def sigmoid2():
    """
    Animate the IRIS dataset, with multi-effect transitions.
    The result is an animation that can be repeated with no
    point of discontinuity.
    """

    with options().ctx({"plot.ctx.default.figsize": (5, 5), "tqdm.disable": True}), mltraq_options().ctx(
        {"tqdm.disable": False, "execution.n_jobs": 1}
    ):
        c = load_sigmoid(n=100, m=10, gaussian_noise=0.1, k=-0.5)
        a = animate(c)
        a.render(n_jobs=1)
        a.show(fps=5)
        return a
