import pygame
import pygame._sdl2.controller as controller

controller.init()


class PSController:
    cross: bool
    circle: bool
    square: bool
    triangle: bool
    share: bool
    ps: bool
    options: bool
    l1: bool
    l3: bool
    r1: bool
    r3: bool
    arrow_up: bool
    arrow_down: bool
    arrow_left: bool
    arrow_right: bool
    touch_pad: bool

    def __init__(self, joystick_num, threshold: float = 0.08):
        self.__joystick_num = joystick_num
        self.__threshold = threshold**2
        self.__controller = controller.Controller(joystick_num)

    def update(self):
        self.cross = self.__controller.get_button(0)
        self.circle = self.__controller.get_button(1)
        self.square = self.__controller.get_button(2)
        self.triangle = self.__controller.get_button(3)
        self.share = self.__controller.get_button(4)
        self.ps = self.__controller.get_button(5)
        self.options = self.__controller.get_button(6)
        self.l1 = self.__controller.get_button(9)
        self.l3 = self.__controller.get_button(7)
        self.r1 = self.__controller.get_button(10)
        self.r3 = self.__controller.get_button(8)
        self.arrow_up = self.__controller.get_button(11)
        self.arrow_down = self.__controller.get_button(12)
        self.arrow_left = self.__controller.get_button(13)
        self.arrow_right = self.__controller.get_button(14)
        self.touch_pad = self.__controller.get_button(20)  # only works on windows

    def get_left_stick(self) -> tuple[float, float]:
        """returns a tuple representing the position of the left joystick"""
        vect = pygame.Vector2(
            (
                max(-1, self.__controller.get_axis(0) / 32767),
                max(-1, self.__controller.get_axis(1) / 32767),
            )
        )
        if vect.length_squared() < self.__threshold:
            return (0, 0)
        else:
            return (vect.x, vect.y)

    def get_right_stick(self) -> tuple[float, float]:
        """returns a tuple representing the position of the right joystick"""
        vect = pygame.Vector2(
            (
                max(-1, self.__controller.get_axis(2) / 32767),
                max(-1, self.__controller.get_axis(3) / 32767),
            )
        )
        if vect.length_squared() < self.__threshold:
            return (0, 0)
        else:
            return (vect.x, vect.y)

    def get_l2(self):
        return self.__controller.get_axis(4) / 32767

    def get_r2(self):
        return self.__controller.get_axis(5) / 32767
