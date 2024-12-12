from contextlib import _GeneratorContextManager
from functools import partial
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Optional

from IPython.display import HTML, Image, display
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mltraq.job import Job
from mltraq.opts import options as mltraq_options
from PIL import Image as PIL_Image
from tqdm.auto import tqdm

from cumulative.opts import options
from cumulative.plotting import plot_ctx


def fig_to_image(fig: Figure) -> bytes:
    """
    Given a figure, return it as an image in PNG format, with
    tight layout and no padding.
    """
    with BytesIO() as buf:
        fig.tight_layout(pad=0)
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        return buf.getvalue()


def ax_func_to_figure(ax_func: callable) -> bytes:
    """
    Given a function that returns a matplotlib axes,
    returns it as a PNG image (bytes).
    """
    return fig_to_image(ax_func().get_figure())


class Animation:
    """
    Helper class that simplifies the creation of animations.
    The generation of frames is parallelized by default, for
    frames passed by .add_frame_func(...).
    """

    def __init__(self, figsize: Optional[tuple[int, int]] = None):
        self.frames = []
        self.frame_funcs = []
        self.figsize = options().get("plot.ctx.default.figsize", prefer=figsize)

    def plot_ctx(self, **params) -> _GeneratorContextManager:
        """
        Return a context manager generator for the plot context, setting
        some options to their correct values for animations.
        """
        params = params | {"figsize": self.figsize, "animation_mode": True}

        return plot_ctx(**params)

    def clear(self):
        """
        Clear all animation frames.
        """

        self.frames = []
        self.frame_funcs = []

    def add_frame(self, ax: Axes):
        """
        Add `ax` as a new frame of the animation.
        """
        frame = fig_to_image(ax.get_figure())
        self.frames.append(frame)

    def add_frame_func(self, func, *args, **kwargs):
        """
        Add a frame of the animation as a function that returns a matplotlib.axes.Axes object.
        The function is not blocking, and its evaluation might be parallelized in .render().
        """
        self.frame_funcs.append(partial(func, *args, **kwargs))

    def render(self, n_jobs: Optional[int] = None):
        """
        Render frames of animation and store them. Function frames are generated
        in parallel by default. You can control the degree of parallelization with `n_jobs`,
        passed to joblib.
        """

        if self.frame_funcs:
            img_funcs = [partial(ax_func_to_figure, ax_func) for ax_func in self.frame_funcs]

            n_jobs = mltraq_options().get("execution.n_jobs", prefer=n_jobs)
            with mltraq_options().ctx({"execution.n_jobs": n_jobs, "tqdm.desc": "Rendering frames"}):
                self.frames += Job(img_funcs).execute()

        artists = []

        with plot_ctx(
            animation_mode=True,
            close=False,  # Not closing to execute statements in the "finally:" of the plotting context
            figsize=self.figsize,
            show_axes=False,
            mpl_rc={"animation.embed_limit": 2**128},
        ) as ax:
            ax.get_figure().subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

            for frame in tqdm(self.frames, desc="Assembling animation", **options().get("tqdm")):
                img = PIL_Image.open(BytesIO(frame))
                a = ax.imshow(img)
                artists.append([a])

        self.rendered = ArtistAnimation(fig=ax.get_figure(), artists=artists)
        plt.close(ax.get_figure())

        self.clear()
        return self

    def show(self, fps: Optional[int] = None):
        """
        Show animation as an HTML5 video with iPython.
        """

        fps = options().get("animation.fps", prefer=fps)
        self.rendered._interval = 1000.0 / fps
        display(HTML(self.rendered.to_html5_video()))

    def show_gif(self, fps: Optional[int] = None):
        """
        Show animation as an embedded GIF.
        """

        fps = options().get("animation.fps", prefer=fps)

        with NamedTemporaryFile(suffix=".gif") as f:
            self.save(f.name)
            display(Image(data=open(f.name, "rb").read(), format="gif"))

    def save(self, filename: str, fps: Optional[int] = None):
        """
        Save animation in MP4 format.
        """

        fps = options().get("animation.fps", prefer=fps)
        writer = animation.FFMpegWriter(fps=fps)
        self.rendered.save(filename, writer=writer)
        return self
