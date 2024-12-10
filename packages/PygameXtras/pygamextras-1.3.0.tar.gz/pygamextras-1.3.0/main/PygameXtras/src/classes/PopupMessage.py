import pygame
import time
from .Label import Label
from .Function import Function

class PopupMessage(Label):
    def __init__(self, passive_xy, active_xy, surface: pygame.Surface, size: int, anchor="center", **kwargs):

        # passive_xy #
        self.__passive_xy = passive_xy
        # assertion #
        assert isinstance(self.__passive_xy, (tuple, list)), f"invalid argument for 'passive_xy': {self.__passive_xy}"
        assert len(self.__passive_xy) == 2, f"invalid argument for 'passive_xy': {self.__passive_xy}"
        
        # active_xy #
        self.__active_xy = active_xy
        # assertion #
        assert isinstance(self.__active_xy, (tuple, list)), f"invalid argument for 'active_xy': {self.__active_xy}"
        assert len(self.__active_xy) == 2, f"invalid argument for 'active_xy': {self.__active_xy}"

        assert self.__active_xy != self.__passive_xy, "passive_xy and active_xy have to be different"

        super().__init__(surface, "", size, passive_xy, anchor, **kwargs)

        self.time = time.time()

        self.__f = Function()
        self.__f.add_const(0)
        self.__f.set_outer_values(0,0)

        self.__dx, self.__dy = self.__active_xy[0] - self.__passive_xy[0], self.__active_xy[1] - self.__passive_xy[1]

    def update(self):
        x = abs(self.time - time.time())
        dx = self.__dx * self.__f.get(x)
        dy = self.__dy * self.__f.get(x)
        self.update_pos((self.__passive_xy[0] + dx, self.__passive_xy[1] + dy))

    def show(self, text, seconds=4):
        self.__f.reset()
        self.__f.add_func("-x**2", -1, 0.3, 0.5)
        self.__f.add_const(1, seconds)
        self.__f.add_func("-x**2", -0.3, 1, 0.5, "max")
        self.__f.set_outer_values(0,0)

        self.update_text(str(text))
        self.time = time.time()

    def update_passive_xy(self, passive_xy):
        # passive_xy #
        self.__passive_xy = passive_xy
        # assertion #
        assert isinstance(self.__passive_xy, (tuple, list)), f"invalid argument for 'passive_xy': {self.__passive_xy}"
        assert len(self.__passive_xy) == 2, f"invalid argument for 'passive_xy': {self.__passive_xy}"
        self.__dx, self.__dy = self.__active_xy[0] - self.__passive_xy[0], self.__active_xy[1] - self.__passive_xy[1]

    def update_active_xy(self, active_xy):
        # active_xy #
        self.__active_xy = active_xy
        # assertion #
        assert isinstance(self.__active_xy, (tuple, list)), f"invalid argument for 'active_xy': {self.__active_xy}"
        assert len(self.__active_xy) == 2, f"invalid argument for 'active_xy': {self.__active_xy}"
        self.__dx, self.__dy = self.__active_xy[0] - self.__passive_xy[0], self.__active_xy[1] - self.__passive_xy[1]
