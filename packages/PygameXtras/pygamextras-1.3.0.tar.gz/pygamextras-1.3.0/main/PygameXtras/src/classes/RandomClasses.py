import pygame
import os
import sys
from .Functions import vect_sum
from .Label import Label
from .Button import Button
from .Messagebox import Messagebox


class ImageFrame:
    def __init__(
            self, surface, width_height: tuple, xy: tuple, anchor="center", auto_scale=True, borderwidth=0,
            bordercolor=(0, 0, 0),
            borderradius=0):
        self.surface = surface
        self.width = width_height[0]
        self.height = width_height[1]
        self.xy = xy
        self.anchor = anchor
        self.auto_scale = auto_scale
        self.borderwidth = borderwidth
        self.bordercolor = bordercolor
        self.image = None
        self.borderradius = borderradius
        if type(self.borderradius) == int:
            self.borderradius = (
                self.borderradius, self.borderradius, self.borderradius, self.borderradius)
        elif type(self.borderradius) == tuple:
            if len(self.borderradius) != 4:
                raise ValueError(
                    f"Invalid argument for 'borderradius': {self.borderradius}.")

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # putting in correct position
        if anchor == "topleft":
            self.rect.topleft = xy
        elif anchor == "topright":
            self.rect.topright = xy
        elif anchor == "bottomleft":
            self.rect.bottomleft = xy
        elif anchor == "bottomright":
            self.rect.bottomright = xy
        elif anchor == "center":
            self.rect.center = xy
        elif anchor == "midtop":
            self.rect.midtop = xy
        elif anchor == "midright":
            self.rect.midright = xy
        elif anchor == "midbottom":
            self.rect.midbottom = xy
        elif anchor == "midleft":
            self.rect.midleft = xy

    def insert_image(self, image):
        """
        Puts a pygame image into the frame.
        """
        if self.auto_scale == True:
            self.image = pygame.transform.scale(
                image, (self.width, self.height))
        else:
            self.image = image
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.rect.center

    def draw(self):
        """
        Draws object to the screen.
        """
        if self.auto_scale == False:
            self.surface.blit(self.image, self.image_rect)
        else:
            self.surface.blit(self.image, self.rect)
        if self.borderwidth > 0:
            pygame.draw.rect(
                self.surface, self.bordercolor, self.rect, self.borderwidth,
                border_top_left_radius=self.borderradius[0],
                border_top_right_radius=self.borderradius[1],
                border_bottom_right_radius=self.borderradius[2],
                border_bottom_left_radius=self.borderradius[3])


class PlayStation_Controller_Buttons:
    def __init__(self):
        """
        Makes it easier to map PlayStation-Controller buttons to functions.
        """
        self.cross = 0
        self.circle = 1
        self.square = 2
        self.triangle = 3
        self.share_button = 4
        self.ps_button = 5
        self.options_button = 6
        self.left_stick_in = 7
        self.right_stick_in = 8
        self.l1 = 9
        self.r1 = 10
        self.arrow_up = 11
        self.arrow_down = 12
        self.arrow_left = 13
        self.arrow_right = 14
        self.touch_pad_click = 15


