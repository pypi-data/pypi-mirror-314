from ..typing import Axes, Figure, PathCollection, Sequence

__all__ = [
    "_scatter2d",
]


def _scatter2d(
    fig: Figure,
    ax: Axes,
    x: Sequence[float],
    y: Sequence[float],
    *args,
    **kwargs,
) -> PathCollection:
    plot: PathCollection = ax.scatter(x, y, *args, **kwargs)

    return plot
