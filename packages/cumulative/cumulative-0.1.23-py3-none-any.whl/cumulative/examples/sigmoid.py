import numpy as np
from mltraq.opts import options as mltraq_options

from cumulative.animation import Animation
from cumulative.cumulative import Cumulative
from cumulative.datasets.load_xy import load_xy
from cumulative.opts import options
from cumulative.transforms.row.template import normalized_tunable_sigmoid


def animate(c: Cumulative):

    a = Animation()

    steps = np.linspace(-0.99, 0.99, 20).tolist()

    for k in steps + list(reversed(steps)):

        def func(k):
            with a.plot_ctx(
                mpl_rc={"font.family": "monospace"},
            ) as ax:

                ax.text(
                    0.90,
                    0.05,
                    "k=" + f"{k:.2f}".rjust(5),
                    horizontalalignment="center",
                    verticalalignment="center",
                    transform=ax.transAxes,
                    color="black",
                )
                c.df["base.y"] = c.df["base.x"].apply(lambda x: normalized_tunable_sigmoid(x, k=k))
                c.plot.draw(style="-", lw=2, ax=ax)
                return ax

        a.add_frame_func(func, k)
    return a


def sigmoid():
    """
    Animate the normalized tunable Sigmoid function.
    """

    with options().ctx({"plot.ctx.default.figsize": (5, 5), "tqdm.disable": True}), mltraq_options().ctx(
        {"tqdm.disable": False, "execution.n_jobs": 1}
    ):
        c = load_xy(m=1000, n=1)
        a = animate(c)
        a.render(n_jobs=1)
        a.show()
        return a
