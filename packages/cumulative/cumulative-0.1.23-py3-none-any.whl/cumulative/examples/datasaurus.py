from textwrap import wrap

import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
from mltraq.opts import options as mltraq_options

from cumulative.animation import Animation
from cumulative.cumulative import Cumulative
from cumulative.datasets.load_datasaurus import load_datasaurus
from cumulative.opts import options
from cumulative.utils.aggregates import get_minmax


def animate(c: Cumulative):
    """
    Animate the Datasaurus dataset, transitioning between different samples.
    """

    a = Animation()
    limits = get_minmax(c, expand=0.01)

    n = 13
    m = 10
    steps = list(range(0, n))
    for i in steps:
        for j in range(m + 1):

            def func(i, j):
                with a.plot_ctx(
                    spines_bottomleft=False,
                    mpl_rc={"font.family": "monospace", "font.size": 20},
                    mpl_style="fast",
                    facecolor="lightgray",
                    show_axes=False,
                    **limits,
                ) as ax:

                    text = "\n".join(
                        wrap(
                            "The Datasaurus dozen consists of thirteen datasets that share almost identical"
                            " descriptive statistics up to two decimal places, yet display strikingly different"
                            " distributions and visual appearances when graphed.",
                            width=20,
                        )
                    )
                    ax.text(
                        0,
                        1,
                        text,
                        horizontalalignment="left",  # center
                        verticalalignment="top",
                        transform=ax.transAxes,
                        color="dimgray",
                    )

                    p_bbox = FancyBboxPatch(
                        (0, 0),
                        1,
                        1,
                        boxstyle="round,pad=.01",
                        ec="black",
                        fc="white",
                        clip_on=False,
                        lw=1,
                        mutation_aspect=1,
                        transform=ax.transAxes,
                    )
                    ax.add_patch(p_bbox)
                    ax.patch = p_bbox

                    row0 = c.df.iloc[i]
                    row1 = c.df.iloc[(i + 1) % (n)]

                    def morph(a, b, pct):
                        return a * (1 - pct) + b * pct

                    x = morph(row0["base.x"], row1["base.x"], pct=j / m)
                    y = morph(row0["base.y"], row1["base.y"], pct=j / m)
                    pd.Series(y, index=x).plot(ax=ax, style=".", ms=15, color="black")

                    ax.text(
                        0.65,
                        0.14,
                        f"{row1['base.name'].replace('_', '-')}\nX mean: {np.mean(x):.4f}\nY mean: {np.mean(y):.4f}",
                        horizontalalignment="left",  # center
                        verticalalignment="top",
                        transform=ax.transAxes,
                        color="black",
                        bbox={"facecolor": "white", "edgecolor": "black", "boxstyle": "round,pad=.3"},
                    )

                    return ax

            a.add_frame_func(func, i, j)

    a.render()
    return a


def datasaurus():
    with options().ctx({"plot.ctx.default.figsize": (8, 8), "tqdm.disable": True}), mltraq_options().ctx(
        {"tqdm.disable": False, "execution.n_jobs": 1}
    ):
        c = load_datasaurus()
        a = animate(c)
        a.show(fps=12)
        return a
