import pygame

from ..parsers.size2 import Size2

from ..parsers.color import Color
from ..parsers.coordinate import Coordinate
from ..parsers.positive_int import PositiveInt


class Bar:
    def __init__(
        self, surface, width_height: tuple, xy: tuple, anchor="center", **kwargs
    ):
        """
        Creates a bar.

        Instructions:
            - To create a bar, create an instance of this class before
            the mainloop of the game.
            - To make the bar appear, call the method 'self.draw()' in
            every loop of the game.
            - To update the fill percentage of the bar, call the
            self.update() method before drawing to the screen.

        Example (simplified):
            bar = Bar(screen, (100, 20), (100, 100))
            health = 20
            max_health = 100
            while True:
                bar.update(health, max_health)
                bar.draw()

        Arguments:
            surface
                the surface the object will be drawn onto
                Type: pygame.Surface, pygame.display.set_mode
            width_height
                specifies the width / height of the bar
                Type: tuple, list
            xy
                refers to the position of the anchor
                Type: tuple, list
            anchor
                the anchor of the object:   topleft,    midtop,    topright,
                                            midleft,    center,    midright,
                                            bottomleft, midbottom, bottomright
                Type: str
            backgroundcolor
                color of the background in rgb
                Type: None, tuple, list
            fillcolor
                color of the filling
                Type: tuple, list
            bordercolor
                color of the border
                Type: tuple, list
            borderwidth
                width of the border
                Type: int
            borderradius
                used to round the corners of the background_rect; use int for all corners or other types for individual corners
                Type: int, tuple, list
            info
                can store any kind of data; usage of dict recommended
                Type: Any
            fill_start
                from which side of the bar to start filling: left (default), right, top, bottom
                Type: str

        All custom arguments can also be used in their short form (eg. "aa" instead of "antialias").
        To see what all the short forms look like, inspect the self.ABBREVIATIONS attribute.
        """

        ABBREVIATIONS = {
            "backgroundcolor": "bgc",
            "fillcolor": "fc",
            "bordercolor": "bc",
            "borderwidth": "bw",
            "borderradius": "br",
            "info": "info",
            "fill_start": "fs",
        }

        self.__surface = surface
        self.__width_height = Size2.parse(width_height)

        self.__xy = Coordinate.parse(xy)
        self.__anchor = anchor
        assert self.__anchor in (
            "topleft",
            "midtop",
            "topright",
            "midleft",
            "center",
            "midright",
            "bottomleft",
            "midbottom",
            "bottomright",
        ), f"invalid argument for 'anchor': {self.__anchor}"

        # backgroundcolor #
        self.__backgroundcolor = kwargs.get("backgroundcolor", (0, 0, 0))
        if self.__backgroundcolor == (0, 0, 0):
            self.__backgroundcolor = kwargs.get(
                ABBREVIATIONS["backgroundcolor"], (0, 0, 0)
            )
        # assertion #
        if self.__backgroundcolor != (0, 0, 0):
            self.__backgroundcolor = Color.parse(self.__backgroundcolor)

        # fillcolor #
        self.__fillcolor = kwargs.get("fillcolor", (255, 255, 255))
        if self.__fillcolor == (255, 255, 255):
            self.__fillcolor = kwargs.get(ABBREVIATIONS["fillcolor"], (255, 255, 255))
        # assertion #
        if self.__fillcolor != (255, 255, 255):
            self.__fillcolor = Color.parse(self.__fillcolor)

        # bordercolor #
        self.__bordercolor = kwargs.get("bordercolor", (0, 0, 0))
        if self.__bordercolor == (0, 0, 0):
            self.__bordercolor = kwargs.get(ABBREVIATIONS["bordercolor"], (0, 0, 0))
        # assertion #
        if self.__bordercolor != (0, 0, 0):
            self.__bordercolor = Color.parse(self.__bordercolor)

        # borderwidth #
        self.__borderwidth = kwargs.get("borderwidth", 0)
        if self.__borderwidth == 0:
            self.__borderwidth = kwargs.get(ABBREVIATIONS["borderwidth"], 0)
        # assertion #
        if self.__borderwidth != 0:
            self.__borderwidth = PositiveInt.parse(self.__borderwidth)

        # borderradius #
        self.__borderradius = kwargs.get("borderradius", 1)
        if self.__borderradius == 1:
            self.__borderradius = kwargs.get(ABBREVIATIONS["borderradius"], 1)
        # assertion #
        if self.__borderradius != 1:
            self.__borderradius = PositiveInt.parse(self.__borderradius)

        # info #
        self.__info = kwargs.get("info", None)
        if self.__info == None:
            self.__info = kwargs.get(ABBREVIATIONS["info"], None)
        # assertion #

        # fill_start #
        self.__fill_start = kwargs.get("fill_start", "left")
        if self.__fill_start == "left":
            self.__fill_start = kwargs.get(ABBREVIATIONS["fill_start"], "left")
        # assertion #
        if self.__fill_start != "left":
            assert self.__fill_start in (
                "top",
                "right",
                "bottom",
                "left",
            ), f"invalid argument for 'fill_start': {self.__fill_start}"

        assert (
            self.__width_height[0] - 2 * self.__borderwidth >= 2
        ), "widget width is too small"
        assert (
            self.__width_height[1] - 2 * self.__borderwidth >= 2
        ), "widget height is too small"

        self.__create()

    def __create(self):
        # background
        self.__r_background = pygame.Rect(
            0, 0, self.__width_height[0], self.__width_height[1]
        )
        # foreground (for calculations)
        self.__r_foreground = pygame.Rect(
            0,
            0,
            self.__width_height[0] - 2 * self.__borderwidth,
            self.__width_height[1] - 2 * self.__borderwidth,
        )
        # filling
        self.__r_filling = pygame.Rect(
            0, 0, self.__r_foreground.width, self.__r_foreground.height
        )

        self.update_pos(self.__xy, self.__anchor)

    def update_pos(self, xy, anchor=None):
        """
        Changes the widgets position. Call this
        method before drawing to the screen.
        """
        self.__xy = Coordinate.parse(xy)
        assert anchor in (
            "topleft",
            "topright",
            "bottomleft",
            "bottomright",
            "center",
            "midtop",
            "midright",
            "midbottom",
            "midleft",
            None,
        ), f"invalid argument for 'anchor': {anchor}"
        if anchor is not None:
            self.__anchor = anchor

        self.__r_background.__setattr__(self.__anchor, self.__xy)
        self.__r_foreground.center = self.__r_background.center
        self.__update_filling_pos()

    def __update_filling_pos(self):
        self.__r_filling.__setattr__(
            "mid" + self.__fill_start,
            self.__r_foreground.__getattribute__("mid" + self.__fill_start),
        )

    def update(self, value, max_value):
        fill = min(1, max(0, value / max_value))
        if self.__fill_start in ["left", "right"]:
            if fill == 0:
                self.__r_filling.width = 0
            elif fill == 1:
                self.__r_filling.width = self.__r_foreground.width
            else:
                self.__r_filling.width = min(self.__r_foreground.width - 1, max(1, self.__r_foreground.width * fill))
        elif self.__fill_start in ["top", "bottom"]:
            self.__r_filling.height = self.__r_foreground.height * fill
        self.__update_filling_pos()

    def draw(self):
        self.draw_to(self.__surface)

    def draw_to(self, surface):
        pygame.draw.rect(
            surface, self.__backgroundcolor, self.__r_background, 0, self.__borderradius
        )
        pygame.draw.rect(
            surface, self.__fillcolor, self.__r_filling, 0, self.__borderradius
        )
        if self.__borderwidth > 0:
            pygame.draw.rect(
                surface,
                self.__bordercolor,
                self.__r_background,
                self.__borderwidth,
                self.__borderradius,
            )

    def update_colors(self, backgroundcolor=None, fillcolor=None, bordercolor=None):
        if backgroundcolor is not None:
            assert isinstance(
                self.__backgroundcolor, (tuple, list)
            ), f"invalid argument for 'backgroundcolor': {self.__backgroundcolor}"
            assert (
                len(self.__backgroundcolor) == 3
            ), f"invalid argument for 'backgroundcolor': {self.__backgroundcolor}"
            self.__backgroundcolor = backgroundcolor
        if fillcolor is not None:
            assert isinstance(
                self.__fillcolor, (tuple, list)
            ), f"invalid argument for 'fillcolor': {self.__fillcolor}"
            assert (
                len(self.__fillcolor) == 3
            ), f"invalid argument for 'fillcolor': {self.__fillcolor}"
            self.__fillcolor = fillcolor
        if bordercolor is not None:
            assert isinstance(
                self.__bordercolor, (tuple, list)
            ), f"invalid argument for 'bordercolor': {self.__bordercolor}"
            assert (
                len(self.__bordercolor) == 3
            ), f"invalid argument for 'bordercolor': {self.__bordercolor}"
            self.__bordercolor = bordercolor