class Switcheroo:
    def __init__(self, surface, switcheroo_elements, previous_next_keys, lower_higher_keys,
                 scrolling_cooldown, starting_index=0, bordercolor=(255, 255, 255),
                 borderwidth=1, borderradius=0):
        """
        game = pygame game object 
        """
        self.surface = surface
        self.switcheroo_elements = switcheroo_elements
        self.previous_key, self.next_key = previous_next_keys[0], previous_next_keys[1]
        self.lower_key, self.higher_key = lower_higher_keys[0], lower_higher_keys[1]
        self.scrolling_cooldown = scrolling_cooldown
        self.scrolling_cooldown_frames = 0
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.borderradius = borderradius

        self.current_index = starting_index  # the element thats currently being edited

        if starting_index not in range(len(switcheroo_elements)):
            raise ValueError(
                f"Invalid argument for 'starting index': '{starting_index}'. Index out of range.")

    def draw_box(self):
        """
        Outlines the current field.
        """
        active_element = self.switcheroo_elements[self.current_index]
        label = active_element.label_object
        pygame.draw.rect(
            self.surface, self.bordercolor,
            (label.rect.x, label.rect.y, label.rect.width, label.rect.height),
            self.borderwidth, self.borderradius)

    def update(self, keys_pressed):
        """
        Updates all values and returns them.

        Usage:
        value_1, value_2, ... = self.update(keys_pressed)
        """
        # decreases the cooldown for all elements
        for element in self.switcheroo_elements:
            if element.cooldown_frames > 0:
                element.cooldown_frames -= 1
        if self.scrolling_cooldown_frames > 0:
            self.scrolling_cooldown_frames -= 1
        # END OF BLOCK #

        # handles global scrolling first #
        keys = keys_pressed
        if not (keys[self.previous_key] and keys[self.next_key]):
            if keys[self.previous_key] and self.current_index > 0 and self.scrolling_cooldown_frames == 0:
                self.current_index -= 1
                self.scrolling_cooldown_frames = self.scrolling_cooldown
            if keys[self.next_key] and self.current_index < len(self.switcheroo_elements)-1 and self.scrolling_cooldown_frames == 0:
                self.current_index += 1
                self.scrolling_cooldown_frames = self.scrolling_cooldown
        # END OF BLOCK #

        # handles individual scrolling second #
        active_element = self.switcheroo_elements[self.current_index]
        if not (keys[self.lower_key] and keys[self.higher_key]):
            if keys[self.lower_key] and active_element.cooldown_frames == 0:
                active_element.decrease()
            if keys[self.higher_key] and active_element.cooldown_frames == 0:
                active_element.increase()
        # END OF BLOCK #

        # in the end, update all text fields and return the values
        values_list = []
        for element in self.switcheroo_elements:
            shown_value = element.var_range[element.index]
            true_value = ...

            # dict like {"Allowed":True,"Forbidden":False} ... basically {"shown_value":true_value}
            has_custom_value = False
            if element.custom_dict != None:
                if shown_value in element.custom_dict.keys():
                    true_value = element.custom_dict[shown_value]
                    has_custom_value = True

            element.label_object.update_text(shown_value)
            if has_custom_value == True:
                values_list.append(true_value)
            else:
                values_list.append(shown_value)
        # END OF BLOCK #

        return values_list


class Switcheroo_Element:
    def __init__(self, label_object, variable, var_range, starting_variable, cooldown, custom_dict=None):
        self.label_object = label_object
        self.variable = variable
        self.var_range = var_range
        self.cooldown = cooldown
        self.cooldown_frames = 0
        self.index = ...
        self.custom_dict = custom_dict

        # searching for the index of the starting variable
        # if type(starting_variable) != str:
        #     raise ValueError(f"Starting variable must be 'str'.")
        found = False
        for num, var in enumerate(var_range):
            if str(var) == str(starting_variable):
                self.index = num
                found = True
                break
        if found == False:
            raise ValueError(
                f"The starting variable '{starting_variable}' could not be found in the variables range.")

    def increase(self):
        """
        Increases self.index by 1 if its within the defined range.
        """
        if self.index + 1 < len(self.var_range):
            self.index += 1
            self.cooldown_frames = self.cooldown

    def decrease(self):
        """
        Decreases self.index by 1 if its within the defined range.
        """
        if self.index - 1 >= 0:
            self.index -= 1
            self.cooldown_frames = self.cooldown


class ImageImport_rotate:
    def __init__(self, assets_dir):
        """
        Simplifies image importing ('up','right','dowm','left').
        """
        self.assets_dir = assets_dir

    def load(self, img_name, width, height, facing="right", colorkey=None, assets_dir=None):
        if assets_dir != None:
            ad = assets_dir
        else:
            ad = self.assets_dir
        try:
            img = pygame.image.load(os.path.join(ad, img_name))
        except:
            raise ValueError(
                f"Could not find file '{img_name}' in '{ad}'.")
        img = pygame.transform.scale(img, (int(width), int(height)))
        if colorkey != None:
            img.set_colorkey(colorkey)
        if facing == "right":
            self.img_right = img
            self.img_down = pygame.transform.rotate(img, 270)
            self.img_left = pygame.transform.rotate(img, 180)
            self.img_up = pygame.transform.rotate(img, 90)
        elif facing == "down":
            self.img_down = img
            self.img_left = pygame.transform.rotate(img, 270)
            self.img_up = pygame.transform.rotate(img, 180)
            self.img_right = pygame.transform.rotate(img, 90)
        elif facing == "left":
            self.img_left = img
            self.img_up = pygame.transform.rotate(img, 270)
            self.img_right = pygame.transform.rotate(img, 180)
            self.img_down = pygame.transform.rotate(img, 90)
        elif facing == "up":
            self.img_up = img
            self.img_right = pygame.transform.rotate(img, 270)
            self.img_down = pygame.transform.rotate(img, 180)
            self.img_left = pygame.transform.rotate(img, 90)

        dct = {}
        dct["right"] = self.img_right
        dct["down"] = self.img_down
        dct["left"] = self.img_left
        dct["up"] = self.img_up
        return dct


