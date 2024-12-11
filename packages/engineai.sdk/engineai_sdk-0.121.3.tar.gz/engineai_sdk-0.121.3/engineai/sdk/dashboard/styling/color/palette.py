"""Color palette."""

import enum
from typing import Any
from typing import Optional
from typing import Type
from typing import Union


class PaletteTypes(enum.Enum):
    """Selection of color palettes.

    Selection of different types of color palettes available.
    """

    QUALITATIVE = "QUALITATIVE"
    SEQUENTIAL = "SEQUENTIAL"


class Palette(enum.Enum):
    """Predefined color palettes.

    Collection of predefined color palettes for various purposes.
    """

    # qualitative
    MINT_GREEN = "#57DBD8"
    SUNSET_ORANGE = "#F79F5F"
    BUBBLEGUM_PINK = "#BA5479"
    GRASS_GREEN = "#68B056"
    LAVENDER_PURPLE = "#9A77FF"
    ALMOND_BROWN = "#CE7737"
    SKY_BLUE = "#5BAAF2"
    CHILI_RED = "#DE4A4A"

    # sequential
    FOREST_GREEN = "#166563"
    PEACOCK_GREEN = "#1D8684"
    LAGOON_GREEN = "#27B4B1"
    AQUA_GREEN = "#A3EBEA"
    FROST_GREEN = "#CDF4F4"

    # diverging
    RUBI_RED = "#C83C3C"
    SALMON_RED = "#EF8F8F"
    COCONUT_GREY = "#F1F4F4"
    BABY_BLUE = "#85C9FA"
    SEA_BLUE = "#338CCC"
    CEMENT_GREY = "#899F9F"
    COAL_GREY = "#2C3535"
    CROW_GREY = "#222A2A"
    SEAL_GREY = "#657B7B"

    # diverging risk
    OCEAN_BLUE = "#2574AD"
    TIGER_ORANGE = "#DE653F"
    PARADISE_GREEN = "#39C6C3"
    RIVER_BLUE = "#68B7D9"

    ASHES_GREY = "#354141"
    RHINO_GREY = "#ABBABA"

    # concept colours (dsi, price, etc)
    ENGINEAI_BLUE = "#1A6A7A"
    TROPICAL_BLUE = "#2CADB5"
    JAVA = "#248F9A"
    MEDIUM_TURQUOISE = "#5CC6CA"
    FUCHSIA_PINK = "#DB57BE"
    BANANA_YELLOW = "#F5D789"

    # extra colors
    JELLYFISH_GREEN = "#5AC4B6"
    FROG_GREEN = "#7ED0B9"
    SPRING_GREEN = "#A2DBBD"
    TEA_GREEN = "#C6E7C0"
    LEMON_YELLOW = "#FAF7C5"
    GOLD_5 = "#f1a649"
    PURPLE_7 = "#782080"
    TEAL_5 = "#54baa0"
    MAGENTA_7 = "#b92051"
    BLUE_3 = "#aab5df"
    BLUE_8 = "#1d3baa"
    PURPLE_4 = "#b280b6"
    ORANGE_7 = "#c94100"
    OCEAN_4 = "#6dacbc"
    PURPLE_9 = "#501555"

    TRAFFIC_RED = "#B54853"
    TRAFFIC_YELLOW = "#F0D582"
    TRAFFIC_GREEN = "#4C8056"

    LIGHTER_GREY = "#EEEEEE"

    # all positive sequential
    BLUE_POSITIVE_0 = "#D5E8F6"
    BLUE_POSITIVE_1 = "#96C6E9"
    BLUE_POSITIVE_2 = "#6CAFE0"
    BLUE_POSITIVE_3 = "#2D8DD2"
    BLUE_POSITIVE_4 = "#2574AD"  # noqa

    # all negative sequential
    RED_NEGATIVE_0 = "#F3D7D7"
    RED_NEGATIVE_1 = "#E8B0B0"
    RED_NEGATIVE_2 = "#DD8888"
    RED_NEGATIVE_3 = "#D26060"
    RED_NEGATIVE_4 = "#C83C3C"  # noqa

    @property
    def color(self) -> str:
        """Returns color without transparency.

        Returns:
            str: hex color
        """
        return f"{self.value}ff"


