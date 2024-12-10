import pygame
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        """
        call super().__init__() right after creating self.image and self.rect

        IMPORTANT: images for animations must be a dict like:
        {
            left: img_left,
            right: img_right
        }

        self.__action__ will be priorized over self.__looping_action_   #! (is it?)

        use PygameXtras.Spritesheet for images (in self.add_action(...))
        """
        super().__init__()

        self.__entity_pos__ = [0, 0]
        self.rect = pygame.Rect(
            0, 0, self.rect.width, self.rect.height)

        self.__hitbox_data__ = (0, 0, self.rect.width, self.rect.height)
        self.__initial_hitbox_data__ = (0, 0, self.rect.width,
                                        self.rect.height)
        self.__hitbox_rect__ = pygame.Rect(
            0, 0, self.rect.width, self.rect.height)

        self.__game_map_tiles__ = None
        self.__do_tile_collision__ = False
        self.__tile_sidelength__ = None
        self.__is_platformer__ = False
        self.__is_touching_ground_precision__ = 0

        # ? idea: a dict that contains what happens during an action (eg "launch rocket at frame 7" or "die at frame 15")
        # ? the dict stores strings that look like functions and that can be called with "exec()"

        # a dict with useful data, such as "has moved", "which direction moved", "jumped", old_center, ...
        # updates every frame so all the data is accessible
        self.__data__ = {
            "old_center": (0, 0),
            "center": (0, 0),
            "last_movement": (0, 0),
            "current_movement": (0, 0),
            "has_moved": False,
            "has_moved_left": False,
            "has_moved_up": False,
            "has_moved_right": False,
            "has_moved_down": False,
            "direction": "right",
            "width": self.rect.width,
            "height": self.rect.height,
            "rect": self.rect,

            # for platformers
            "is_touching_ground": False
        }
        self.__data__["is_touching_ground_list"] = [False for i in range(
            self.__is_touching_ground_precision__)]  # [new, old, older, ...]

        # checking the init-method
        self.__init_check__ = {
            "self.add_action": False,
            "self.set_looping_action": False,
            "self.set_speed": False,
            "self.set_tile_collision": False
        }
        self.__init_check_success__ = False

        # contains the images, that are blitted next
        self.__animation_sequence__ = []

        # current 'action', change with self.__set_action__()
        self.__action__ = None
        self.__looping_action__ = None
        self.__current_action__ = None
        self.__actions__ = {}
        self.__action_run_timer__ = 0

        # additional data for movement
        self.__entity_speed__ = 0
        self.__movement_vector__ = [0, 0]
        self.__constant_movement_vector__ = [0, 0]
        self.__constant_movement_max_vector__ = [0, 0]
        self.__constant_movement_initial_vector__ = [0, 0]
        self.__constant_movement_affection__ = False
        self.__knockback_vector__ = [0, 0]
        self.__knockback_resistance__ = 1
        self.__automatic_direction_control__ = True
        self.__direction_factor__ = 1  # -1 == left; 1 == right
        self.__rotation__ = 0
        self.__rotation_point_right__ = (0, 0)
        self.__rotation_point_left__ = (0, 0)
        self.__temp_collision_rects__ = []

    def __get_distance__(self, xy1, xy2, digits_after_comma=None):
        x1, y1 = xy1[0], xy1[1]
        x2, y2 = xy2[0], xy2[1]
        if digits_after_comma == None:
            return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
        else:
            return self.round_half_up(math.sqrt(((x2-x1)**2)+((y2-y1)**2)), digits_after_comma)

    def __get_angle_between_points__(self, xy1, xy2):
        vect = pygame.math.Vector2(xy2[0]-xy1[0], xy2[1]-xy1[1])
        if vect.length() != 0:
            vect.normalize()
        cos = self.__rhu__(vect.y, 2)
        deg_cos = int(math.degrees(math.acos(vect.x)))
        if cos <= 0:
            return deg_cos
        else:
            return 180 + (180-deg_cos)

    def __get_normalized_vector_between_points__(self, xy1, xy2):
        return pygame.math.Vector2(xy2[0]-xy1[0], xy2[1]-xy1[1]).normalize()

    def __get_normalized_vector_from_angle__(self, angle):
        vect = pygame.Vector2(self.__rhu__(math.cos(math.radians(
            angle)), 3), self.__rhu__(math.sin(math.radians(angle)), 3))
        return vect.normalize()

    def __rhu__(self, n, decimals=0):
        """ -> round_half_up """
        multiplier = 10 ** decimals
        return math.floor(n*multiplier + 0.5) / multiplier

    def __reset_constant_movement_vector__(self):
        self.__constant_movement_vector__ = self.__constant_movement_initial_vector__[:]

    def __move__(self):

        # x movement ##########################################################################################

        if self.__knockback_vector__[0] != 0:
            self.__movement_vector__[0] += self.__knockback_vector__[0]
            self.__knockback_vector__[0] = int(self.__knockback_vector__[0] / self.__knockback_resistance__)

        if self.__constant_movement_affection__:
            self.__movement_vector__[0] += self.__constant_movement_vector__[0]

            if (self.__movement_vector__[0] > 0 and self.__constant_movement_vector__[0] > 0) or \
                    (self.__movement_vector__[0] < 0 and self.__constant_movement_vector__[0] < 0):
                self.__constant_movement_vector__[0] += self.__constant_movement_initial_vector__[0]
            else:
                self.__constant_movement_vector__[0] = self.__constant_movement_initial_vector__[0]

            # limits the vector to its maximum value
            if self.__constant_movement_max_vector__[0] > 0:
                if self.__constant_movement_vector__[0] > self.__constant_movement_max_vector__[0]:
                    self.__constant_movement_vector__[0] = self.__constant_movement_max_vector__[0]
            elif self.__constant_movement_max_vector__[0] < 0:
                if self.__constant_movement_vector__[0] < self.__constant_movement_max_vector__[0]:
                    self.__constant_movement_vector__[0] = self.__constant_movement_max_vector__[0]

        self.rect.x += self.__movement_vector__[0]
        self.__adjust_hitbox_position__()
        if self.__do_tile_collision__:
            surrounding_tiles = self.__get_tiles_within_radius__(
                self.__game_map_tiles__, self.get_pos_factor(1/self.__tile_sidelength__))
            if len(self.__temp_collision_rects__) > 0:
                surrounding_tiles += self.__temp_collision_rects__
            collided_tiles = self.__tile_collision_test__(surrounding_tiles)
            for tile in collided_tiles:
                if self.__movement_vector__[0] > 0:
                    self.__hitbox_rect__.right = tile.left
                elif self.__movement_vector__[0] < 0:
                    self.__hitbox_rect__.left = tile.right
                self.__adjust_rect_position__()
                self.__constant_movement_vector__[0] = self.__constant_movement_initial_vector__[0]
                self.__knockback_vector__[0] = 0
        self.__movement_vector__[0] = 0

        # y movement ##########################################################################################

        if self.__knockback_vector__[1] != 0:
            self.__movement_vector__[1] += self.__knockback_vector__[1]
            self.__knockback_vector__[1] = int(self.__knockback_vector__[1] / self.__knockback_resistance__)

        if self.__constant_movement_affection__:
            self.__movement_vector__[1] += self.__constant_movement_vector__[1]

            if (self.__movement_vector__[1] > 0 and self.__constant_movement_vector__[1] > 0) or \
                    (self.__movement_vector__[1] < 0 and self.__constant_movement_vector__[1] < 0):
                self.__constant_movement_vector__[1] += self.__constant_movement_initial_vector__[1]
            else:
                self.__constant_movement_vector__[1] = self.__constant_movement_initial_vector__[1]

            # limits the vector to its maximum value
            if self.__constant_movement_max_vector__[1] > 0:
                if self.__constant_movement_vector__[1] > self.__constant_movement_max_vector__[1]:
                    self.__constant_movement_vector__[1] = self.__constant_movement_max_vector__[1]
            elif self.__constant_movement_max_vector__[1] < 0:
                if self.__constant_movement_vector__[1] < self.__constant_movement_max_vector__[1]:
                    self.__constant_movement_vector__[1] = self.__constant_movement_max_vector__[1]

        if self.__is_platformer__:
            # moving the list by one
            for i in range(self.__is_touching_ground_precision__-1, 0, -1):
                self.__data__["is_touching_ground_list"][i] = self.__data__["is_touching_ground_list"][i-1]

            self.__data__["is_touching_ground_list"][0] = False
            old_y = self.rect.y
        self.rect.y += self.__movement_vector__[1]
        self.__adjust_hitbox_position__()
        if self.__do_tile_collision__:
            surrounding_tiles = self.__get_tiles_within_radius__(
                self.__game_map_tiles__, self.get_pos_factor(1/self.__tile_sidelength__))
            if len(self.__temp_collision_rects__) > 0:
                surrounding_tiles += self.__temp_collision_rects__
            collided_tiles = self.__tile_collision_test__(surrounding_tiles)
            for tile in collided_tiles:
                if self.__movement_vector__[1] > 0:
                    self.__hitbox_rect__.bottom = tile.top
                elif self.__movement_vector__[1] < 0:
                    self.__hitbox_rect__.top = tile.bottom
                self.__adjust_rect_position__()
                self.__constant_movement_vector__[1] = self.__constant_movement_initial_vector__[1]
                self.__knockback_vector__[1] = 0

        if self.__is_platformer__:
            if old_y == self.rect.y:
                self.__data__["is_touching_ground_list"][0] = True
        self.__movement_vector__[1] = 0

        self.__temp_collision_rects__ = []

    def __update_data__(self):
        self.__data__["old_center"] = self.__data__["center"]
        self.__data__["center"] = self.get_pos()
        self.__data__["last_movement"] = (
            self.__data__["center"][0] - self.__data__["old_center"][0],
            self.__data__["center"][1] - self.__data__["old_center"][1]
        )
        self.__data__["has_moved_left"] = self.__data__["last_movement"][0] < 0
        self.__data__["has_moved_right"] = self.__data__["last_movement"][0] > 0
        self.__data__["has_moved_up"] = self.__data__["last_movement"][1] < 0
        self.__data__["has_moved_down"] = self.__data__["last_movement"][1] > 0
        self.__data__["has_moved"] = any(
            [self.__data__["has_moved_" + direction]
             for direction in "left,up,right,down".split(",")])
        if self.__automatic_direction_control__ and self.__data__["has_moved"]:
            if self.__data__["has_moved_left"]:
                self.__data__["direction"] = "left"
                self.__direction_factor__ = -1
            elif self.__data__["has_moved_right"]:
                self.__data__["direction"] = "right"
                self.__direction_factor__ = 1
        self.__data__["is_touching_ground"] = all(self.__data__["is_touching_ground_list"])

        # updating global position and position on the screen
        self.__entity_pos__ = list(self.get_pos())
        self.rect.center = self.get_pos()

    def __update_image__(self):

        self.__action_run_timer__ += 1

        static_image = False  # ! not tested (15.2.2022, 11:57)
        if self.__animation_sequence__ == []:
            if len(self.__actions__[self.__looping_action__]["frames"]) == 1:
                static_image = True
                next_image = self.__actions__[
                    self.__looping_action__]["frames"][0][
                    self.__data__["direction"]]
            else:
                self.__animation_sequence__ += self.__actions__[self.__looping_action__]["frames"]
                self.__action_run_timer__ = 0
                self.__current_action__ = self.__looping_action__

        if not static_image:
            try:
                next_image = self.__animation_sequence__[0][self.__data__["direction"]]
            except TypeError as e:
                raise Exception(
                    "At least some elements of the action '" + self.__current_action__ +
                    "' are not formatted correctly. Make sure that all elements are in the form of a dict: \n{'left': <image_left>, 'right': <image_right>}")

        if self.__rotation__ != 0:  # ! not tested (15.2.2022, 11:47)
            blue_vect = pygame.Vector2(
                self.__rotation_point_right__[0] * self.get_direction_factor(),
                self.__rotation_point_right__[1])
            saved_center = pygame.Vector2(
                self.rect.center) + pygame.Vector2(
                self.__rotation_point_right__[0] * self.get_direction_factor(),
                self.__rotation_point_right__[1])
            new_vect = blue_vect.rotate(-self.__rotation__ * self.get_direction_factor())
            next_image = pygame.transform.rotate(next_image, self.__rotation__ * self.get_direction_factor())
            self.rect = self.image.get_rect(center=saved_center - new_vect)

        # ? check hitbox stuff
        # ? check pygame.mask

        self.image = next_image

        if not static_image:
            del self.__animation_sequence__[0]

    def __execute_action_methods__(self):
        if self.__action_run_timer__ in self.__actions__[
                self.__current_action__]["methods_to_execute"].keys():
            string = "self." + self.__actions__[
                self.__current_action__]["methods_to_execute"][
                self.__action_run_timer__]
            try:
                exec(string)
            except Exception as e:
                raise Exception(
                    f"An error occurred while executing a method from the action '{self.__current_action__}':\n\n{e}")

    def __tile_collision_test__(self, tiles: list) -> list:
        """ not very precise, should only be used for movement """
        collisions = []
        for tile in tiles:
            if self.__hitbox_rect__.colliderect(tile):
                collisions.append(tile)
        return collisions

    def __get_tiles_within_radius__(self, tiles_in_2d: list[list], xy: tuple, radius: int = 2) -> list:
        """ gets awfully inefficient with increasing radius, but 2 should be sufficient for everything """
        # automatically avoids crossing game borders
        tiles = []
        for x in range(max(int(xy[0])-radius, 0),
                       min(int(xy[0])+radius, len(tiles_in_2d))):
            for y in range(max(int(xy[1])-radius, 0),
                           min(int(xy[1])+radius, len(tiles_in_2d[0]))):
                if tiles_in_2d[x][y] != 0:
                    tiles.append(tiles_in_2d[x][y])
        return tiles

    def __adjust_hitbox_position__(self):
        self.__hitbox_rect__.topleft = (
            self.rect.topleft[0] + self.__hitbox_data__[0],
            self.rect.topleft[1] + self.__hitbox_data__[1])

    def __adjust_rect_position__(self):
        self.rect.topleft = (
            self.__hitbox_rect__.topleft[0] - self.__hitbox_data__[0],
            self.__hitbox_rect__.topleft[1] - self.__hitbox_data__[1])

    def __init_check_func__(self):
        if not all(self.__init_check__.values()):
            string1 = [f"{k}: {v}" for k, v in self.__init_check__.items()]
            string2 = "\n".join(string1)
            raise Exception(f"Not all necessary init-methods called:\n\n{string2}")

    def internal_update(self):
        """ needs to be called at the end of the entities .move method \n
            methods can also be called individually """
        if self.__init_check_success__ == False:
            self.__init_check_func__()
            self.__init_check_success__ = True

        self.__move__()
        self.__update_data__()
        self.__update_image__()
        self.__execute_action_methods__()

    def add_action(self, name: str, image_dicts: list, frames_per_image: list[int],
                   methods_to_execute: dict[str: str] = None):
        """
        image_dicts: dicts of image ("left":..., "right":...)
        frames_per_image can be either a list or an int \n
        adds an action to self.__actions__ in the following form:
        {
            "<action_name>": {
                "frames": ["<frame0>", "<frame1>", "<frame2>", ...],
                "methods_to_execute": {
                    "<frame>": "self.method(*args)",
                    ...
                }
            }
        }
        """
        if type(frames_per_image) == list:
            assert len(image_dicts) == len(
                frames_per_image), "received lists of different lengths"

        # creating list
        frame_sequence = []
        if type(frames_per_image) == list:
            for image, count in zip(image_dicts, frames_per_image):
                for i in range(count):
                    frame_sequence.append(image)
        elif type(frames_per_image) == int:
            for image in image_dicts:
                for i in range(frames_per_image):
                    frame_sequence.append(image)

        # adding "methods_to_execute" functionality
        self._layer = None  # dont ask why this is here, but it crashes if it isnt
        if methods_to_execute != None:
            method_list = [func for func in dir(self) if callable(
                getattr(self, func)) and not func.startswith("__")]  # "set_action", ...
            for k, v in methods_to_execute.items():
                if type(k) != int:
                    raise ValueError(
                        f"Error in 'methods_to_execute': '{k}' is not a number")
                if v.split("(")[0] not in method_list:  # ) avoid brackets changing colors
                    # ! not sure if this works as intended
                    raise Exception(
                        f"Error in 'methods_to_execute': '{v.split('(')[0]}' is not a valid method")  # )
        else:
            methods_to_execute = {}

        self.__actions__[name] = {
            "frames": frame_sequence,
            "methods_to_execute": methods_to_execute
        }
        self.__init_check__["self.add_action"] = True

    def set_looping_action(self, action: str, cancel_other_action: bool = True) -> None:
        assert action in self.__actions__.keys(), f"unknown action: '{action}'"
        if cancel_other_action and self.__looping_action__ != action:
            self.__animation_sequence__ = []
            self.__animation_sequence__ += self.__actions__[action]["frames"]
            self.__action_run_timer__ = 0
            self.__current_action__ = action
        self.__looping_action__ = action
        self.__init_check__["self.set_looping_action"] = True

    def set_action(self, action: str, cancel_other_action: bool = True) -> None:
        assert action in self.__actions__.keys(), f"unknown action: '{action}'"
        if cancel_other_action and self.__current_action__ != action:
            self.__animation_sequence__ = []
            self.__animation_sequence__ += self.__actions__[action]["frames"]
            self.__action_run_timer__ = 0
            self.__current_action__ = action
        self.__action__ = action

    def get_data(self, name: str):
        """ access useful data like "has_moved", "last_movement", etc. """
        assert name in self.__data__.keys(), f"no entry in __data__ for '{name}'"
        return self.__data__[name]

    def set_speed(self, speed: float):
        """ needs to be called in the init-method """
        self.__entity_speed__ = speed
        self.__init_check__["self.set_speed"] = True

    def get_speed(self):
        return self.__entity_speed__

    def move_right(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[0] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[0] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_left(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[0] -= self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[0] -= custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_up(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[1] -= self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[1] -= custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_down(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[1] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[1] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_horizontal(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[0] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[0] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def move_vertical(self, custom_value=None):
        if custom_value == 0:
            return
        elif custom_value == None:
            self.__movement_vector__[1] += self.__entity_speed__
        elif type(custom_value) in [int, float]:
            self.__movement_vector__[1] += custom_value
        else:
            raise TypeError(f"Incorrect input type for 'custom_value': {custom_value}")

    def get_pos(self, reference_point="center"):
        """ uses pixel """
        assert reference_point in ["topleft", "top", "topright",
                                   "left", "center", "centerx", "centery", "right",
                                   "bottomleft", "bottom", "bottomright"]

        if reference_point == "topleft":
            return self.rect.topleft
        elif reference_point == "top":
            return self.rect.top
        elif reference_point == "topright":
            return self.rect.topright
        elif reference_point == "left":
            return self.rect.left
        elif reference_point == "center":
            return self.rect.center
        elif reference_point == "centerx":
            return self.rect.centerx
        elif reference_point == "centery":
            return self.rect.centery
        elif reference_point == "right":
            return self.rect.right
        elif reference_point == "bottomleft":
            return self.rect.bottomleft
        elif reference_point == "bottom":
            return self.rect.bottom
        elif reference_point == "bottomright":
            return self.rect.bottomright

    def get_pos_factor(self, factor, reference_point="center", decimals=0):
        """ uses the coordinate system """
        assert reference_point in ["topleft", "top", "topright",
                                   "left", "center", "centerx", "centery", "right",
                                   "bottomleft", "bottom", "bottomright"]

        if reference_point == "topleft":
            return self.__rhu__(
                self.rect.topleft[0] * factor, decimals), self.__rhu__(
                self.rect.topleft[1],
                decimals)
        elif reference_point == "top":
            return self.__rhu__(self.rect.top * factor, decimals)
        elif reference_point == "topright":
            return self.__rhu__(
                self.rect.topright[0] * factor, decimals), self.__rhu__(
                self.rect.topright[1] * factor, decimals)
        elif reference_point == "left":
            return self.__rhu__(self.rect.left * factor, decimals)
        elif reference_point == "center":
            return self.__rhu__(
                self.rect.center[0] * factor, decimals), self.__rhu__(
                self.rect.center[1] * factor, decimals)
        elif reference_point == "centerx":
            return self.__rhu__(self.rect.centerx * factor, decimals)
        elif reference_point == "centery":
            return self.__rhu__(self.rect.centery * factor, decimals)
        elif reference_point == "right":
            return self.__rhu__(self.rect.right * factor, decimals)
        elif reference_point == "bottomleft":
            return self.__rhu__(
                self.rect.bottomleft[0] * factor, decimals), self.__rhu__(
                self.rect.bottomleft[1] * factor, decimals)
        elif reference_point == "bottom":
            return self.__rhu__(self.rect.bottom * factor, decimals)
        elif reference_point == "bottomright":
            return self.__rhu__(
                self.rect.bottomright[0] * factor, decimals), self.__rhu__(
                self.rect.bottomright[1] * factor, decimals)

    def set_pos(self, xy, reference_point="center"):
        """ uses pixel \n 'xy' can be either a tuple or an integer, depending on 'reference_point' """
        assert type(xy) in [tuple, list, int, pygame.Vector2]
        assert type(reference_point) == str
        if reference_point in ["topleft", "topright", "center", "bottomleft", "bottomright"]:
            assert type(xy) in [
                tuple, list, int, pygame.Vector2], f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"
            assert len(xy) == 2, f"invalid length of tuple <xy> ({xy})"
        elif reference_point in ["top", "left", "centerx", "centery", "right", "bottom"]:
            assert type(
                xy) == int, f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"

        if reference_point == "topleft":
            self.rect.topleft = xy
        elif reference_point == "top":
            self.rect.top = xy
        elif reference_point == "topright":
            self.rect.topright = xy
        elif reference_point == "left":
            self.rect.left = xy
        elif reference_point == "center":
            self.rect.center = xy
        elif reference_point == "centerx":
            self.rect.centerx = xy
        elif reference_point == "centery":
            self.rect.centery = xy
        elif reference_point == "right":
            self.rect.right = xy
        elif reference_point == "bottomleft":
            self.rect.bottomleft = xy
        elif reference_point == "bottom":
            self.rect.bottom = xy
        elif reference_point == "bottomright":
            self.rect.bottomright = xy

        self.__entity_pos__ = list(self.rect.center)

    def set_pos_factor(self, xy, factor: int, reference_point="center"):
        """ uses the coordinate system if <factor> == self.__tile_sidelength__ \n <xy> can be either a tuple or an integer, depending on <reference_point> """
        assert type(xy) in [tuple, list, int]
        assert type(reference_point) == str
        # <factor> could (and should!) be automated with the side length of the current levels tiles
        if reference_point in ["topleft", "topright", "center", "bottomleft", "bottomright"]:
            assert type(xy) in [
                list, tuple], f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"
            assert len(xy) == 2, f"invalid length of tuple <xy> ({xy})"
        elif reference_point in ["top", "left", "centerx", "centery", "right", "bottom"]:
            assert type(
                xy) == int, f"invalid combination of <xy> ({xy}) and <reference_point> ({reference_point})"

        assert type(factor) == int, f"invalid argument for <factor> ({factor}), integer required"

        if reference_point == "topleft":
            self.rect.topleft = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "top":
            self.rect.top = xy * factor
        elif reference_point == "topright":
            self.rect.topright = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "left":
            self.rect.left = xy * factor
        elif reference_point == "center":
            self.rect.center = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "centerx":
            self.rect.centerx = xy * factor
        elif reference_point == "centery":
            self.rect.centery = xy * factor
        elif reference_point == "right":
            self.rect.right = xy * factor
        elif reference_point == "bottomleft":
            self.rect.bottomleft = (xy[0] * factor, xy[1] * factor)
        elif reference_point == "bottom":
            self.rect.bottom = xy * factor
        elif reference_point == "bottomright":
            self.rect.bottomright = (xy[0] * factor, xy[1] * factor)

        self.__entity_pos__ = list(self.rect.center)

    def move_to(self, xy, reference_point="center"):
        """ same as self.set_pos() """
        self.set_pos(xy, reference_point)

    def set_game_map_tiles(self, tiles: list[list], do_tile_collision: bool = True):
        """ <tiles> must be a 2d list of pygame.Rect objects """
        assert type(tiles) == list, "failed to load map tiles"
        assert type(tiles[0]) == list, "failed to load map tiles"
        assert type(do_tile_collision) == bool
        self.__game_map_tiles__ = tiles
        self.__do_tile_collision__ = do_tile_collision

    def set_tile_collision(self, boolean: bool, tile_sidelength: int = None):
        assert type(boolean) == bool
        self.__do_tile_collision__ = boolean
        if boolean == True:
            assert tile_sidelength != None, "if tile_collision should be done, tile_sidelength needs to be set"
            assert type(tile_sidelength) == int
            assert tile_sidelength >= 8, "tile_sidelength must be greater or equal to 8"
            self.set_tile_sidelength(tile_sidelength)
        self.__init_check__["self.set_tile_collision"] = True

    def get_tile_sidelength(self):
        return self.__tile_sidelength__

    def set_constant_movement(self, vector2: tuple, max_vector2: tuple,
                              set_constant_movement_affection: bool = True):
        assert type(vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({vector2})"
        assert len(vector2) == 2, f"invalid vector ({vector2})"
        assert type(max_vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({max_vector2})"
        assert len(max_vector2) == 2, f"invalid vector ({max_vector2})"
        assert type(set_constant_movement_affection) == bool

        self.__constant_movement_vector__ = list(vector2)
        self.__constant_movement_max_vector__ = list(max_vector2)
        self.__constant_movement_initial_vector__ = list(vector2)
        self.set_constant_movement_affection(set_constant_movement_affection)

    def get_constant_movement(self):
        return self.__constant_movement_vector__

    def set_constant_movement_affection(self, boolean):
        assert type(boolean) == bool
        self.__constant_movement_affection__ = boolean

    def get_constant_movement_affection(self):
        return self.__constant_movement_affection__

    def set_custom_hitbox(self, rect: tuple[int, int, int, int]):
        """ sets a custom hitbox for tile collision """
        assert type(rect) in [list, tuple]
        assert len(rect) == 4

        self.__hitbox_data__ = rect
        self.__hitbox_rect__ = pygame.Rect(*rect)
        self.__adjust_hitbox_position__()

    def get_hitbox(self):
        return self.__hitbox_rect__

    def reset_hitbox(self):
        """ resets the hitbox to default (the entities 'rect') """
        self.__hitbox_data__ = self.__initial_hitbox_data__
        self.__hitbox_rect__ = pygame.Rect(*self.__hitbox_data__)
        self.__adjust_hitbox_position__()

    def set_knockback_resistance(self, knockback_resistance: float):
        """ sets the number the knockback vector will be divided by each frame, must be between 1 and 1.2 """
        assert 1 < knockback_resistance <= 1.2, "knockback_resistance must be between 1 and 1.2"
        self.__knockback_resistance__ = knockback_resistance

    def get_knockback_resistance(self):
        """ returns the number the knockback vector gets divided by """
        return self.__knockback_resistance__

    def set_knockback(self, vector2: tuple, reset_constant_movement: bool = True):
        """ applies knockback to the entity """
        assert type(vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({vector2})"
        assert len(vector2) == 2, f"invalid vector ({vector2})"
        assert self.__knockback_resistance__ != 1, "knockback_resistance must be between 1 and 1.2"

        self.__knockback_vector__ = list(vector2)
        if reset_constant_movement:
            self.__reset_constant_movement_vector__()

    def add_knockback(self, vector2: tuple):
        """ applies additional knockback on top of the current one to the entity """
        assert type(vector2) in [list, tuple, pygame.Vector2], f"invalid vector ({vector2})"
        assert len(vector2) == 2, f"invalid vector ({vector2})"
        assert self.__knockback_resistance__ != 1, "knockback_resistance must be between 1 and 1.2 "

        self.__knockback_vector__ = [
            self.__knockback_vector__[0] + vector2[0],
            self.__knockback_vector__[1] + vector2[1]]

    def move_at_angle(self, angle, custom_speed=None):
        """ 0 degrees = right | then clockwise """
        temp_vect = self.__get_normalized_vector_from_angle__(angle)
        if custom_speed != None:
            vect = temp_vect * custom_speed
        else:
            vect = temp_vect * self.__entity_speed__

        self.__movement_vector__[0] += vect[0]
        self.__movement_vector__[1] += vect[1]

    def set_tile_sidelength(self, tile_sidelength: int):
        assert type(tile_sidelength) == int
        self.__tile_sidelength__ = tile_sidelength

    def set_platformer_status(self, is_platformer: bool, set_touching_ground_precision: int = 3):
        """ decide whether the game is a platformer or not (enables some platformer features) """
        assert type(is_platformer) == bool
        self.__is_platformer__ = is_platformer
        self.set_touching_ground_precision(set_touching_ground_precision)

    def set_touching_ground_precision(self, precision: int):
        """ higher precision means that the ground will be detected with more certainty, 
        but it takes longer to realize that the entity is not touching the ground anymore...
        this might result in the player being able to jump again mid-air \n
        note: \n
        automatically calls self.set_platformer_status
        1 <= precision <= 6 | recommended value: 3 """
        assert type(precision) == int
        assert 1 <= precision <= 6
        self.__is_platformer__ = True
        self.__is_touching_ground_precision__ = precision
        self.__data__["is_touching_ground_list"] = [False for i in range(
            self.__is_touching_ground_precision__)]  # [new, old, older, ...]

    def set_automatic_direction_control(self, boolean: bool):
        """ automatically sets the direction of the entity based on its movement """
        assert type(boolean) == bool
        self.__automatic_direction_control__ = boolean

    def set_direction(self, direction):
        """ <direction> can be either "left" and "right" or -1 and 1 """
        assert direction in ["left", "right", -1, 1]
        if direction in ["left", -1]:
            self.__data__["direction"] = "left"
            self.__direction_factor__ = -1
        elif direction in ["right", 1]:
            self.__data__["direction"] = "right"
            self.__direction_factor__ = 1

    def get_direction(self):
        return self.get_data("direction")

    def get_direction_factor(self):
        return self.__direction_factor__

    def set_rotation_point_vector(self, xy: tuple):
        """ sets the point the entity rotates around; vector starts at the center of the entity; \n
            default = center; IMPORTANT: configure for entity facing right """
        assert type(xy) in [tuple, list, pygame.Vector2]
        self.__rotation_point_right__ = tuple(xy)
        self.__rotation_point_left__ = (xy[0]*-1, xy[1])

    def get_rotation_point_right(self) -> tuple:
        """ returns the point the entity rotates around when it is facing right """
        return self.__rotation_point_right__

    def get_rotation_point_left(self) -> tuple:
        """ returns the point the entity rotates around when it is facing left """
        return self.__rotation_point_left__

    def set_rotation(self, angle):
        """ sets the entities rotation to the given angle """
        assert type(angle) in [int, float]
        self.__rotation__ = int(angle) % 360

    def get_rotation(self):
        """ returns the current rotation """
        return self.__rotation__

    def do_platformer_jump(self, factor: float):
        self.__constant_movement_vector__[1] = factor

    def add_temp_collision_rects(self, rects: list):
        """ adds a list of rectangles to the collision tiles list for ONE iteration """
        assert type(rects) in [tuple, list]
        for item in rects:
            assert type(item) == pygame.Rect
        self.__temp_collision_rects__ = rects
