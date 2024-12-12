from mltraq.utils.base_options import BaseOptions


class Options(BaseOptions):
    default_values = {
        "reproducibility": {"random_seed": 123},
        "tqdm": {"disable": True, "leave": False, "delay": 0},
        "transforms": {
            "src": "base",
            "dst": "base",
            "tmp": "temp",
            "drop": True,
        },
        "animation": {"fps": 12},
        "plot": {
            # Defaults used by collection visualizers
            "color": "black",
            "colormap": "cool",
            "ctx": {
                # Templates for mltraq.utils.plotting.plot_ctx(...) parameters
                "default": {
                    "spines_bottomleft": True,
                    "x_label": "X",
                    "y_label": "Y",
                    "figsize": (3, 3),
                    "facecolor": "white",
                },
                "whiteboard": {"show_axes": False, "figsize": (3, 3)},
            },
        },
        "warnings": {"disable": False},
        "doc": {"url": "https://elehcimd.github.io/cumulative/"},
    }


def options() -> BaseOptions:
    """
    Returns singleton object of options.
    """

    return Options.instance()
