import logging
from contextlib import _GeneratorContextManager, contextmanager
from typing import Any, Dict, Optional

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from cumulative.opts import options

log = logging.getLogger(__name__)


def default_subplots() -> tuple[Figure, Axes]:
    """
    Create subplots with a given figsize config via options.
    """
    fig, ax = plt.subplots(figsize=options().get("plot.ctx.default.figsize"))
    return fig, ax


@contextmanager
def plot_notemplate_ctx(  # noqa: C901
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    legend: Optional[Any] = None,
    interactive_mode: Optional[bool] = None,
    animation_mode: Optional[bool] = None,
    backend: Optional[str] = None,
    title: Optional[str] = None,
    facecolor: Optional[str] = None,
    facecolor_fig: Optional[str] = None,
    x_min: Optional[float] = None,
    x_max: Optional[float] = None,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
    x_lim: Optional[Dict] = None,
    y_lim: Optional[Dict] = None,
    spines_bottomleft: bool = False,
    x_minor_locator: Optional[float] = None,
    x_major_locator: Optional[float] = None,
    y_minor_locator: Optional[float] = None,
    y_major_locator: Optional[float] = None,
    y_grid: bool = False,
    hatches: bool = False,
    ax: Optional[Any] = None,
    figsize: Optional[tuple[int, int]] = None,
    show_axes: bool = True,
    show: bool = True,
    savefig_svg: Optional[str] = None,
    close: bool = True,
    mpl_rc: Optional[str] = None,
    mpl_style: str = "default",
):
    """
    Prepare a matplotlib plot (single sub-plot):

    `x_label`: X label
    `y_label`: Y label
    `legend`: Dictionary passed to ax.legend(...)
    `title`: Title of the plot
    `interactive_mode`: set plt.ioff() or plt.ion()
    `animation_mode`: if True, sets `interactive_mode` and `show` off
    `backend`: Backend to use
    `facecolor`: Background color of axis area
    `facecolor_fig`: Background color of figure area
    `yerr`: If true, report Y error bars
    `x_min`: X left limit
    `x_max`: X right limit
    `y_min`: Y bottom limit
    `y_max`: Y top limit
    `x_lim`: X limits, passed to ax.set_xlim(...)
    `y_lim`: Y limits, passed to ax.set_ylim(...)
    `spines_bottomleft`: Show only left,bottom spines
    `x_minor_locator`: X Minor locator
    `x_major_locator`: X Major locator
    `y_minor_locator`: Y Minor locator
    `y_major_locator`: Y Major locator
    `y_logscale`: If true, set logscale for Y
    `y_grid`: If true, show grid on Y
    `hatches`: Show hatches on bars
    `ax`: If not None, use it as axis object to draw on
    `fixsize`: size (x,y) of the subplot
    `show`: If true, call plt.show()
    `show_axes`: If false, empty white canvas without axes
    `savefig_svg`: Save figure to pathname in SVG format
    `close`: If true, close figure as last step
    `mpl_rc`': matplotlib rc options
    `mpl_style`: matplotlib style options
    """

    rc = options().get("matplotlib.rc", prefer=mpl_rc, otherwise={})
    style = options().get("matplotlib.style", prefer=mpl_style, otherwise={})

    current_backend = mpl.get_backend()
    current_interactive_mode = plt.isinteractive()

    if savefig_svg:
        # If saving figure to file, don't display it (we cannot render to both.)
        show = False

    if backend:
        plt.switch_backend(backend)

    if animation_mode:
        interactive_mode = False
        show = False

    if interactive_mode is not None:
        if interactive_mode is True:
            plt.ion()
        else:
            plt.ioff()

    with plt.rc_context(rc), plt.style.context(style):
        if ax is None:
            # Note: You can retrieve the figure with ax.get_figure().
            figsize = options().get("plot.ctx.default.figsize", prefer=figsize)
            fig, ax = plt.subplots(facecolor=facecolor_fig, figsize=figsize)

        try:
            yield ax
        finally:
            if facecolor:
                ax.set_facecolor(facecolor)

            if spines_bottomleft:
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)

            if not show_axes:
                ax.set_axis_off()

            if x_minor_locator:
                ax.yaxis.set_minor_locator(mtick.MultipleLocator(x_minor_locator))
            if x_major_locator:
                ax.yaxis.set_major_locator(mtick.MultipleLocator(x_major_locator))
            if y_minor_locator:
                ax.yaxis.set_minor_locator(mtick.MultipleLocator(y_minor_locator))
            if y_major_locator:
                ax.yaxis.set_major_locator(mtick.MultipleLocator(y_major_locator))

            if x_label is not None:
                ax.set_xlabel(x_label)
            if y_label is not None:
                ax.set_ylabel(y_label)

            # Ensure no rotated labels on X axis
            ax.tick_params(axis="x", labelrotation=0)

            if hatches:
                hatches = ("./O\o*" * len(ax.patches))[: len(ax.patches)]
                for idx, bar in enumerate(ax.patches):
                    bar.set_hatch(hatches[idx])

            # set X and Y limits
            x_lim = {} if not x_lim else x_lim
            y_lim = {} if not y_lim else y_lim
            if x_min is not None:
                x_lim["left"] = x_min
            if x_max is not None:
                x_lim["right"] = x_max
            if y_min is not None:
                y_lim["bottom"] = y_min
            if y_max is not None:
                y_lim["top"] = y_max
            if x_lim is not None:
                ax.set_xlim(**x_lim)
            if y_lim:
                ax.set_ylim(**y_lim)

            if y_grid:
                ax.grid(axis="y", which="major")

            if title is not None:
                ax.set_title(title, fontsize=plt.rcParams["font.size"] * 1)

            if legend:
                if isinstance(legend, dict):
                    ax.legend(**legend)
                else:
                    ax.legend()

            if show:
                plt.show()

            if backend:
                plt.switch_backend(current_backend)

            if interactive_mode is not None:
                if current_interactive_mode is True:
                    plt.ion()
                else:
                    plt.ioff()

            if savefig_svg is not None:
                plt.savefig(savefig_svg, format="svg", bbox_inches="tight")

            if close:
                plt.close(fig)


