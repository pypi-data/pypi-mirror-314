import pygame
from .Label import Label

class Paragraph:
    def __init__(self, surface, text, size, xy: tuple, anchor="center", **kwargs):
        """
        Creates a multiline label (using '\\n').

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
                Type: pygame.Surface, pygame.display.set_mode
            text
                the text displayed on the label / button
                Type: Any
            size
                refers to the size of text in pixels
                Type: int
            xy
                refers to the position of the anchor
                Type: tuple, list
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
                the font used when displaying the text; to get all fonts available, use "pygame.font.get_fonts()"
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
            binding_rect
                whether the text_rect or the background_rect should be used with <xy> and <anchor>
                Type: [0, 1]
            borderradius
                used to round the corners of the background_rect; use int for all corners or other types for individual corners
                Type: int, tuple, list
            text_offset
                moves the text by the given values; is inverted if binding_rect == 1
                Type: tuple, list
            image
                blits an image onto the label / button; only works when using <force_dim>
                Type: pygame.Image
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
            "binding_rect": "bR",
            "borderradius": "br",
            "text_offset": "to",
            "image": "img",
            "info": "info",
            "text_binding": "tb",
            "highlight": "hl",
            "active_area": "aA",
        }

        self.surface = surface
        self.text = text
        assert type(size) in [int, float], f"invalid argument for 'size': {size}"
        self.size = int(size)
        assert type(xy) in [tuple, list], f"invalid argument for 'xy': {xy}"
        assert len(xy) == 2, f"invalid argument for 'xy': {xy}"
        self.xy = xy
        assert anchor in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
            ","), f"invalid argument for 'anchor': {anchor}"
        self.anchor = anchor

        kw = kwargs

        # textcolor
        self.textcolor = kw.get("textcolor", None)
        if self.textcolor == None:
            self.textcolor = kw.get(self.ABBREVIATIONS["textcolor"], None)
        if self.textcolor == None:
            self.textcolor = (255, 255, 255)
        # assertion
        if self.textcolor != None:
            assert type(self.textcolor) in [
                tuple, list], f"invalid argument for 'textcolor': {self.textcolor}"
            assert len(self.textcolor) == 3, f"invalid argument for 'textcolor': {self.textcolor}"

        # backgroundcolor
        self.backgroundcolor = kw.get("backgroundcolor", None)
        if self.backgroundcolor == None:
            self.backgroundcolor = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion
        if self.backgroundcolor != None:
            assert type(self.backgroundcolor) in [
                tuple, list], f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"
            assert len(
                self.backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {self.backgroundcolor}"

        # backgroundcolor backup
        self.backgroundcolor_init = kw.get("backgroundcolor", None)
        if self.backgroundcolor_init == None:
            self.backgroundcolor_init = kw.get(self.ABBREVIATIONS["backgroundcolor"], None)
        # assertion completed by previous assertion

        # antialias
        self.antialias = kw.get("antialias", None)
        if self.antialias == None:
            self.antialias = kw.get(self.ABBREVIATIONS["antialias"], None)
        if self.antialias == None:
            self.antialias = True
        # assertion
        assert type(self.antialias) == bool, f"invalid argument for 'antialias': {self.antialias}"

        # font
        self.font = kw.get("font", None)
        if self.font == None:
            self.font = kw.get(self.ABBREVIATIONS["font"], None)
        if self.font == None:
            self.font = ""
        # assertion
        if self.font != None:
            assert type(self.font) == str, f"invalid argument for 'font': {self.font}"

        # x_axis_addition
        self.x_axis_addition = kw.get("x_axis_addition", None)
        if self.x_axis_addition == None:
            self.x_axis_addition = kw.get(self.ABBREVIATIONS["x_axis_addition"], None)
        if self.x_axis_addition == None:
            self.x_axis_addition = 0
        # assertion
        if self.x_axis_addition != None:
            assert type(
                self.x_axis_addition) == int, f"invalid argument for 'x_axis_addition': {self.x_axis_addition}"
            assert self.x_axis_addition >= 0, f"invalid argument for 'x_axis_addition': {self.x_axis_addition}"

        # y_axis_addition
        self.y_axis_addition = kw.get("y_axis_addition", None)
        if self.y_axis_addition == None:
            self.y_axis_addition = kw.get(self.ABBREVIATIONS["y_axis_addition"], None)
        if self.y_axis_addition == None:
            self.y_axis_addition = 0
        # assertion
        if self.y_axis_addition != None:
            assert type(
                self.y_axis_addition) == int, f"invalid argument for 'y_axis_addition': {self.y_axis_addition}"
            assert self.y_axis_addition >= 0, f"invalid argument for 'y_axis_addition': {self.y_axis_addition}"

        # borderwidth
        self.borderwidth = kw.get("borderwidth", None)
        if self.borderwidth == None:
            self.borderwidth = kw.get(self.ABBREVIATIONS["borderwidth"], None)
        if self.borderwidth == None:
            self.borderwidth = 0
        # assertion
        if self.borderwidth != None:
            assert type(self.borderwidth) == int, f"invalid argument for 'borderwidth': {self.borderwidth}"
            assert self.borderwidth >= 0, f"invalid argument for 'borderwidth': {self.borderwidth}"

        # bordercolor
        self.bordercolor = kw.get("bordercolor", None)
        if self.bordercolor == None:
            self.bordercolor = kw.get(self.ABBREVIATIONS["bordercolor"], None)
        if self.bordercolor == None:
            self.bordercolor = (0, 0, 0)
        # assertion
        if self.bordercolor != None:
            assert type(self.bordercolor) in [
                tuple, list], f"invalid argument for 'bordercolor': {self.bordercolor}"
            assert len(self.bordercolor) == 3, f"invalid argument for 'bordercolor': {self.bordercolor}"

        # force_width
        self.force_width = kw.get("force_width", None)
        if self.force_width == None:
            self.force_width = kw.get(self.ABBREVIATIONS["force_width"], None)
        # assertion
        if self.force_width != None:
            assert type(self.force_width) == int, f"invalid argument for 'force_width': {self.force_width}"
            assert self.force_width > 0, f"invalid argument for 'force_width': {self.force_width}"

        # force_height
        self.force_height = kw.get("force_height", None)
        if self.force_height == None:
            self.force_height = kw.get(self.ABBREVIATIONS["force_height"], None)
        # assertion
        if self.force_height != None:
            assert type(self.force_height) == int, f"invalid argument for 'force_height': {self.force_height}"
            assert self.force_height > 0, f"invalid argument for 'force_height': {self.force_height}"

        # force_dim
        force_dim = kw.get("force_dim", None)
        if force_dim == None:
            force_dim = kw.get(self.ABBREVIATIONS["force_dim"], None)
        # assertion
        if force_dim != None:
            if type(force_dim) not in [tuple, list] or len(force_dim) != 2:
                raise ValueError(
                    f"Invalid argument for 'force_dim': '{force_dim}'.")
            if force_dim[0] != None:
                self.force_width = force_dim[0]
            if force_dim[1] != None:
                self.force_height = force_dim[1]

        # binding_rect
        self.binding_rect = kw.get("binding_rect", None)
        if self.binding_rect == None:
            self.binding_rect = kw.get(self.ABBREVIATIONS["binding_rect"], None)
        if self.binding_rect == None:
            self.binding_rect = 0
        # assertion
        assert self.binding_rect in [0, 1], f"invalid argument for 'binding_rect': {self.binding_rect}"

        # borderradius
        self.borderradius = kw.get("borderradius", None)
        if self.borderradius == None:
            self.borderradius = kw.get(self.ABBREVIATIONS["borderradius"], None)
        if self.borderradius == None:
            self.borderradius = (0, 0, 0, 0)
        # assertion
        elif type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) in [tuple, list]:
            if len(self.borderradius) != 4:
                raise ValueError(
                    f"Invalid argument for 'borderradius': {self.borderradius}.")
        else:
            raise Exception(f"invalid argument for 'borderradius': {self.borderradius}")

        # text_offset
        self.text_offset = kw.get("text_offset", None)
        if self.text_offset == None:
            self.text_offset = kw.get(self.ABBREVIATIONS["text_offset"], None)
        if self.text_offset == None:
            self.text_offset = (0, 0)
        # assertion
        if self.text_offset != None:
            assert type(self.text_offset) in [
                tuple, list], f"invalid argument for 'text_offset': {self.text_offset}"
            assert len(self.text_offset) == 2, f"invalid argument for 'text_offset': {self.text_offset}"

        # image
        self.image = kw.get("image", None)
        if self.image == None:
            self.image = kw.get(self.ABBREVIATIONS["image"], None)
        # # assertion # ! somethings not working here # TODO
        # if self.image != None:
        #     if self.force_width == None or self.force_height == None:
        #         raise ValueError(
        #             "If an image is used, forced dimensions are needed!")
        #     try:
        #         img = pygame.transform.scale(pygame.image.load(self.image), (self.force_width, self.force_height))
        #         self.image = img
        #     except FileNotFoundError:
        #         raise Exception(f"Could not find file '{self.image}'")

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
            assert self.text_binding in "topleft,midtop,topright,midleft,center,midright,bottomleft,midbottom,bottomright".split(
                ","), f"invalid argument for 'text_binding': {self.text_binding}"

        # highlight
        self.highlight = kw.get("highlight", None)
        if self.highlight == None:
            self.highlight = kw.get(self.ABBREVIATIONS["highlight"], None)
        # assertion
        if self.highlight != None:
            assert type(self.backgroundcolor) in [
                tuple, list], f"'backgroundcolor' (currently: {self.backgroundcolor}) must be defined when using 'highlight' (currently: {self.highlight})"
            if self.highlight == True:
                val = 50
                self.highlight = (
                    min(self.backgroundcolor[0] + val, 255),
                    min(self.backgroundcolor[1] + val, 255),
                    min(self.backgroundcolor[2] + val, 255)
                )
            else:
                assert type(self.highlight) in [
                    tuple, list], f"unknown format for 'highlight': (type: {type(self.highlight)}, value: {self.highlight})"

        # active_area
        self.active_area = kw.get("active_area", None)
        if self.active_area == None:
            self.active_area = kw.get(self.ABBREVIATIONS["active_area"], None)
        # assertion
        if self.active_area != None:
            if type(self.active_area) in [tuple, list]:
                assert len(self.active_area) == 4, f"invalid argument for 'active_area': {self.active_area}"
                self.active_area = pygame.Rect(*self.active_area)
            elif type(self.active_area) == pygame.Rect:
                pass
            else:
                raise Exception(f"invalid argument for 'active_area': {self.active_area}")

        self.kwargs = kwargs
        self.__create__()

    def __create__(self):
        self.__labels__: list[Label] = []
        strings = self.text.split("\n")
        width = 0
        height = 0
        for string in strings:
            l = Label(
                self.surface, string, self.size, self.xy, **self.kwargs
            )
            width = max(width, l.rect.width)
            height = max(height, l.rect.height)

        # removing some arguments by setting them to default
        # bR, fd
        parsed_kwargs = self.kwargs.copy()
        parsed_kwargs["bR"] = 1
        parsed_kwargs["fd"] = (width, height)
        self.__borderwidth__ = self.borderwidth
        parsed_kwargs["bw"] = 0
        self.__borderradius__ = self.borderradius
        parsed_kwargs["br"] = (0, 0, 0, 0)
        self.__bordercolor__ = self.bordercolor
        # kwargs["bc"] = (0, 0, 0) # not needed

        for count, string in enumerate(strings):
            self.__labels__.append(
                Label(
                    self.surface, string, self.size,
                    (self.xy[0],
                     self.xy[1] + height * count),
                    self.anchor, **parsed_kwargs))

        fl = self.__labels__[0]     # first label
        ll = self.__labels__[-1]    # last label
        self.rect = pygame.Rect(fl.rect.left, fl.rect.top, ll.rect.right-fl.rect.left,
                                ll.rect.bottom-fl.rect.top)

    def draw(self):
        for label in self.__labels__:
            label.draw()
        if self.__borderwidth__ > 0:
            pygame.draw.rect(self.surface, self.__bordercolor__, self.rect,
                             self.__borderwidth__, *self.__borderradius__)

    def update_text(self, text: str):
        if str(text) != str(self.text):
            self.text = str(text)
            self.__create__()

    def update_colors(self, textcolor=None, backgroundcolor=None, bordercolor=None):
        if textcolor != None:
            assert type(textcolor) in [
                tuple, list], f"invalid argument for 'textcolor': {textcolor}"
            assert len(textcolor) == 3, f"invalid argument for 'textcolor': {textcolor}"
            self.textcolor = textcolor
            self.__create__()
        if backgroundcolor != None:
            assert type(backgroundcolor) in [
                tuple, list], f"invalid argument for 'backgroundcolor': {backgroundcolor}"
            assert len(
                backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {backgroundcolor}"
            self.backgroundcolor = backgroundcolor
            self.backgroundcolor_init = backgroundcolor
            val = 50
            self.highlight = (
                min(self.backgroundcolor[0] + val, 255),
                min(self.backgroundcolor[1] + val, 255),
                min(self.backgroundcolor[2] + val, 255)
            )
            self.__create__()
        if bordercolor != None:
            assert type(bordercolor) in [
                tuple, list], f"invalid argument for 'bordercolor': {bordercolor}"
            assert len(bordercolor) == 3, f"invalid argument for 'bordercolor': {bordercolor}"
            self.bordercolor = bordercolor
