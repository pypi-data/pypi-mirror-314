import pygame
from .Label import Label

class Button(Label):
    def __init__(self, surface, text, size, xy: tuple, anchor="center", **kwargs):
        """
        Creates a clickable button.

        Instructions:
            - To create a button, create an instance of this class before
            the mainloop of the game.
            - To make the button appear, call the method 'self.draw()' in
            every loop of the game.
            - To check if the button has been clicked, call the method
            'self.update()' with a list of mouse events in an if-statement.

        Example (simplified):
            button = Button(screen, "Hello world!", 32, (100,100), "topleft")
            while True:
                events = pygame.event.get()
                if button.update(events):
                    ...
                button.draw()

        For information about arguments see parent class (Label).
        """

        super().__init__(surface, text, size, xy, anchor, **kwargs)

    def update(self, event_list, button: int = 1, offset: tuple = (0, 0)) -> bool:
        """
        Checks if button has been pressed and returns True if so.
        <button> can specify a certain button (1-3).
        <offset> will be subtracted from the current mouse position.
        """
        assert type(button) == int, f"invalid argument for 'button': {button}"
        assert 1 <= button <= 5, f"invalid argument for 'button': {button}"
        assert type(offset) in [tuple, list], f"invalid argument for 'offset': {offset}"
        assert len(offset) == 2, f"invalid argument for 'offset: {offset}"

        # stops if one_click_manager tells that a click has taken place elsewhere
        if self.one_click_manager != None and self.one_click_manager.get_clicked() == True:
            self.__is_touching__ = False
            return False

        # managing the actual clicks
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = list(event.pos)
                if self.active_area != None and not self.active_area.collidepoint(pos):
                    continue
                pos[0] -= offset[0]
                pos[1] -= offset[1]
                if button == None:
                    if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                        if self.one_click_manager != None:
                            self.one_click_manager.set_clicked()
                        return True

                elif 0 < button < 4:
                    if button == event.button:
                        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                            if self.one_click_manager != None:
                                self.one_click_manager.set_clicked()
                            return True

                else:
                    raise ValueError(f"invalid argument for 'button': {button}")

        if self.one_click_manager != None and self.one_click_manager.get_hovering() == True:
            self.__is_touching__ = False
            return False

        # managing the hovering (highlight)
        pos = list(pygame.mouse.get_pos())
        if self.active_area != None and not self.active_area.collidepoint(pos):
            self.__is_touching__ = False
            return False
        pos[0] -= offset[0]
        pos[1] -= offset[1]
        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
            if self.highlight != None:
                self.__is_touching__ = True
            if self.one_click_manager != None:
                self.one_click_manager.set_hovering()
        else:
            self.__is_touching__ = False

        return False