class ImageImport_flip:
    def __init__(self, assets_dir):
        """
        Simplifies image importing ('right','left').
        """
        self.assets_dir = assets_dir

    def load(self, img_name, width, height, facing="right", colorkey=None, assets_dir=None):
        if assets_dir != None:
            ad = assets_dir
        else:
            ad = self.assets_dir
        try:
            img = pygame.image.load(os.path.join(ad, img_name))
        except:
            raise ValueError(
                f"Could not find file '{img_name}' in '{ad}'.")
        img = pygame.transform.scale(img, (int(width), int(height)))
        if colorkey != None:
            img.set_colorkey(colorkey)
        if facing == "right":
            self.img_right = img
            self.img_left = pygame.transform.flip(img, True, False)
        elif facing == "left":
            self.img_left = img
            self.img_right = pygame.transform.flip(img, True, False)

        dct = {}
        dct["right"] = self.img_right
        dct["left"] = self.img_left
        return dct


class Tile:
    def __init__(self, image, rect, type=None, hitbox=None, pos_hint=None):
        """
        image needs to be an image of the size of rect.
        rect needs to be a pygame.Rect object.
        hitbox can be None or a pygame.Rect object.
        """
        self.image = image
        self.rect = rect
        self.type = type
        self.pos_hint = pos_hint
        if hitbox != None:
            self.hitbox = pygame.Rect(
                self.rect.x + hitbox.x,
                self.rect.y + hitbox.y,
                hitbox.width,
                hitbox.height
            )


class FileDialogElement:
    def __init__(self, surface, name: str, count: int, role: str, topleft_pos, dimensions, textsize, textcolor,
                 backgroundcolor2, borderwidth):
        self.name = name
        self.role = role

        if self.role == "dir":
            bgc = (250, 150, 70)
        elif self.role == "file":
            bgc = backgroundcolor2

        self.b_name = Button(
            surface, name, textsize, (0, count * textsize),
            "topleft", fd=(dimensions[0], textsize),
            tc=textcolor, bgc=bgc, hl=True, bR=1, tb="midleft", to=(5, 1),
            aA=(topleft_pos[0] + 0, topleft_pos[1] + textsize, dimensions[0],
                dimensions[1] - textsize - 50), bc=(0, 0, 200), bw=borderwidth, br=1)

    def update(self, mouse_events, _offset):
        if self.b_name.update(mouse_events, offset=_offset):
            return True
        return False

    def draw(self):
        self.b_name.draw()


