import os

import pygame

from ..parsers.color import Color
from ..parsers.coordinate import Coordinate
from ..parsers.positive_float import PositiveFloat
from ..parsers.positive_int import PositiveInt
from ..parsers.size2 import Size2
from ..parsers.size4 import Size4
from .OneClickManager import OneClickManager


class Label:

    def __init__(
        self,
        surface: pygame.Surface | None,
        text: str,
        size: int,
        xy: tuple,
        anchor: str = "center",
        **kwargs,
    ):
        """
        Creates a label.

        Instructions:
            - To create a label, create an instance of this class before
            the mainloop of the game.
            - To make the label appear, call the method 'self.draw()' in
            every loop of the game.

        Example (simplified):
            label = Label(screen, "Hello world!", 32, (100,100), "topleft")
            while True:
                label.draw()

        Arguments:
            surface
                the surface the object will be drawn onto
                Type: pygame.Surface
            text
                the text displayed on the label / button
                Type: Any
            size
                refers to the size of text in pixels
                Type: int
            xy
                refers to the position of the anchor
                Type:
                    tuple[int, int]
                    tuple[tuple[int, int], tuple[int, int]] -> performs sum of vectors (v1[0] + v2[0], v1[1] + v2[1])
                    list[...]
                    list[list[...]]
            anchor
                the anchor of the object:   topleft,    midtop,    topright,
                                            midleft,    center,    midright,
                                            bottomleft, midbottom, bottomright
                Type: str
            textcolor
                color of the text in rgb
                Type: tuple, list
            backgroundcolor
                color of the background in rgb
                Type: None, tuple, list
            antialias
                whether antialias (blurring to make text seem more realistic) should be used
                Type: bool
            font
                The font used for the text. Tries to match a font of PygameXtras first, then checks sysfonts.
                To get a list of all available PygameXtras fonts, run 'PygameXtras.list_fonts()'. To get a list
                of all sysfonts, run 'pygame.font.get_fonts()'.
                Type: str
            x_axis_addition
                adds the given amount of pixels to the left and right (-> x axis) of the text
                Type: int
            y_axis_addition
                adds the given amount of pixels to the top and bottom (-> y axis) of the text
                Type: int
            borderwidth
                width of the border
                Type: int
            bordercolor
                color of the border
                Type: tuple, list
            force_width
                forces the width of the background
                Type: int
            force_height
                forces the height of the background
                Type: int
            force_dim
                forces width and height of the background
                Type: tuple, list
            borderradius
                used to round the corners of the background_rect; use int for all corners or other types for individual corners
                Type: int, tuple, list
            text_offset
                moves the text by the given values; is inverted if binding_rect == 1
                Type: tuple, list
            image
                takes an image as background for the widget; configures the widget to use the dimensions of the image, unless specified otherwise
                Type: pygame.Surface
            info
                can store any kind of data; usage of dict recommended
                Type: Any
            text_binding
                binds the text within the background_rect
                Type: str (same as <anchor>)
            highlight
                (button only)
                makes the button shine when the mouse hovers over it; when using "True", the button shines a little brighter than
                its usual backgroundcolor; otherwise, the button shines in the given rgb color; only works when using <backgroundcolor>
                Type: True, tuple, list
            active_area
                (button only)
                makes the self.update method only work if the mouse click / hovering is also within the specified rect; useful if
                buttons are moveable but should not be clickable if they are outside a certain area
                Type: tuple, list, pygame.Rect
            bold
                makes the text appear bold (faked)
                Type: bool
            italic
                makes the text appear italic (faked)
                Type: bool
            underline
                underlines the text
                Type: bool
            one_click_manager
                (button only)
                assures that overlaying buttons can not be clicked at the same time
                Type: PygameXtras.OneClickManager
            margin
                decreases the size of the widget without affecting the position
                Type: int
            font_file
                use font from a file (path expected)
                Type: str

        All custom arguments can also be used in their short form (eg. "aa" instead of "antialias").
        To see what all the short forms look like, inspect the self.ABBREVIATIONS attribute.
        """

        self.ABBREVIATIONS = {
            "textcolor": "tc",
            "backgroundcolor": "bgc",
            "antialias": "aa",
            "font": "f",
            "x_axis_addition": "xad",
            "y_axis_addition": "yad",
            "borderwidth": "bw",
            "bordercolor": "bc",
            "force_width": "fw",
            "force_height": "fh",
            "force_dim": "fd",
            "borderradius": "br",
            "text_offset": "to",
            "image": "img",
            "info": "info",
            "text_binding": "tb",
            "highlight": "hl",
            "active_area": "aA",
            "bold": "bo",
            "italic": "it",
            "underline": "ul",
            "one_click_manager": "ocm",
            "template": "t",
            "margin": "m",
            "font_file": "ff",
        }

        # inserting template (if exists)
        template = kwargs.get("template", None)
        if template is None:
            template = kwargs.get(self.ABBREVIATIONS["template"], None)
        if template is not None:
            assert isinstance(template, dict), f"invalid argument for 'template': {template}"
            for k in template.keys():
                if not k in kwargs.keys():
                    kwargs[k] = template[k]

        self.__is_touching__ = False  # if cursor is touching the rect, only for buttons
        self.__has_hl_image__ = False

        self.surface = surface
        if self.surface != None:
            assert isinstance(
                self.surface, pygame.Surface
            ), f"invalid argument for 'surface': {self.surface}"

        self.text = str(text)

        self.size = PositiveFloat.parse(size)
        self.size = round(self.size)

        self.xy = Coordinate.parse(xy)

        self.anchor = anchor
        if "anchor" in kwargs.keys():
            self.anchor = kwargs["anchor"]

        assert self.anchor in (
            "topleft",
            "midtop",
            "topright",
            "midleft",
            "center",
            "midright",
            "bottomleft",
            "midbottom",
            "bottomright",
        ), f"invalid argument for 'anchor': {self.anchor}"

        kw = kwargs

        # textcolor
        self.textcolor = kw.get("textcolor", None)
        if self.textcolor == None:
            self.textcolor = kw.get(self.ABBREVIATIONS["textcolor"], None)
        if self.textcolor == None:
            self.textcolor = (0, 0, 0)
        # assertion
        if self.textcolor != None:
            self.textcolor = Color.parse(self.textcolor)

        # backgroundcolor
        self.backgroundcolor = kw.get("backgroundcolor", None)
        if self.backgroundcolor == None:
            self.backgroundcolor = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion
        if self.backgroundcolor != None:
            self.backgroundcolor = Color.parse(self.backgroundcolor)

        # backgroundcolor backup
        self.backgroundcolor_init = self.backgroundcolor
        # assertion completed by previous assertion

        # antialias
        self.antialias = kw.get("antialias", None)
        if self.antialias == None:
            self.antialias = kw.get(self.ABBREVIATIONS["antialias"], None)
        if self.antialias == None:
            self.antialias = True
        # assertion
        self.antialias = bool(self.antialias)

        # font
        self.font = kw.get("font", None)
        if self.font == None:
            self.font = kw.get(self.ABBREVIATIONS["font"], None)
        if self.font == None:
            self.font = "verdana"
        # assertion
        if self.font != None:
            assert isinstance(
                self.font, str
            ), f"invalid argument for 'font': {self.font}"

        # font_file
        self.font_file = kw.get("font_file", None)
        if self.font_file == None:
            self.font_file = kw.get(self.ABBREVIATIONS["font_file"], None)
        # assertion
        if self.font_file != None:
            assert isinstance(
                self.font_file, str
            ), f"invalid argument for 'font_file': {self.font_file}"

        # x_axis_addition
        self.x_axis_addition = kw.get("x_axis_addition", None)
        if self.x_axis_addition == None:
            self.x_axis_addition = kw.get(self.ABBREVIATIONS["x_axis_addition"], None)
        if self.x_axis_addition == None:
            self.x_axis_addition = 0
        # assertion
        if self.x_axis_addition != None:
            self.x_axis_addition = PositiveInt.parse(self.x_axis_addition)

        # y_axis_addition
        self.y_axis_addition = kw.get("y_axis_addition", None)
        if self.y_axis_addition == None:
            self.y_axis_addition = kw.get(self.ABBREVIATIONS["y_axis_addition"], None)
        if self.y_axis_addition == None:
            self.y_axis_addition = 0
        # assertion
        if self.y_axis_addition != None:
            self.y_axis_addition = PositiveInt.parse(self.y_axis_addition)

        # borderwidth
        self.borderwidth = kw.get("borderwidth", None)
        if self.borderwidth == None:
            self.borderwidth = kw.get(self.ABBREVIATIONS["borderwidth"], None)
        if self.borderwidth == None:
            self.borderwidth = 0
        # assertion
        if self.borderwidth != None:
            self.borderwidth = PositiveInt.parse(self.borderwidth)

        # bordercolor
        self.bordercolor = kw.get("bordercolor", None)
        if self.bordercolor == None:
            self.bordercolor = kw.get(self.ABBREVIATIONS["bordercolor"], None)
        if self.bordercolor == None:
            self.bordercolor = (0, 0, 0)
        # assertion
        if self.bordercolor != None:
            self.bordercolor = Color.parse(self.bordercolor)

        # force_width
        self.force_width = kw.get("force_width", None)
        if self.force_width == None:
            self.force_width = kw.get(self.ABBREVIATIONS["force_width"], None)
        # assertion
        if self.force_width != None:
            self.force_width = PositiveInt.parse(self.force_width)

        # force_height
        self.force_height = kw.get("force_height", None)
        if self.force_height == None:
            self.force_height = kw.get(self.ABBREVIATIONS["force_height"], None)
        # assertion
        if self.force_height != None:
            self.force_height = PositiveInt.parse(self.force_height)

        # force_dim
        force_dim = kw.get("force_dim", None)
        if force_dim == None:
            force_dim = kw.get(self.ABBREVIATIONS["force_dim"], None)
        # assertion
        if force_dim != None:
            self.force_dim = Size2.parse(force_dim)
            self.force_width = force_dim[0]
            self.force_height = force_dim[1]

        # borderradius
        self.borderradius = kw.get("borderradius", None)
        if self.borderradius == None:
            self.borderradius = kw.get(self.ABBREVIATIONS["borderradius"], None)
        if self.borderradius == None:
            self.borderradius = (1, 1, 1, 1)
        # assertion
        elif isinstance(self.borderradius, int):
            self.borderradius = PositiveInt.parse(self.borderradius)
            self.borderradius = (
                self.borderradius,
                self.borderradius,
                self.borderradius,
                self.borderradius,
            )
        elif isinstance(self.borderradius, (tuple, list)):
            self.borderradius = Size4.parse(self.borderradius)
        else:
            raise AssertionError(
                f"invalid argument for 'borderradius': {self.borderradius}"
            )

        # text_offset
        self.text_offset = kw.get("text_offset", None)
        if self.text_offset == None:
            self.text_offset = kw.get(self.ABBREVIATIONS["text_offset"], None)
        if self.text_offset == None:
            self.text_offset = (0, 0)
        # assertion
        if self.text_offset != None:
            self.text_offset = Size2.parse(self.text_offset)

        # image
        self.image = kw.get("image", None)
        if self.image == None:
            self.image = kw.get(self.ABBREVIATIONS["image"], None)
        # assertion
        if self.image != None:
            assert isinstance(
                self.image, pygame.Surface
            ), f"invalid argument for 'image': {self.image}"
            if self.force_width == None:
                self.force_width = self.image.get_width()
            if self.force_height == None:
                self.force_height = self.image.get_height()
            self.image = pygame.transform.scale(
                self.image, (self.force_width, self.force_height)
            )

        # info
        self.info = kw.get("info", None)
        if self.info == None:
            self.info = kw.get(self.ABBREVIATIONS["info"], None)
        # no assertion needed

        # text_binding
        self.text_binding = kw.get("text_binding", None)
        if self.text_binding == None:
            self.text_binding = kw.get(self.ABBREVIATIONS["text_binding"], None)
        if self.text_binding == None:
            self.text_binding = "center"
        # assertion
        if self.text_binding != None:
            assert self.text_binding in [
                "topleft",
                "midtop",
                "topright",
                "midleft",
                "center",
                "midright",
                "bottomleft",
                "midbottom",
                "bottomright",
            ]

        # highlight
        self.highlight = kw.get("highlight", None)
        if self.highlight == None:
            self.highlight = kw.get(self.ABBREVIATIONS["highlight"], None)
        # assertion
        if self.highlight != None:
            if type(self.highlight) in [tuple, list]:
                pass  # ok
            elif self.highlight == False:
                self.highlight = None  # ok
            elif self.highlight == True:
                if self.image == None:
                    assert (
                        self.backgroundcolor != None
                    ), f"'backgroundcolor' (currently: {self.backgroundcolor}) must be defined when using 'highlight' (currently: {self.highlight})"
            else:
                raise AssertionError(
                    f"invalid argument for 'highlight': {self.highlight}"
                )

            if self.image == None:
                if self.highlight == True:
                    self.highlight = (
                        min(self.backgroundcolor[0] + 50, 255),
                        min(self.backgroundcolor[1] + 50, 255),
                        min(self.backgroundcolor[2] + 50, 255),
                    )
            else:
                self.__has_hl_image__ = True
                # if the backgroundcolor is not defined, the regular image will be taken for the hl_image
                # if there is a backgroundcolor, the backgroundcolor will be included in the hl_image
                if self.backgroundcolor == None:
                    self.hl_image = self.image.copy()
                else:
                    self.hl_image = pygame.Surface(self.image.get_size())
                    self.hl_image.fill(self.backgroundcolor)
                    self.hl_image.blit(self.image, (0, 0))
                # applying the brightening effect / coloring
                if self.highlight == True:
                    self.hl_image.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
                else:
                    self.hl_image.fill(
                        self.highlight, special_flags=pygame.BLEND_RGB_MULT
                    )
                # scaling to fit the size
                self.hl_image = pygame.transform.scale(
                    self.hl_image, (self.force_width, self.force_height)
                )

        # active_area
        self.active_area = kw.get("active_area", None)
        if self.active_area == None:
            self.active_area = kw.get(self.ABBREVIATIONS["active_area"], None)
        # assertion
        if self.active_area != None:
            if isinstance(self.active_area, (tuple, list)):
                self.active_area = Size4.parse(self.active_area)
                self.active_area = pygame.Rect(self.active_area)
            elif isinstance(self.active_area, pygame.Rect):
                pass
            else:
                raise AssertionError(
                    f"invalid argument for 'active_area': {self.active_area}"
                )

        # bold
        self.bold = kw.get("bold", None)
        if self.bold == None:
            self.bold = kw.get(self.ABBREVIATIONS["bold"], None)
        if self.bold == None:
            self.bold = False
        # assertion
        self.bold = bool(self.bold)

        # italic
        self.italic = kw.get("italic", None)
        if self.italic == None:
            self.italic = kw.get(self.ABBREVIATIONS["italic"], None)
        if self.italic == None:
            self.italic = False
        # assertion
        self.italic = bool(self.italic)

        # underline
        self.underline = kw.get("underline", None)
        if self.underline == None:
            self.underline = kw.get(self.ABBREVIATIONS["underline"], None)
        if self.underline == None:
            self.underline = False
        # assertion
        self.underline = bool(self.underline)

        # one_click_manager
        self.one_click_manager = kw.get("one_click_manager", None)
        if self.one_click_manager == None:
            self.one_click_manager = kw.get(
                self.ABBREVIATIONS["one_click_manager"], None
            )
        # assertion
        if self.one_click_manager != None:
            assert isinstance(
                self.one_click_manager, OneClickManager
            ), f"invalid argument for 'one_click_manager': {self.one_click_manager}"

        # margin
        self.margin = kw.get("margin", None)
        if self.margin == None:
            self.margin = kw.get(self.ABBREVIATIONS["margin"], None)
        if self.margin == None:
            self.margin = 0
        # assertion
        if self.margin != None:
            self.margin = PositiveInt.parse(self.margin)

        self.__load_font_path()
        self.__create__()

    def __create__(self):

        font = pygame.font.Font(self.font_path, self.size)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        font.set_underline(self.underline)
        self.text_surface = font.render(str(self.text), self.antialias, self.textcolor)
        self.text_rect = self.text_surface.get_rect()

        # x y w h
        # x_axis: x, w
        # y_axis: y, h

        if self.x_axis_addition == 0:
            x = self.text_rect.x
            w = self.text_rect.width
        elif self.x_axis_addition > 0:
            x = self.text_rect.x - self.x_axis_addition
            w = self.text_rect.width + self.x_axis_addition * 2

        if self.y_axis_addition == 0:
            y = self.text_rect.y
            h = self.text_rect.height
        elif self.y_axis_addition > 0:
            y = self.text_rect.y - self.y_axis_addition
            h = self.text_rect.height + self.y_axis_addition * 2

        if self.force_width == None:
            pass
        else:
            w = self.force_width

        if self.force_height == None:
            pass
        else:
            h = self.force_height

        # creating the background rect
        self.background_rect = pygame.Rect(
            x + self.margin,
            y + self.margin,
            w - 2 * self.margin,
            h - 2 * self.margin,
        )

        # creating positioning rect
        self.positioning_rect = pygame.Rect(x, y, w, h)

        # putting everything in correct position
        self.update_pos(self.xy, self.anchor)

    def __load_font_path(self):
        if self.font_file is None:
            fonts = [
                f.removesuffix(".ttf")
                for f in os.listdir(
                    os.path.join(os.path.dirname(__file__), "..", "fonts")
                )
            ]
            if self.font.lower() in fonts:
                self.font_path = os.path.join(
                    os.path.dirname(__file__), "..", "fonts", self.font.lower() + ".ttf"
                )
            else:
                self.font_path = pygame.font.match_font(self.font)
        else:
            self.font_path = self.font_file

    def draw(self):
        """
        Draws the widget to the screen.
        """
        if self.surface is None:
            raise Exception(f"no surface given to draw to")

        if self.backgroundcolor != None:
            if self.__is_touching__ and self.image == None:
                pygame.draw.rect(
                    self.surface,
                    self.highlight,
                    self.background_rect,
                    0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3],
                )
            else:
                pygame.draw.rect(
                    self.surface,
                    self.backgroundcolor,
                    self.background_rect,
                    0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3],
                )
        if self.image != None:
            if self.__has_hl_image__ and self.__is_touching__:
                self.surface.blit(self.hl_image, self.background_rect)
            else:
                self.surface.blit(self.image, self.background_rect)

        if self.borderwidth > 0:
            pygame.draw.rect(
                self.surface,
                self.bordercolor,
                self.background_rect,
                self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3],
            )
        self.surface.blit(self.text_surface, self.text_rect)

    def draw_to(self, surface: pygame.Surface):
        """
        Draws the widget to a different surface than initially specified.
        """
        assert (
            type(surface) == pygame.Surface
        ), f"invalid argument for 'surface': {surface}"

        if self.backgroundcolor != None:
            if self.__is_touching__ and self.image == None:
                pygame.draw.rect(
                    surface,
                    self.highlight,
                    self.background_rect,
                    0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3],
                )
            else:
                pygame.draw.rect(
                    surface,
                    self.backgroundcolor,
                    self.background_rect,
                    0,
                    border_top_left_radius=self.borderradius[0],
                    border_top_right_radius=self.borderradius[1],
                    border_bottom_right_radius=self.borderradius[2],
                    border_bottom_left_radius=self.borderradius[3],
                )
        if self.image != None:
            if self.__has_hl_image__ and self.__is_touching__:
                surface.blit(self.hl_image, self.background_rect)
            else:
                surface.blit(self.image, self.background_rect)

        if self.borderwidth > 0:
            pygame.draw.rect(
                surface,
                self.bordercolor,
                self.background_rect,
                self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3],
            )
        surface.blit(self.text_surface, self.text_rect)

    def update_text(self, text):
        """
        Updates the text of a widget. Call this
        method before drawing to the screen.
        """
        if str(text) != str(self.text):
            self.text = str(text)
            self.__create__()

    def update_colors(self, textcolor=None, backgroundcolor=None, bordercolor=None):
        """
        Updates the colors of a widget. Call this
        method before drawing to the screen.

        This method can be called every loop without worrying about performance problems.
        """
        if textcolor != None and textcolor != self.textcolor:
            self.textcolor = Color.parse(textcolor)
            self.__create__()
        if backgroundcolor != None and backgroundcolor != self.backgroundcolor:
            c = Color.parse(backgroundcolor)
            self.backgroundcolor = c
            self.backgroundcolor_init = c
            val = 50
            self.highlight = (
                min(self.backgroundcolor[0] + val, 255),
                min(self.backgroundcolor[1] + val, 255),
                min(self.backgroundcolor[2] + val, 255),
            )
            self.__create__()
        if bordercolor != None and bordercolor != self.bordercolor:
            self.bordercolor = Color.parse(bordercolor)

    def update_borderwidth(self, borderwidth: int):
        """
        Updates the borderwidth of the widget. Call
        this method before drawing to the screen.
        """
        self.borderwidth = PositiveInt.parse(borderwidth)

    def update_pos(self, xy, anchor=None):
        """
        Changes the widgets position. Call this
        method before drawing to the screen.
        """
        self.xy = Coordinate.parse(xy)
        if not anchor in [
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
        ]:
            raise ValueError(f"invalid argument for 'anchor': {anchor}")
        if anchor is not None:
            self.anchor = anchor

        self.positioning_rect.__setattr__(self.anchor, self.xy)
        self.background_rect.__setattr__("center", self.positioning_rect.center)
        background_rect_coords = getattr(self.background_rect, self.text_binding)
        self.text_rect.__setattr__(
            self.text_binding,
            (
                background_rect_coords[0] + self.text_offset[0],
                background_rect_coords[1] + self.text_offset[1],
            ),
        )

        # data # should actually be accessed through 'self.rect.' but I
        # will leave it as it is to not break any programs
        self.topleft = self.positioning_rect.topleft
        self.topright = self.positioning_rect.topright
        self.bottomleft = self.positioning_rect.bottomleft
        self.bottomright = self.positioning_rect.bottomright
        self.center = self.positioning_rect.center
        self.midtop = self.positioning_rect.midtop
        self.midright = self.positioning_rect.midright
        self.midbottom = self.positioning_rect.midbottom
        self.midleft = self.positioning_rect.midleft
        self.left = self.positioning_rect.left
        self.right = self.positioning_rect.right
        self.top = self.positioning_rect.top
        self.bottom = self.positioning_rect.bottom

        self.rect = self.positioning_rect

        # for buttons:
        self.x_range = (
            self.background_rect.x,
            self.background_rect.x + self.background_rect.width,
        )
        self.y_range = (
            self.background_rect.y,
            self.background_rect.y + self.background_rect.height,
        )

    def set_style(self, bold: bool = None, italic: bool = None, underline: bool = None):
        old_bold = self.bold
        if bold != None:
            self.bold = bool(bold)
        old_italic = self.italic
        if italic != None:
            self.italic = bool(italic)
        old_underline = self.underline
        if underline != None:
            self.underline = bool(underline)
        if (
            old_bold != self.bold
            or old_italic != self.italic
            or old_underline != self.underline
        ):
            self.__create__()

    def get_rect(self) -> pygame.Rect:
        return self.rect