class QualitativePalette(enum.Enum):
    """Qualitative Palette."""

    MINT_GREEN = Palette.MINT_GREEN.value
    SUNSET_ORANGE = Palette.SUNSET_ORANGE.value
    BUBBLEGUM_PINK = Palette.BUBBLEGUM_PINK.value
    GRASS_GREEN = Palette.GRASS_GREEN.value
    LAVENDER_PURPLE = Palette.LAVENDER_PURPLE.value
    ALMOND_BROWN = Palette.ALMOND_BROWN.value
    SKY_BLUE = Palette.SKY_BLUE.value
    CHILI_RED = Palette.CHILI_RED.value


class SequentialPaletteTwoSeries(enum.Enum):
    """Sequential Palette for charts with two series."""

    LAGOON_GREEN = Palette.LAGOON_GREEN.value
    FROST_GREEN = Palette.FROST_GREEN.value


class SequentialPaletteThreeSeries(enum.Enum):
    """Sequential Palette for charts with three series."""

    PEACOCK_GREEN = Palette.PEACOCK_GREEN.value
    MINT_GREEN = Palette.MINT_GREEN.value
    FROST_GREEN = Palette.FROST_GREEN.value


class SequentialPalette(enum.Enum):
    """Sequential Palette."""

    FOREST_GREEN = Palette.FOREST_GREEN.value
    PEACOCK_GREEN = Palette.PEACOCK_GREEN.value
    LAGOON_GREEN = Palette.LAGOON_GREEN.value
    MINT_GREEN = Palette.MINT_GREEN.value
    AQUA_GREEN = Palette.AQUA_GREEN.value
    FROST_GREEN = Palette.FROST_GREEN.value


class PercentageAllPositiveSequentialPalette(enum.Enum):
    """All Positive Sequential Palette."""

    POSITIVE_0 = Palette.BLUE_POSITIVE_0.value
    POSITIVE_1 = Palette.BLUE_POSITIVE_1.value
    POSITIVE_2 = Palette.BLUE_POSITIVE_2.value
    POSITIVE_3 = Palette.BLUE_POSITIVE_3.value
    POSITIVE_4 = Palette.BLUE_POSITIVE_4.value


class PercentageAllNegativeSequentialPalette(enum.Enum):
    """All Negative Sequential Palette."""

    NEGATIVE_0 = Palette.RED_NEGATIVE_0.value
    NEGATIVE_1 = Palette.RED_NEGATIVE_1.value
    NEGATIVE_2 = Palette.RED_NEGATIVE_2.value
    NEGATIVE_3 = Palette.RED_NEGATIVE_3.value
    NEGATIVE_4 = Palette.RED_NEGATIVE_4.value


def qualitative_palette(*, index: int) -> Palette:
    """Returns color of qualitative palette given index.

    Args:
        index: index of qualitative palette (e.g. index of series of a
            timeseries chart)

    Returns:
        Palette: returns corresponding color of qualitative palette
    """
    colors = list(QualitativePalette.__members__.values())

    return Palette(colors[index % len(colors)].value)


SequentialPaletteType = Union[
    Type[SequentialPalette],
    Type[SequentialPaletteTwoSeries],
    Type[SequentialPaletteThreeSeries],
    Type[PercentageAllPositiveSequentialPalette],
    Type[PercentageAllNegativeSequentialPalette],
]


def sequential_palette(
    *,
    index: int,
    n_series: Optional[int] = None,
    palette: SequentialPaletteType = SequentialPalette,
) -> Palette:
    """Returns color of sequential palette given index.

    Args:
        index: index of sequential palette (e.g. index of series of a
            timeseries chart)
        n_series: total number of series used for sequential palette.
            Determines sub-versions of sequential palette to improve contrast.
            Defaults to None, i.e. uses entire palette.
        palette: enum of sequential palettes to use.

    Returns:
        Palette: returns corresponding color of sequential palette
    """
    colors: Any = list(palette.__members__.values())
    if n_series is not None:
        if n_series <= 2:
            palette = SequentialPaletteTwoSeries
        elif n_series == 3:
            palette = SequentialPaletteThreeSeries

        colors = list(palette.__members__.values())
        if n_series in [4, 5]:
            colors = colors[-n_series:]  # select last n_series colors

    return Palette(colors[index % len(colors)].value)
