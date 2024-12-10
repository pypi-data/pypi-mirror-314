import pygame
from .Button import Button
from .Keyboard import Keyboard

class Entry(Button):
    def __init__(self, surface, text, size, xy: tuple, anchor="center", **kwargs):
        """
        Click to activate, click somewhere else to deactivate.
        If active, typed letters will appear on the widget.
        An indication, that the entry widget is active, has to
        be implemented externally (use self.get_state()).

        IMPORTANT:
            - The update method takes a complete event list as
              an input, while a regular button just needs a mouse event list.
            - Entries (unlike buttons) should NOT be updated in an if-statement!

        Additional keywords:
            max_chars / mc
                maximum number of characters
                Type: int
            text_when_empty / twe
                text that appears when there is currently no other content
                Type: str
            auto_style / ast
                if text_when_empty is set, this text will appear italic,
                while the real user input will appear in the regular font style
                IMPORTANT: this mechanic breaks if the style is set manually
                after the first initialization of the widget
                Type: bool
            strict_input / si
                only allow numeric ("int", "float", 0 - +inf by using "int+" / "float+") or alphabetic ("str") input
                Type: str
            show_cursor
                show a moveable (left and right) cursor, that makes it possible
                to edit text in the middle without deleting everything to its right
                Type: bool
        """

        # max_chars
        self.max_chars = kwargs.get("max_chars", None)
        if self.max_chars == None:
            self.max_chars = kwargs.get("max", None)
        # assertion
        if self.max_chars != None:
            assert type(self.max_chars) == int, f"invalid argument for 'max_chars': {self.max_chars}"
            assert self.max_chars >= 0, f"invalid argument for 'max_chars': {self.max_chars}"

        # min_chars
        self.min_chars = kwargs.get("min_chars", None)
        if self.min_chars == None:
            self.min_chars = kwargs.get("min", None)
        # assertion
        if self.min_chars != None:
            assert type(self.min_chars) == int, f"invalid argument for 'min_chars': {self.min_chars}"
            assert self.min_chars >= 0, f"invalid argument for 'min_chars': {self.min_chars}"

        # text_when_empty
        self.text_when_empty = kwargs.get("text_when_empty", None)
        if self.text_when_empty == None:
            self.text_when_empty = kwargs.get("twe", None)
        if self.text_when_empty != None:
            self.text_when_empty = str(self.text_when_empty)
        # assertion not needed

        # auto_style
        self.auto_style = kwargs.get("auto_style", None)
        if self.auto_style == None:
            self.auto_style = kwargs.get("ast", None)
        if self.auto_style == None:
            self.auto_style = False
        # assertion
        self.auto_style = bool(self.auto_style)

        # strict_input
        self.strict_input = kwargs.get("strict_input", None)
        if self.strict_input == None:
            self.strict_input = kwargs.get("si", None)
        # assertion
        assert self.strict_input is None or self.strict_input in ["int", "float", "int+", "float+", "str"], f"invalid argument for 'strict_input': {self.strict_input}"

        # show_cursor
        self.show_cursor = kwargs.get("show_cursor", None)
        if self.show_cursor == None:
            self.show_cursor = kwargs.get("sc", True)
        # assertion
        self.show_cursor = bool(self.show_cursor)
        self.__cursor_pos = 0 # 0 means "at the end", while 2 means "2 characters from the end", ...
        self.__old_cursor_pos = 0
        
        
        

        self.__state__ = False
        self.__old_state__ = False
        self.__force__ = False # used to set state even before the update method
        self.__permanent_state__ = None
        self.__value__ = str(text)
        self.__old_value__ = str(text)

        self.__keyboard__ = Keyboard()
        self.__keyboard__.set_forbidden_characters(["\t", "\n"])




        super().__init__(surface, text, size, xy, anchor, **kwargs)

        self.bold_init = self.bold
        self.italic_init = self.italic

        self.__manage_twe()

    def update(self, event_list, button: int = 1, offset: tuple = (0, 0)) -> bool:
        """
        Checks if entry has been clicked on and activates widget if so.
        Should be used with a regular event_list.
        <button> can specify a certain button (1-3).
        Also updates the text, if input is detected.
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
                        self.__state__ =  True
                    else:
                        self.__state__ = False

                elif 0 < button < 4:
                    if button == event.button:
                        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
                            if self.one_click_manager != None:
                                self.one_click_manager.set_clicked()
                            self.__state__ =  True
                        else:
                            self.__state__ = False

                else:
                    raise ValueError(f"invalid argument for 'button': {button}")
        if self.__permanent_state__ != None:
            self.__state__ = self.__permanent_state__

        if self.__force__ != None:
            self.__state__ = self.__force__
            self.__force__ = None

        # managing the hovering (highlight)
        pos = list(pygame.mouse.get_pos())
        if self.active_area != None and not self.active_area.collidepoint(pos):
            self.__is_touching__ = False
            self.__state__ = False
        pos[0] -= offset[0]
        pos[1] -= offset[1]
        if self.x_range[0] < pos[0] < self.x_range[1] and self.y_range[0] < pos[1] < self.y_range[1]:
            if self.highlight != None:
                self.__is_touching__ = True
            if self.one_click_manager != None:
                self.one_click_manager.set_hovering()
        else:
            self.__is_touching__ = False

        if self.__state__:

            # deleting chars
            for event in event_list:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    if self.min_chars == None or len(self.__value__) - 1 >= self.min_chars:
                        if self.show_cursor:
                            if self.__cursor_pos != len(self.__value__):
                                val_list = list(self.__value__)
                                del val_list[len(self.__value__)-1-self.__cursor_pos]
                                self.__value__ = "".join(val_list)
                        else:
                            self.__value__ = self.__value__[:-1]

                # managing cursor
                if self.show_cursor and event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.__cursor_pos += 1
                    elif event.key == pygame.K_RIGHT:
                        self.__cursor_pos -= 1
                    elif event.key == 1073741898: # key "pos1"
                        self.__cursor_pos = len(self.__value__)
                    elif event.key == 1073741901: # key "ende"
                        self.__cursor_pos = 0

            # adding chars
            val = self.__keyboard__.get(event_list)
            new_val_list: list = list(self.__value__)
            new_val_list.insert(len(self.__value__) - self.__cursor_pos, val)
            new_val: str = "".join(new_val_list)

            # checks for self.strict_input and sets val to "" if condition does not apply
            if self.strict_input is not None and val != "":

                if new_val == "-":
                    if not (self.strict_input == "int+" or self.strict_input == "float+"):
                        self.__value__ = new_val
                elif new_val.startswith("-"):
                    if (self.strict_input == "int"     and new_val[1:].isnumeric()) or \
                       (self.strict_input == "float"   and "".join(new_val[1:].split(".", 1)).isnumeric()) or \
                       (self.strict_input == "str"     and new_val[1:].isalpha()):
                        self.__value__ = new_val
                else:
                    if (self.strict_input == "int"     and new_val.isnumeric()) or \
                       (self.strict_input == "float"   and "".join(new_val.split(".", 1)).isnumeric()) or \
                       (self.strict_input == "str"     and new_val.isalpha()) or \
                       (self.strict_input == "int+"    and new_val.isnumeric()) or \
                       (self.strict_input == "float+"  and "".join(new_val.split(".", 1)).isnumeric()):
                        self.__value__ = new_val
                        
            else:
                self.__value__ = new_val



            # dealing with self.max_chars
            if self.max_chars is not None:
                self.__value__ = self.__value__[:self.max_chars]

        if self.__value__ != self.__old_value__ or self.__cursor_pos != self.__old_cursor_pos or self.__old_state__ != self.__state__:
            if self.show_cursor:
                if self.__old_state__ != self.__state__:
                    self.__cursor_pos = 0
                else:
                    self.__clamp_cursor()
                self.__old_cursor_pos = self.__cursor_pos
            self.__old_state__ = self.__state__
            self.__refresh_text()

            # maybe the following line has to be unindented once, I am not sure
            self.__manage_twe()

    def get_state(self):
        """
        Returns boolean whether the entry is active (True) or not (False).
        """
        return self.__state__

    def get(self):
        """
        Returns the text.
        """
        return self.__value__

    def set(self, value):
        """
        Sets the value of the Entry.
        """
        self.__value__ = str(value)
        self.__refresh_text()

    def set_forbidden_characters(self, characters: list):
        """
        Bans all given characters.
        """
        self.__keyboard__.set_forbidden_characters(characters)

    def set_forbidden_characters_for_filename(self):
        forbidden_chars_in_filenames = "<>:\"/\\|?* \n\t\r,.;"
        self.set_forbidden_characters(list(forbidden_chars_in_filenames))

    def clear(self):
        """
        Clears the text.
        """
        self.__value__ = ""
        self.__refresh_text()

    def set_state(self, state: bool):
        """
        Sets activity state.
        """
        self.__force__ = bool(state)

    def set_permanent_state(self, state: bool):
        """
        Sets activity state permanently. Remove with self.remove_permanent_state().
        """
        self.__permanent_state__ = bool(state)

    def remove_permanent_state(self):
        """
        Removes permanent state.
        """
        self.__permanent_state__ = None
    
    def __refresh_text(self):
        if self.show_cursor and self.__state__:
            chars = list(self.__value__)
            chars.insert(len(self.__value__) - self.__cursor_pos, "|")
            self.update_text("".join(chars))
        else:
            self.update_text(self.__value__)
        self.__old_value__ = self.__value__

    def __manage_twe(self):
        if self.text_when_empty != None and len(self.__value__) == 0:
            self.update_text(self.text_when_empty)
            if self.auto_style:
                self.set_style(italic=True)
        else:
            if self.auto_style:
                self.set_style(self.bold_init, self.italic_init)

    def __clamp_cursor(self):
        self.__cursor_pos = max(0, min(self.__cursor_pos, len(self.__value__)))
