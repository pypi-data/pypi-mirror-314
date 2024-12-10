import pygame
from ..Label import Label


def up(size: int):
    points = []

    angle = 110

    v = pygame.Vector2(0, -1)
    v.scale_to_length(size * 0.4)
    points.append((v.x, v.y))

    v.scale_to_length(size * 0.55)
    v.rotate_ip(angle)
    points.append((v.x, v.y))

    v.rotate_ip((180 - angle) * 2)
    points.append((v.x, v.y))

    return points


def right(size: int):
    points = []

    angle = 110

    v = pygame.Vector2(1, 0)
    v.scale_to_length(size * 0.4)
    points.append((v.x, v.y))

    v.scale_to_length(size * 0.55)
    v.rotate_ip(angle)
    points.append((v.x, v.y))

    v.rotate_ip((180 - angle) * 2)
    points.append((v.x, v.y))

    return points


def down(size: int):
    points = []

    angle = 110

    v = pygame.Vector2(0, 1)
    v.scale_to_length(size * 0.4)
    points.append((v.x, v.y))

    v.scale_to_length(size * 0.55)
    v.rotate_ip(angle)
    points.append((v.x, v.y))

    v.rotate_ip((180 - angle) * 2)
    points.append((v.x, v.y))

    return points


def left(size: int):
    points = []

    angle = 110

    v = pygame.Vector2(-1, 0)
    v.scale_to_length(size * 0.4)
    points.append((v.x, v.y))

    v.scale_to_length(size * 0.55)
    v.rotate_ip(angle)
    points.append((v.x, v.y))

    v.rotate_ip((180 - angle) * 2)
    points.append((v.x, v.y))

    return points


def triangle(size: int):
    points = []

    v = pygame.Vector2(0, -1)
    v.scale_to_length(size * 0.6)
    points.append((v.x, v.y))

    v.rotate_ip(120)
    points.append((v.x, v.y))

    v.rotate_ip(120)
    points.append((v.x, v.y))

    return points


def square(size: int):
    points = []

    v = pygame.Vector2(1, 1)
    v.scale_to_length(size * 0.6)
    for _ in range(4):
        v.rotate_ip(90)
        points.append((v.x, v.y))

    return points


def slash(size: int):
    points = []

    v = pygame.Vector2(0, -1)
    v.scale_to_length(size * 1.2)
    v.rotate_ip(25)
    points.append((v.x, v.y))
    v.rotate_ip(180)
    points.append((v.x, v.y))

    return points


def __small_box(size: int):
    points = []

    v = pygame.Vector2(0, -1)
    v.scale_to_length(size * 1)

    v.rotate_ip(60)
    points.append((v.x, v.y))

    v.rotate_ip(60)
    points.append((v.x, v.y))

    v.rotate_ip(120)
    points.append((v.x, v.y))

    v.rotate_ip(60)
    points.append((v.x, v.y))

    return points


def __big_box(size: int):
    points = []

    v = pygame.Vector2(0, -1)
    v.scale_to_length(size * 1)

    angle_start = 35
    angle_between = 95

    v.rotate_ip(angle_start)
    points.append((v.x, v.y))

    v.rotate_ip(angle_between)
    points.append((v.x, v.y))

    v = pygame.Vector2(0, -1)
    v.scale_to_length(size * 1)

    v.rotate_ip(-angle_start)
    points.append((v.x, v.y))

    v.rotate_ip(-angle_between)
    points.insert(2, (v.x, v.y))

    return points


size_factor = 0.6


def l1(size: int, color: tuple):
    return __small_box(size), Label(
        None, "L1", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )


def l2(size: int, color: tuple):
    return __big_box(size), Label(
        None, "L2", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )


def l3(size: int, color: tuple):
    return Label(None, "L3", int(size * size_factor), (0, 0), tc=color, f="verdana")


def r1(size: int, color: tuple):
    return __small_box(size), Label(
        None, "R1", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )


def r2(size: int, color: tuple):
    return __big_box(size), Label(
        None, "R2", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )


def r3(size: int, color: tuple):
    return Label(None, "R3", int(size * size_factor), (0, 0), tc=color, f="verdana")


def __octagon(size: int):
    points = []

    v = pygame.Vector2(0, 1)
    v.scale_to_length(size)

    corners = 8

    v.rotate_ip(360 / corners / 2)

    for _ in range(corners):
        points.append((v.x, v.y))
        v.rotate_ip(360 / corners)

    return points


def ps(size: int, color: tuple):
    return __octagon(size), Label(
        None, "PS", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )


def options(size: int, color: tuple):
    return __octagon(size), Label(
        None, "OPT", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )


def share(size: int, color: tuple):
    return __octagon(size), Label(
        None, "SHA", int(size * size_factor), (0, 0), tc=color, f="verdana"
    )
