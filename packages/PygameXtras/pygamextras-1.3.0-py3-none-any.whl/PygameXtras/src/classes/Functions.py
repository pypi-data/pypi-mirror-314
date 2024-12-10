import ctypes
import math
import os

import pygame

from ..parsers.color import Color


def higher_resolution(boolean: bool = True):
    """
    Most Windows PCs (automatically) use scaling to 150% which makes many applications appear
    blurry. To avoid this effect, this function can be called to increase the resolution on
    affected displays without having to manually change the scaling in the computers settings.
    """
    if os.name == "nt":
        ctypes.windll.shcore.SetProcessDpiAwareness(bool(boolean))


def scale_image(image, factor):
    """
    Changes the size of an image while keeping its proportions.
    """
    return pygame.transform.scale(
        image, (int(image.get_width() * factor), int(image.get_height() * factor))
    )


def create_animation(image_ids: list, frames_per_image: list):
    """
    create a dict with image_ids and corresponding
    images before using this function.

    If usage unclear, refer to:
    marcel-python-programs\PYGAME_GAMES\pve\mini_warfare\data\player.py
    """
    assert len(image_ids) == len(
        frames_per_image
    ), "received lists of different lengths"
    seq = []
    for image_id, count in zip(image_ids, frames_per_image):
        for i in range(count):
            seq.append(image_id)
    return seq


def get_distance_squared(xy1: tuple, xy2: tuple) -> float:
    return (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2


def get_distance(xy1: tuple, xy2: tuple) -> float:
    return math.sqrt(get_distance_squared(xy1, xy2))


def get_angle_between_points(xy1, xy2):
    vect = pygame.math.Vector2(xy2[0] - xy1[0], xy2[1] - xy1[1]).normalize()
    cos = round_half_up(vect.y, 2)
    deg_cos = int(math.degrees(math.acos(vect.x)))
    if cos <= 0:
        return deg_cos
    else:
        return 180 + (180 - deg_cos)


def get_normalized_vector_between_points(xy1, xy2):
    vect = pygame.math.Vector2(xy2[0] - xy1[0], xy2[1] - xy1[1])
    if vect.length() > 0:
        vect.normalize()
    return vect


def get_normalized_vector_from_angle(angle):
    vect = pygame.Vector2(
        round_half_up(math.cos(math.radians(angle)), 3),
        round_half_up(math.sin(math.radians(angle)), 3),
    )
    return vect.normalize()


def round_half_up(n, decimals=0):
    if isinstance(n, int):
        return n
    multiplier = 10**decimals
    if decimals == 0:
        return int(math.floor(n * multiplier + 0.5) / multiplier)
    else:
        return math.floor(n * multiplier + 0.5) / multiplier


def vect_sum(a: tuple, b: tuple):
    if len(a) != len(b):
        raise ValueError("Received vectors of different dimensions.")
    vect = []
    for num1, num2 in zip(a, b):
        vect.append(num1 + num2)
    return tuple(vect)


def vs(a: tuple, b: tuple):
    """vect_sum(...)"""
    return vect_sum(a, b)


def invert(a: tuple):
    """inverts a vector"""
    return (-a[0], -a[1])


def inv(a: tuple):
    """invert(...)"""
    return invert(a)


def draw_rect_alpha(
    surface,
    color,
    rect,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(
        shape_surf,
        Color.parse(color),
        shape_surf.get_rect(),
        width,
        border_radius,
        border_top_left_radius,
        border_top_right_radius,
        border_bottom_left_radius,
        border_bottom_right_radius,
    )
    surface.blit(shape_surf, rect)


def draw_circle_alpha(
    surface,
    color,
    center,
    radius,
    width: int = 0,
    draw_top_right: bool = None,
    draw_top_left: bool = None,
    draw_bottom_left: bool = None,
    draw_bottom_right: bool = None,
):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(
        shape_surf,
        Color.parse(color),
        (radius, radius),
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(
        shape_surf, Color.parse(color), [(x - min_x, y - min_y) for x, y in points]
    )
    surface.blit(shape_surf, target_rect)


def ask_filename():
    """temporary method to get filename"""
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def ask_directory():
    """temporary method to get foldername"""
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


def get_fonts():
    return [
        f.removesuffix(".ttf")
        for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "fonts"))
    ]


def hide_mouse():
    if not pygame.get_init():
        pygame.init()
    pygame.mouse.set_cursor(
        (8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)
    )


def check(func):
    """decorator to validate a function against its type hints"""

    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        for arg_name, arg_value in zip(func.__code__.co_varnames, args):
            if arg_name in annotations and not isinstance(
                arg_value, annotations[arg_name]
            ):
                raise TypeError(
                    f"Argument '{arg_name}' (value={arg_value}, type={type(arg_value)}) is not consistent with type(s) '{annotations[arg_name]}'"
                )
        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations and not isinstance(
                arg_value, annotations[arg_name]
            ):
                raise TypeError(
                    f"Argument '{arg_name}' (value={arg_value}, type={type(arg_value)}) is not consistent with type(s) '{annotations[arg_name]}'"
                )
        return func(*args, **kwargs)

    return wrapper
