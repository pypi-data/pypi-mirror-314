from matplotlib.colors import to_rgba, ListedColormap
from numpy import linspace, concatenate

from mpl_format.compound_types import Color
from mpl_format.utils.color_utils import cross_fade


class ColorMapGenerator(object):

    @staticmethod
    def fade_in_to_color(to_color: Color) -> ListedColormap:

        to_color = to_rgba(to_color)
        from_color = (to_color[0], to_color[1], to_color[2], 0.0)
        return ListedColormap(cross_fade(
            from_color, to_color, linspace(0, 1, 256)))

    @staticmethod
    def fade_from_white(to_color:  Color) -> ListedColormap:
        to_color = to_rgba(to_color)
        from_color = 'white'
        return ListedColormap(cross_fade(
            from_color, to_color, linspace(0, 1, 256)))

    @staticmethod
    def cross_fade(from_color: Color, to_color: Color) -> ListedColormap:
        return ListedColormap(cross_fade(
            from_color, to_color, linspace(0, 1, 256)
        ))

    @staticmethod
    def diverging_fade_in_to_colors(
        low_color: Color,
        high_color: Color
    ):
        low_color = to_rgba(low_color)
        low_color_transparent = (
            low_color[0], low_color[1], low_color[2], 0.0
        )
        low_half = cross_fade(
            low_color, low_color_transparent, linspace(0, 1, 128)
        )
        high_color = to_rgba(high_color)
        high_color_transparent = (
            high_color[0], high_color[1], high_color[2], 0.0
        )
        high_half = cross_fade(
            high_color_transparent, high_color, linspace(0, 1, 128)
        )
        return ListedColormap(concatenate([low_half, high_half]))
