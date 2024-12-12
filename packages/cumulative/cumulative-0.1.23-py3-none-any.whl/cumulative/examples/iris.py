from mltraq.opts import options as mltraq_options
from sklearn.datasets import load_iris

from cumulative.animation import Animation
from cumulative.cumulative import Cumulative
from cumulative.datasets.load_sklearn import load_sklearn
from cumulative.opts import options
from cumulative.transforms.row.row_apply import mid_points
from cumulative.utils.aggregates import get_minmax


def animate(c: Cumulative):
    """
    Animate the dataset, with multi-effect transitions.
    The result is an animation that can be repeated with no
    point of discontinuity.
    """

    c.sample(m=200)
    c.copy(dst="seq")
    c.interpolate(method="pchip", num=100)
    c.copy(dst="interp")
    c.template(dst="template", method="horizon")
    c.template(dst="template2", method="center")
    c.score(src="seq.z", dst="score", method="value")
    c.sort(by="score.value")

    a = Animation()
    count = len(c.df)
    limits = get_minmax(c, expand=0.01)
    n = 20
    for direction in [0, 1]:
        steps = list(range(0, n + 1))
        if direction == 1:
            steps = reversed(steps)
        for i in steps:

            def func(i):
                with a.plot_ctx(
                    mpl_rc={"font.family": "monospace", "savefig.facecolor": "#382c3c"},
                    mpl_style="dark_background",
                    facecolor="#382c3c",
                    facecolor_fig="#382c3c",
                    show_axes=False,
                    **limits,
                ) as ax:
                    c2 = c.dup()
                    c2.frame_apply(func=lambda df: df[: i * int(count / n) + 1])
                    c2.morph(src="template", src2="interp", pct=i / n)
                    c2.row_apply(func=mid_points, pct=i / n, rand=1 / 10)
                    c2.plot.draw(ax=ax, style="-", lw=2, alpha=i / n, score="score.value")

                    return ax

            a.add_frame_func(func, i)

    a.render()
    return a


def iris():
    """
    Animate Iris dataset.
    """

    with options().ctx({"plot.ctx.default.figsize": (5, 5), "tqdm.disable": True}), mltraq_options().ctx(
        {"tqdm.disable": False, "execution.n_jobs": 1}
    ):
        c = load_sklearn(load_iris)
        a = animate(c)
        a.show()
        return a