def plot_ctx(template_name: Optional[str] = None, **params) -> _GeneratorContextManager:
    """
    Return a context manager generator with options pulled
    from a template name `template_name`, and custom ones via `params`.
    """
    if not template_name:
        template_name = "plot.ctx.default"
    params = options().get(template_name) | params
    return plot_notemplate_ctx(**params)


class Plot:
    """
    This class provides an interface to a curated set of visualization routines.
    """

    def __init__(self, c):
        """
        Initializes the plotting interface for the `c` Cumulative instance.
        """
        self.c = c

    def xrays(
        self,
        src: str | None = None,
        ax: mpl.axes.Axes | None = None,
        alpha: float = 1,
        ms: float = 1,
        lw: float = 1,
        k: int = 20,
        style: str = "-",
        color=None,
    ):
        """
        Interpolate series on `k` points and render them as monochrome points/curves.
        """

        src = options().get("transforms.src", prefer=src)
        tmp = options().get("transforms.tmp") + ".plot"

        with options().ctx({"transforms.src": tmp, "transforms.dst": tmp}):
            self.c.copy(src=src)
            self.c.interpolate(method="pchipp", k=k, num=k)
            self.c.plot.draw(ax=ax, alpha=alpha, ms=ms, lw=lw, style=style, color=color)
            self.c.drop()
            return self

    def draw(
        self,
        src: str | None = None,
        ax: mpl.axes.Axes | None = None,
        style: str = ".",
        ms: float = 2,
        lw: float = 1,
        score: str | None = None,
        alpha: str | None = 0.5,
        only_changes: bool = False,
        color=None,
        score_legend=None,
        colormap=None,
    ):
        """
        Basic visualization of a collection of series.
        """

        if not ax:
            _, ax = default_subplots()
            force_show = True
        else:
            force_show = False

        src = options().get("transforms.src", prefer=src)

        color = options().get("plot.color", prefer=color)
        cmap = mpl.colormaps[options().get("plot.colormap", prefer=colormap)]

        for _, row in self.c.df.iterrows():
            row_color = cmap(row[score]) if isinstance(score, str) else color
            row_alpha = row[alpha] if isinstance(alpha, str) else alpha

            if only_changes:
                # If activated, only the first occurrence of a repeated value is retained
                # and the subsequent ones are set to nan (lossless compression, provided
                # there are no missing values in the original series.)
                a = row[f"{src}.y"].copy()
                a = np.where(np.insert(np.diff(a), 0, 1) != 0, a, np.nan)
            else:
                a = row[f"{src}.y"]

            pd.Series(a, index=row[f"{src}.x"]).plot(
                style=style,
                lw=lw,
                ms=ms,
                color=row_color,
                alpha=row_alpha,
                ax=ax,
            )

        if score_legend is not None:

            # We can show the legend only if there's a score
            assert isinstance(score, str)

            # Sort in ascending order fo score
            df = self.c.df.sort_values(by=score)

            # take 16 equidistant percentiles as representatives,
            # covering the whole distribution of scores.
            df = df.iloc[np.linspace(len(df) - 1, 0, 16, dtype=int)]

            handles = []
            for _, row in df.iterrows():
                patch = mpatches.Patch(color=cmap(row[score]), label=row[score_legend["label"]])
                handles.append(patch)

            ax.legend(
                handles=handles, loc="center left", bbox_to_anchor=(1, 0.5), title=score_legend["title"], frameon=False
            )

        if force_show:
            # If the axis is the default one, we force the rendering of the plot
            # before returning (otherwise, it remains in the queue of plots to display.)
            plt.show()

        return self

    def fingerprint(
        self, src: str | None = None, ax: mpl.axes.Axes | None = None, score: str = "base.z", style="-", alpha=0.5
    ):
        """
        Sample and interpolate series on max 100 series, 100 points each, and use the ".z" suffix to select the
        color from the default colormap. This visualization is robust to large datasets, as it samples and
        simplifies the curves.
        """

        src = options().get("transforms.src", prefer=src)
        tmp = options().get("transforms.tmp") + ".plot"

        with options().ctx({"transforms.src": tmp, "transforms.dst": tmp}):
            # Copy from src to tmp, and then work only on tmp (the default src/dst)
            self.c.copy(src=src)
            self.c.sample(m=100)
            self.c.interpolate(method="pchipp", k=100, num=100)
            # Transform .interpolate cleans the tmp prefix, this is why we must create the score column afterwards.
            self.c.score(src=score, dst=f"{tmp}.score", method="value")
            # The highest value ir rendered last, increasing odds it is visible.
            self.c.sort(by=f"{tmp}.score.value")

            self.draw(src=src, ax=ax, style=style, ms=1, alpha=alpha, score=f"{tmp}.score.value", only_changes=True)
            # Transform .drop removes all columns with tmp prefix
            self.c.drop()
            return self

    def ridges(
        self, src: str | None = None, ax: mpl.axes.Axes | None = None, score: str = "base.z", style="-", alpha=0.5
    ):

        if not ax:
            _, ax = default_subplots()
            force_show = True
        else:
            force_show = False

        src = options().get("transforms.src", prefer=src)
        tmp = options().get("transforms.tmp") + ".plot"

        with options().ctx({"transforms.src": tmp, "transforms.dst": tmp}):
            # Copy from src to tmp, and then work only on tmp (the default src/dst)
            self.c.copy(src=src)
            self.c.df[f"{tmp}.name"] = np.arange(1, len(self.c.df) + 1)

            def update_y(row):
                row["y"] = row["y"] ** 3
                row["y"] -= row["y"].min()
                row["y"] /= row["y"].max() * 0.2
                row["y"] += row["name"]
                return row

            self.c.row_apply(func=update_y)

            for _, row in self.c.df[::-1].iterrows():
                ax.fill_between(row[f"{tmp}.x"], row[f"{tmp}.y"], color="white", alpha=1, edgecolor="black")

        if force_show:
            # If the axis is the default one, we force the rendering of the plot
            # before returning (otherwise, it remains in the queue of plots to display.)
            plt.show()
