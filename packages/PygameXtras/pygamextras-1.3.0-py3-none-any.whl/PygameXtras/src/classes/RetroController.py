import pygame


class RetroController:
    def __init__(self, index):
        self._controller = pygame.joystick.Joystick(index)

    def button_up(self) -> bool:
        return self._controller.get_axis(1) < -0.5

    def button_down(self) -> bool:
        return self._controller.get_axis(1) > 0.5

    def button_left(self) -> bool:
        return self._controller.get_axis(0) < -0.5

    def button_right(self) -> bool:
        return self._controller.get_axis(0) > 0.5

    def button_x(self) -> bool:
        return self._controller.get_button(0)

    def button_y(self) -> bool:
        return self._controller.get_button(3)

    def button_a(self) -> bool:
        return self._controller.get_button(1)

    def button_b(self) -> bool:
        return self._controller.get_button(2)

    def button_select(self) -> bool:
        return self._controller.get_button(8)

    def button_start(self) -> bool:
        return self._controller.get_button(9)

    def button_l(self) -> bool:
        return self._controller.get_button(4)

    def button_r(self) -> bool:
        return self._controller.get_button(5)
