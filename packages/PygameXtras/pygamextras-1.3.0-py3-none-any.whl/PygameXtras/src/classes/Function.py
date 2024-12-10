import math
import pygame
import sys
import os
from .Label import Label
from .Button import Button

class Function:
    def __init__(self, min_: int = 0, max_: int = 1, function_variable: str = "x"):
        """ scales everything to a function between min_ and max_ (on the y axis) """
        self.__min = min_
        self.__max = max_
        self.__function_variable = function_variable
        self.__length = 0
        self.__funcs = [
            # every func except last:
            # [from (including), to (excluding), f_from, f_to, func, x_dist, y_dist]
            # last func:
            # [from (including), to (including), f_from, f_to, func, x_dist, y_dist]
        ]

        assert isinstance(function_variable, str) and function_variable.isalpha(), \
            f"invalid argument for 'function_variable': {function_variable}"

        self.__val_before = None
        self.__val_after = None

    def add_const(self, constant: float, length: float = 1):
        """ add a constant value """
        assert length > 0, f"<length> as to be greater than 0"
        assert isinstance(constant, (float, int)), f"invalid argument for 'constant': {constant}"
        self.__funcs.append(
            {
                # i_... = internal_... -> regarding the internal function that is being constructed
                # f_... = function_... -> regarding the function that is given by <func>
                "value": constant,
                "i_from": self.__length,
                "i_to": self.__length + length,
                "is_constant": True,
            }
        )
        self.__length += length

    def add_func(self, func: str, f_from: float, f_to: float, length: float = 1, start_at="min"):
        """ use the <function_variable> (by default 'x'), eg. '-x**2'; use 'math.' for the math library;
        <start_at> can be either 'min' or 'max' """

        assert isinstance(eval(func, {self.__function_variable: 0, "math": math}), int) or \
            isinstance(eval(func, {self.__function_variable: 0, "math": math}), float), \
            f"invalid argument for 'func': {func} | error: does not return integer or float"
        assert f_from < f_to, f"<f_from> can not be greater than or equal to <f_to>"
        assert length > 0, f"<length> as to be greater than 0"
        assert start_at in ("min", "max"), f"invalid argument for 'start_at': {start_at}"
        # assert (start_at in ["min", "max"] or isinstance(start_at, int) or isinstance(start_at, float)), \
        #     f"invalid argument for 'start_at': {start_at}"
        self.__funcs.append(
            {
                # i_... = internal_... -> regarding the internal function that is being constructed
                # f_... = function_... -> regarding the function that is given by <func>
                "func": func,
                "i_from": self.__length,
                "i_to": self.__length + length,
                "i_xdist": length,
                "i_ydist": self.__max - self.__min,
                "f_from": f_from,
                "f_to": f_to,
                "f_xdist": f_to - f_from,
                "f_ydist": abs(eval(func, {"x": f_to, "math": math}) - eval(func, {"x": f_from, "math": math})),
                "start_at": start_at,
                "is_constant": False,
            }
        )
        self.__length += length

    def __round_half_up(self, n, decimals):
        if isinstance(n, int):
            return n
        multiplier = 10 ** decimals
        if decimals == 0:
            return int(math.floor(n*multiplier + 0.5) / multiplier)
        else:
            return math.floor(n*multiplier + 0.5) / multiplier

    def get(self, x, decimals=None):
        """ return the value of the function at <x> """

        if not 0 <= x <= self.__length:
            if self.__val_before is not None and x < 0:
                return self.__val_before
            elif self.__val_after is not None and x > self.__length:
                return self.__val_after
            else:
                raise ValueError(f"<x> is out of range! Function length: {self.__length}")

        # finding the correct function (setting to 'f')
        for count, func in enumerate(self.__funcs):

            # if last function
            if count == len(self.__funcs)-1:
                if func["i_from"] <= x <= func["i_to"]:
                    f = func
                    break

            # every function but the last
            else:
                if func["i_from"] <= x < func["i_to"]:
                    f = func
                    break

        # now we have 'f' as the correct function
        if f["is_constant"] == False:
            actual_x = x - func["i_from"]
            percent = actual_x / func["i_xdist"]

            new_x_dist = func["f_xdist"]
            filling = percent * new_x_dist
            f_x = func["f_from"] + filling

            y_val = eval(f["func"],
                         {self.__function_variable: f_x, "math": math})

            y_min = eval(f["func"],
                         {self.__function_variable: func["f_from"], "math": math})
            y_max = eval(f["func"],
                         {self.__function_variable: func["f_to"], "math": math})
            g = abs(y_max - y_min)
            a = y_val - y_min
            factor = a/g

            if f["start_at"] == "min":
                start = self.__min
                end = self.__max
            elif f["start_at"] == "max":
                start = self.__max
                end = self.__min
            # else:
            #     start = f["start_at"]

            filling = factor * abs(end - start)
            value = start + filling

        elif f["is_constant"] == True:
            value = f["value"]

        if decimals != None:
            return self.__round_half_up(value, decimals)
        else:
            return value

    def set_outer_values(self, value_before: float, value_after: float):
        assert isinstance(value_before, int) or isinstance(
            value_before, float), f"invalid argument for 'value_before': {value_before}"
        assert isinstance(value_after, int) or isinstance(
            value_after, float), f"invalid argument for 'value_after': {value_after}"
        self.__val_before = value_before
        self.__val_after = value_after

    def show(self, show_every_value=False):
        """ display the current function in a window """

        if self.__length == 0:
            raise Exception("Can not draw function because the length is zero.")

        # creating the dots # ! improvement needed # TODO
        dots = []
        dots_count = 200
        step = self.__length / dots_count
        x = 0
        while x <= self.__length:
            dots.append(
                (x, self.get(x))
            )
            x += step

        d_min = min([d[1] for d in dots])
        d_max = max([d[1] for d in dots])

        if show_every_value:
            MIN = d_min
            MAX = d_max
        else:
            MIN = self.__min
            MAX = self.__max

        pygame.init()
        screen = pygame.display.set_mode((900, 500))
        fpsclock = pygame.time.Clock()
        fps = 60

        col = [160 for i in range(3)]

        l_y_max = Label(screen, self.__round_half_up(MAX, 2), 20, (50, 50), "midright", xad=10, tc=col)
        l_y_min = Label(screen, self.__round_half_up(MIN, 2), 20, (50, 450), "midright", xad=10, tc=col)
        l_y_max.draw()
        l_y_min.draw()

        # if show_every_value: also draw self.__min and self.__max marks
        if show_every_value:
            l_mark_max_percent = (self.__max - MIN) / (MAX - MIN)
            l_mark_max_height = 450 - 400*l_mark_max_percent
            if self.__max != MAX:
                l_y_max_mark = Label(
                    screen, self.__round_half_up(self.__max, 3),
                    20, (50, l_mark_max_height),
                    "midright", xad=10, tc=col)
                l_y_max_mark.draw()

            l_mark_min_percent = (self.__min - MIN) / (MAX - MIN)
            l_mark_min_height = 450 - 400*l_mark_min_percent
            if self.__min != MIN:
                l_y_min_mark = Label(
                    screen, self.__round_half_up(self.__min, 3),
                    20, (50, l_mark_min_height),
                    "midright", xad=10, tc=col)
                l_y_min_mark.draw()

        l_x_min = Label(screen, 0, 20, (50, 450), "midtop", yad=10, tc=col)
        l_x_max = Label(screen, self.__length, 20, (850, 450), "midtop", yad=10, tc=col)
        l_x_min.draw()
        l_x_max.draw()

        # drawing the lines
        pygame.draw.line(screen, col, (50, 50), (50, 450), 1)
        if show_every_value:
            pygame.draw.line(screen, (255, 0, 0), (50, l_mark_max_height), (850, l_mark_max_height), 1)
            pygame.draw.line(screen, (255, 0, 0), (50, l_mark_min_height), (850, l_mark_min_height), 1)
        else:
            pygame.draw.line(screen, (255, 0, 0), (50, 450), (850, 450), 1)
            pygame.draw.line(screen, (255, 0, 0), (50, 50), (850, 50), 1)

        # drawing the dots
        for dot in dots:
            min_percent = (self.__min - MIN) / (MAX - MIN)
            min_height = 400*min_percent
            pygame.draw.circle(
                screen, (0, 0, 255),
                (50 + dot[0] * (800 / self.__length),
                 450 - min_height - dot[1] * (400 / (MAX - MIN))),
                2)

        # incr_size_img = pygame.image.load(r"images\increase_size.png")
        incr_size_img = pygame.image.load(os.path.join(os.path.split(os.path.dirname(__file__))[0], "images", "increase_size.png"))
        incr_size_img.set_colorkey((255, 255, 255))
        # decr_size_img = pygame.image.load(r"images\decrease_size.png")
        decr_size_img = pygame.image.load(os.path.join(os.path.split(os.path.dirname(__file__))[0], "images", "decrease_size.png"))
        decr_size_img.set_colorkey((255, 255, 255))

        if show_every_value:
            button = Button(screen, "", 10, (22, 22), "center", fd=(32, 32), img=decr_size_img)
        else:
            button = Button(screen, "", 10, (22, 22), "center", fd=(32, 32), img=incr_size_img)
        button.draw()

        run = True
        while run:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            if button.update(event_list):
                self.show(not show_every_value)

            pygame.display.flip()
            fpsclock.tick(fps)

    def reset(self):
        """ deletes all previously added functions """
        self.__length = 0
        self.__funcs = []

    def example_function(self):
        """ show the example function """
        self.__min = 0
        self.__max = 1
        self.__function_variable = "x"
        self.__length = 0
        self.__funcs = []
        self.add_func("(-math.sin(x*3))/math.cos(x/2)", 0.5, 4.5, 10)
        print("Function: (-math.sin(x*3))/math.cos(x/2)")
        self.show()
