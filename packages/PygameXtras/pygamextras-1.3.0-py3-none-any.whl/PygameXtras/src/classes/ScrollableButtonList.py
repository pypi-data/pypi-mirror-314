import pygame
from .Button import Button

class ScrollableButtonList:
    def __init__(
            self, surface, target_rect: tuple[int, int, int, int], scrolling_speed: int, backgroundcolor: tuple = (0,0,0)):
        """
        target_rect specifies the area in which buttons will be visible

        to update the buttons, use: 
            for b in self.get_buttons():
                if b.update(event_list, offset=self.get_offset()):
                    ...

        also, a general update every loop is needed:
            self.update(event_list)

        it is also possible to change the buttons:
            self.clear_buttons()
            self.add_buttons(list_of_button_names)

        IMPORTANT:
        this widget has to be drawn DIRECTLY to the screen, otherwise the clicking will be messed up.
        to check the active area, use self.get_rect() and draw it to the screen
        ALSO IMPORTANT:
        the buttons might not show up if the self.update method is not constantly called. to
        fix this, just call the method once with an emtpy list after initializing the class. (self.update([]))
        """

        # only vertical scroll
        # TODO: assertions
        assert type(surface) == pygame.Surface, f"invalid argument for 'surface': {surface}"
        self.__main_surface__ = surface
        assert type(target_rect) in [tuple, list, pygame.Rect]
        if type(target_rect) in [tuple, list]:
            assert len(target_rect) == 4, f"invalid argument for 'target_rect': {target_rect}"
        self.__target_rect__ = pygame.Rect(target_rect)
        self.__surface__ = pygame.Surface((self.__target_rect__.width, 0))

        assert type(scrolling_speed) == int, f"invalid argument for 'scrolling_speed': {scrolling_speed}"
        assert scrolling_speed > 0, f"invalid argument for 'scrolling_speed': {scrolling_speed}"
        self.__scrolling_speed__ = scrolling_speed

        assert type(backgroundcolor) in [tuple, list], f"invalid argument for 'backgroundcolor': {backgroundcolor}"
        assert len(backgroundcolor) == 3, f"invalid argument for 'backgroundcolor': {backgroundcolor}"
        self.__backgroundcolor__ = backgroundcolor        

        self.__scroll__ = 0
        self.__max_scroll__ = self.__surface__.get_height() - self.__target_rect__.height #! has to be reconfigured if anything changes

        self.__button_names__: list[str] = []
        self.__old_button_names__: list[str] = []
        self.__buttons__: list[Button] = []

        self.__int_surf__ = pygame.Surface((10, 10)) # internal surface

    def set_button_style(self, size: int, **kwargs):
        """ dont forget about the backgroundcolor and the height """
        try:
            Button(self.__int_surf__, "Test", size=size, xy=(0,0), anchor="topleft", **kwargs)
            self.__size__ = size
            kwargs["bR"] = 1 # important !
            kwargs["fw"] = self.__target_rect__.width
            kwargs["aA"] = self.__target_rect__
            self.__style__ = kwargs
        except Exception as e:
            raise e

    def add_button(self, button_name: str):
        self.__button_names__.append(str(button_name))

    def add_buttons(self, button_names: list[str]):
        for button in button_names:
            self.add_button(button)

    def clear_buttons(self):
        """ removes all buttons """
        self.__button_names__ = []
    
    def reset_scroll(self):
        """ resets the scroll value """
        self.__scroll__ = 0

    def set_buttons(self, button_names: list[str]):
        self.__button_names__ = []
        self.add_buttons(button_names)

    def update_surface(self):
        """ updates the surface if something has changed """

        if self.__old_button_names__ != self.__button_names__:
            self.__old_button_names__ = self.__button_names__[:]
            self.__buttons__ = []
            borderwidth = 0
            for count, name in enumerate(self.__button_names__):
                if count == 0:
                    self.__buttons__.append(
                        Button(self.__int_surf__, name, self.__size__, (0,0), "topleft", **self.__style__)
                    )
                    borderwidth = self.__buttons__[0].borderwidth
                else:
                    self.__buttons__.append(
                        Button(self.__int_surf__, name, self.__size__, (self.__buttons__[count-1].left, self.__buttons__[count-1].bottom-borderwidth), "topleft", **self.__style__)
                    )

            # determining the surface height
            if len(self.__buttons__) > 0:
                lowest = self.__buttons__[-1].bottom
            else:
                lowest = 0
            self.__surface__ = pygame.Surface((self.__target_rect__.width, lowest))
            
            self.__max_scroll__ = self.__surface__.get_height() - self.__target_rect__.height
            if self.__max_scroll__ > 0 and self.__scroll__ > self.__max_scroll__:
                self.__scroll__ = self.__max_scroll__
            elif self.__max_scroll__ <= 0:
                self.__scroll__ = 0

    def update_scroll(self, event_list):
        """ updates the scroll value """
        
        if self.__max_scroll__ > 0:
            for event in event_list:
                if event.type == pygame.MOUSEWHEEL:
                    self.__scroll__ = max(
                        min(self.__max_scroll__, self.__scroll__ + event.y*-1*self.__scrolling_speed__), 0)

    def update(self, event_list):
        """ updates surface and scroll """
        self.update_surface()
        self.update_scroll(event_list)

    def draw(self):
        self.__surface__.fill(self.__backgroundcolor__)
        for button in self.__buttons__:
            button.draw_to(self.__surface__)
        tr = self.__target_rect__
        pygame.draw.rect(self.__main_surface__, self.__backgroundcolor__, tr)
        if self.__surface__.get_height() > tr.height:
            self.__main_surface__.blit(self.__surface__.subsurface(
                (0, self.__scroll__, tr[2], tr[3])), self.__target_rect__.topleft)
        else:
            self.__main_surface__.blit(self.__surface__, self.__target_rect__.topleft)

    def get_buttons(self):
        return self.__buttons__

    def get_offset(self):
        return self.__target_rect__[0], self.__target_rect__[1] - self.__get_scroll__()

    def __get_scroll__(self):
        return self.__scroll__

    def get_rect(self):
        return self.__target_rect__