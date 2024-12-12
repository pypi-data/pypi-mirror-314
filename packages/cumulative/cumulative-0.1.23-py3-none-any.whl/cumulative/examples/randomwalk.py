import matplotlib.ticker as ticker
from mltraq.opts import options as mltraq_options

from cumulative.animation import Animation
from cumulative.cumulative import Cumulative
from cumulative.datasets.load_randomwalk import load_randomwalk
from cumulative.opts import options


def animate(c: Cumulative):
    c.scale(kind="xy")
    c.interpolate(dst="interp", method="pchipp", k=5, num=100)

    a = Animation()
    n = 20
    for direction in [0, 1]:
        steps = list(range(0, n + 1))
        if direction == 1:
            steps = reversed(steps)
        for i in steps:

            def func(i):
                with a.plot_ctx(spines_bottomleft=False, x_min=0, x_max=1, y_min=0, y_max=1) as ax:
                    ax.xaxis.set_major_locator(ticker.NullLocator())
                    ax.yaxis.set_major_locator(ticker.NullLocator())
                    ax.xaxis.label.set_visible(False)
                    ax.yaxis.label.set_visible(False)

                    c2 = c.dup()
                    c2.frame_apply(func=lambda df: df[: int(len(df) * i / n) + 1])
                    c2.plot.draw(src="interp", ax=ax, style="-", lw=(1 + i / n) ** 5, color="black", alpha=0.5)
                    return ax

            a.add_frame_func(func, i)
    return a


def randomwalk():
    """
    Animate a dataset of random walks.
    """

    with options().ctx({"plot.ctx.default.figsize": (5, 5), "tqdm.disable": True}), mltraq_options().ctx(
        {"tqdm.disable": False, "execution.n_jobs": 1}
    ):
        c = load_randomwalk(m=5, n=200)
        a = animate(c)
        a.render(n_jobs=1)
        a.show()
        return a
