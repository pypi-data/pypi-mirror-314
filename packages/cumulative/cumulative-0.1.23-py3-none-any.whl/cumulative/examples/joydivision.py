import numpy as np

from cumulative.animation import Animation
from cumulative.datasets.load_joydivision import load_joydivision
from cumulative.plotting import plot_ctx
from cumulative.utils.aggregates import get_minmax


def animate():
    c = load_joydivision()

    def update_y(row):
        row["y"] -= row["y"].min()
        row["y"] /= row["y"].max() * 0.2
        row["y"] = row["y"] + np.sin(row["x"]) / 100
        row["y"] += row["name"]
        return row

    c.row_apply(func=update_y)

    c.interpolate(method="pchip")

    c.scale(kind="x")
    c.copy(dst="orig")

    limits = get_minmax(c, expand=0.01) | {"x_min": 0.1, "x_max": 0.9}

    a = Animation(figsize=(5, 5))

    n = 20
    steps = list(range(n))
    steps = steps + list(reversed(steps))
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
                c.interpolate(method="pchipp", src="orig", dst="interp", k=8)
                np.random.seed(i)
                c2 = c.dup()
                c2.morph(src="orig", src2="interp", pct=np.sin(i / n) * (2 + i / n))
                for _, row in c2.df[::-1].iterrows():
                    ax.fill_between(row["base.x"], row["base.y"], color="#382c3c", alpha=1, edgecolor="white", lw=1)
                return ax

        a.add_frame_func(func, i)

    a.render(n_jobs=1)
    a.show()
    return a


def joydivision():
    return animate()


def image_joydivision():
    c = load_joydivision()

    def update_y(row):
        row["y"] -= row["y"].min()
        row["y"] /= row["y"].max() * 0.2
        row["y"] += row["name"]
        return row

    c.row_apply(func=update_y)
    with plot_ctx(
        figsize=(10, 10),
        mpl_rc={"font.family": "monospace", "savefig.facecolor": "#382c3c"},
        mpl_style="dark_background",
        facecolor="#382c3c",
        facecolor_fig="#382c3c",
        show_axes=False,
    ) as ax:
        for _, row in c.df[::-1].iterrows():
            ax.fill_between(row["base.x"], row["base.y"], color="#382c3c", alpha=1, edgecolor="white", lw=1)

        return ax