class FileDialog:
    def __init__(
            self, surface, pygame_clock, fps, topleft_pos=(100, 50),
            dimensions=(600, 400), textsize=25,
            textcolor=(0, 0, 0),
            backgroundcolor1=(150, 180, 240),
            backgroundcolor2=(128, 128, 128)):

        self.blitting_surface = surface
        self.pygame_clock = pygame_clock
        self.fps = fps
        self.topleft_pos = topleft_pos
        assert dimensions[0] >= 200
        assert dimensions[1] >= 200
        self.dimensions = dimensions
        assert 20 <= textsize <= 40
        self.textsize = textsize
        self.textcolor = textcolor
        self.backgroundcolor1 = backgroundcolor1
        self.backgroundcolor2 = backgroundcolor2


        w, h = self.dimensions
        self.center = (self.topleft_pos[0]+w//2, self.topleft_pos[1]+h//2)
        self.surface = pygame.Surface((w, h))
        self.surface.fill(self.backgroundcolor1)
        self.messagebox = Messagebox(self.blitting_surface, self.pygame_clock, self.fps, (topleft_pos[0]+dimensions[0]//2, topleft_pos[1]+dimensions[1]//2))
        self.l_path = Label(
            self.surface, "", textsize, (0, 0),
            "topleft", tc=self.textcolor, bgc=self.backgroundcolor1, br=1, tb="midright", to=(-4, 2),
            bR=1, fd=(self.dimensions[0],
                      textsize),
            bw=1)
        self.b_back = Button(
            self.surface, "<", int(textsize*1.5), (0, 0),
            "topleft", tc=self.textcolor, fd=(textsize, textsize),
            bgc=self.backgroundcolor1, hl=True, bw=1, bR=1, to=(0, -3))

        self.b_cancel = Button(self.surface, "Cancel", textsize,
                               (11, self.dimensions[1] - int(self.textsize * 1.5) // 2),
                               "midleft", tc=self.textcolor, bgc=self.backgroundcolor1, bR=1, xad=10,
                               fh=textsize, bw=3, br=1, hl=True)
        self.l_selected = Label(self.surface, "Selected:", textsize,
                                vect_sum(self.b_cancel.midright, (10, 0)),
                                "midleft", bR=1, tc=self.textcolor, bgc=self.backgroundcolor1)
        self.l_selected_name = Label(
            self.surface, "", textsize, vect_sum(self.l_selected.midright, (10, 0)),
            "midleft", bR=1, tc=self.textcolor, bgc=self.backgroundcolor1)
        self.b_open = Button(self.surface, "Open", textsize,
                             (self.dimensions[0] - 11, self.b_cancel.rect.centery),
                             "midright", tc=self.textcolor, bgc=self.backgroundcolor1, bR=1, xad=10,
                             fh=textsize, bw=3, br=1, hl=True)

        self.b_req_ending = Button(
            self.surface, "!", textsize, vect_sum(self.b_open.midleft, (-5, 0)),
            "midright", tc=(0,0,0), bR=1, f="bauhaus", to=(0, 0),
            br=1, fd=(textsize, textsize),
            bw=3, hl=True, bgc=(255, 80, 80))

    def error(self, error_message: str):
        surface = pygame.Surface((self.textsize*10, self.textsize*4))
        surface.fill(self.backgroundcolor2)
        rect = surface.get_rect()
        rect.center = self.center

        l_error = Label(surface, "Error", self.textsize, (0, 0), "topleft",
                        bR=1, tc=self.textcolor, fh=self.textsize, to=(7, 1))
        l_error_name = Label(surface, error_message, self.textsize,
                             (surface.get_width() // 2, int(self.textsize * 1.7)),
                             "midtop", tc=self.textcolor)
        b_okay = Button(
            surface, "OK", self.textsize, (surface.get_width() - 7, surface.get_height() - 7),
            "bottomright", tc=self.textcolor, bgc=self.backgroundcolor2, hl=True, xad=5, yad=3, bR=1, bw=2,
            br=1)

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            surface.fill(self.backgroundcolor2)
            l_error.draw()
            l_error_name.draw()
            b_okay.draw()
            pygame.draw.line(surface, (0, 0, 0), (0, self.textsize), (self.dimensions[0], self.textsize), 3)
            self.blitting_surface.blit(surface, rect)
            pygame.draw.rect(self.blitting_surface, (0, 0, 0), rect, 3, 1, 1, 1, 1)

            if b_okay.update(mouse_events, offset=rect.topleft):
                run = False

            pygame.display.flip()
            self.pygame_clock.tick(self.fps)

    def ask_filename(self, starting_path, required_ending: str = None, dim_background: bool = True) -> str:
        if not os.path.exists(starting_path):
            raise Exception(f"Given path does not exist. ({starting_path})")
        if required_ending != None:
            assert type(required_ending) == str, f"invalid argument for 'required_ending': {required_ending}"

        if dim_background:
            self.blitting_surface.fill([60 for i in range(3)], special_flags=pygame.BLEND_MULT)

        current_path = starting_path
        old_path = ""
        directory_scan: list

        buttons_list = []

        scroll = 0
        max_scroll = 0
        old_selected = ["", ""]  # [path, end_of_path]
        selected = ["", ""]
        self.l_selected_name.update_text("")

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                elif max_scroll > 0 and event.type == pygame.MOUSEWHEEL:
                    scroll = max(min(max_scroll, scroll + event.y*-1*int(self.textsize*1.5)), 0)

            # update
            if current_path != old_path or selected != old_selected:
                try:
                    directory_scan = os.scandir(current_path)

                    self.l_path.update_text(current_path.replace("\\", " > "))
                    old_path = current_path
                    buttons_list = []
                    MAX_ELEMENTS = 80
                    length = min(len(os.listdir(current_path)), MAX_ELEMENTS) * self.textsize
                    dir_surf = pygame.Surface((self.dimensions[0], length))
                    for count, path in enumerate(directory_scan):
                        if count == MAX_ELEMENTS:
                            break
                        new_path = os.path.join(current_path, path)
                        if os.path.isdir(new_path):
                            role = "dir"
                        elif os.path.isfile(new_path):
                            role = "file"
                        else:
                            raise Exception(f"what is this file? ({new_path})")
                        if path.name == selected[1]:
                            bw = 3
                        else:
                            bw = 0
                        buttons_list.append(FileDialogElement(dir_surf, path.name, count, role, self.topleft_pos,
                                                              self.dimensions, self.textsize, self.textcolor, self.backgroundcolor2, bw))
                    if selected == old_selected:
                        scroll = 0
                        max_scroll = length - (self.dimensions[1]-self.textsize-int(self.textsize*1.5))
                except PermissionError:
                    self.error("Permission denied.")
                    current_path = os.path.split(current_path)[0]

            if selected != old_selected:
                old_selected = selected[:]
                self.l_selected_name.update_text(selected[1])

            # updating each button
            for element in buttons_list:
                if element.update(
                    mouse_events, _offset=(self.topleft_pos[0],
                                           self.topleft_pos[1] + self.textsize + scroll)):
                    if element.role == "dir":
                        current_path = os.path.join(current_path, element.name)
                    elif element.role == "file":
                        if required_ending == None or required_ending != None and element.name.endswith(
                                required_ending):
                            selected[0] = os.path.join(current_path, element.name)
                            selected[1] = element.name

            if self.b_cancel.update(mouse_events, offset=self.topleft_pos):
                return None

            if self.b_back.update(mouse_events, offset=self.topleft_pos):
                current_path = os.path.split(current_path)[0]

            if self.b_open.update(mouse_events, offset=self.topleft_pos):
                if selected[0] != "":
                    return selected[0]
                else:
                    return None
            
            if required_ending != None and self.b_req_ending.update(mouse_events, offset=self.topleft_pos):
                self.messagebox.show_message(f"Required file ending: '{required_ending}'", False)

            # ? DRAWING ? #
            self.surface.fill(self.backgroundcolor1)

            # drawing on dir_surf
            for button in buttons_list:
                button.draw()
            self.surface.blit(dir_surf, (0, self.textsize-scroll))
            self.l_path.draw()
            self.b_back.draw()
            pygame.draw.rect(
                self.surface, (0, 0, 0),
                (0, self.textsize, self.dimensions[0],
                 self.dimensions[1] - self.textsize - int(self.textsize * 1.5)),
                1)

            # bottom part
            pygame.draw.rect(
                self.surface, self.backgroundcolor1,
                (0, self.dimensions[1] - int(self.textsize * 1.5),
                 self.dimensions[0],
                 int(self.textsize * 1.5)))
            pygame.draw.rect(
                self.surface, (0, 0, 0),
                (0, self.dimensions[1] - int(self.textsize * 1.5),
                 self.dimensions[0],
                 int(self.textsize * 1.5)),
                1)
            self.b_cancel.draw()
            self.l_selected.draw()
            self.l_selected_name.draw()
            self.b_open.draw()
            if required_ending != None:
                self.b_req_ending.draw()

            # at the end
            self.blitting_surface.blit(self.surface, self.topleft_pos)
            pygame.draw.rect(
                self.blitting_surface, (0, 0, 0),
                (self.topleft_pos[0] - 5, self.topleft_pos[1] - 5, self.dimensions[0] + 10, self.dimensions
                 [1] + 10),
                5, 1, 1, 1, 1)

            pygame.display.flip()
            self.pygame_clock.tick(self.fps)

    def ask_foldername(self, starting_path, dim_background: bool = True) -> str:
        raise Exception("not yet implemented")
