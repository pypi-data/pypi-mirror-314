import warnings

from cumulative.opts import options


def warn(*args, stacklevel=1, **kwargs):
    """
    Utility function to handle warnings.
    """
    if not options().get("warnings.disable"):
        warnings.warn(*args, stacklevel=stacklevel, **kwargs)
