import pygame
pygame.init()

from .psvg_util import *


class PSVG:

    __color = (255, 255, 255)
    __size = 50
    __linewidth = 5

    __up = up(__size)
    __right = right(__size)
    __down = down(__size)
    __left = left(__size)

    __triangle = triangle(__size)
    # __circle = circle(__size)
    # __cross = cross(__size)
    __square = square(__size)

    __slash = slash(__size)

    __l1 = l1(__size, __color)
    __l2 = l2(__size, __color)
    __l3 = l3(__size, __color)

    __r1 = r1(__size, __color)
    __r2 = r2(__size, __color)
    __r3 = r3(__size, __color)

    __ps = ps(__size, __color)
    __options = options(__size, __color)
    __share = share(__size, __color)

    @staticmethod
    def __reload():
        PSVG.__up = up(PSVG.__size)
        PSVG.__right = right(PSVG.__size)
        PSVG.__down = down(PSVG.__size)
        PSVG.__left = left(PSVG.__size)

        PSVG.__triangle = triangle(PSVG.__size)
        PSVG.__square = square(PSVG.__size)

        PSVG.__slash = slash(PSVG.__size)

        PSVG.__l1 = l1(PSVG.__size, PSVG.__color)
        PSVG.__l2 = l2(PSVG.__size, PSVG.__color)
        PSVG.__l3 = l3(PSVG.__size, PSVG.__color)

        PSVG.__r1 = r1(PSVG.__size, PSVG.__color)
        PSVG.__r2 = r2(PSVG.__size, PSVG.__color)
        PSVG.__r3 = r3(PSVG.__size, PSVG.__color)

        PSVG.__ps = ps(PSVG.__size, PSVG.__color)
        PSVG.__options = options(PSVG.__size, PSVG.__color)
        PSVG.__share = share(PSVG.__size, PSVG.__color)

    @staticmethod
    def set_color(color: tuple[int, int, int]):
        PSVG.__color = color
        PSVG.__reload()

    @staticmethod
    def set_size(size: int):
        PSVG.__size = size
        PSVG.__reload()

    @staticmethod
    def set_linewidth(linewidth: int):
        PSVG.__linewidth = linewidth

    @staticmethod
    def __outline(surface, center):
        pygame.draw.circle(
            surface,
            PSVG.__color,
            center,
            PSVG.__size,
            PSVG.__linewidth,
        )

    @staticmethod
    def __draw_lines(surface, center, offset_points):
        for i in range(len(offset_points)):
            pygame.draw.line(
                surface,
                PSVG.__color,
                (
                    center[0] + offset_points[i][0],
                    center[1] + offset_points[i][1],
                ),
                (
                    center[0] + offset_points[i - 1][0],
                    center[1] + offset_points[i - 1][1],
                ),
                PSVG.__linewidth,
            )

    @staticmethod
    def up(surface, center):
        PSVG.__outline(surface, center)
        PSVG.__draw_lines(surface, center, PSVG.__up)

    @staticmethod
    def right(surface, center):
        PSVG.__outline(surface, center)
        PSVG.__draw_lines(surface, center, PSVG.__right)

    @staticmethod
    def down(surface, center):
        PSVG.__outline(surface, center)
        PSVG.__draw_lines(surface, center, PSVG.__down)

    @staticmethod
    def left(surface, center):
        PSVG.__outline(surface, center)
        PSVG.__draw_lines(surface, center, PSVG.__left)

    @staticmethod
    def triangle(surface, center):
        PSVG.__outline(surface, center)
        PSVG.__draw_lines(surface, center, PSVG.__triangle)

    @staticmethod
    def circle(surface, center):
        PSVG.__outline(surface, center)
        pygame.draw.circle(
            surface,
            PSVG.__color,
            center,
            PSVG.__size * 0.575,
            PSVG.__linewidth,
        )

    @staticmethod
    def cross(surface, center):
        PSVG.__outline(surface, center)
        pygame.draw.line(
            surface,
            PSVG.__color,
            (
                center[0] + PSVG.__square[0][0],
                center[1] + PSVG.__square[0][1],
            ),
            (
                center[0] + PSVG.__square[2][0],
                center[1] + PSVG.__square[2][1],
            ),
            PSVG.__linewidth,
        )
        pygame.draw.line(
            surface,
            PSVG.__color,
            (
                center[0] + PSVG.__square[1][0],
                center[1] + PSVG.__square[1][1],
            ),
            (
                center[0] + PSVG.__square[3][0],
                center[1] + PSVG.__square[3][1],
            ),
            PSVG.__linewidth,
        )

    @staticmethod
    def square(surface, center):
        PSVG.__outline(surface, center)
        PSVG.__draw_lines(surface, center, PSVG.__square)

    @staticmethod
    def slash(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__slash)

    @staticmethod
    def l1(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__l1[0])
        PSVG.__l1[1].update_pos(center)
        PSVG.__l1[1].draw_to(surface)

    @staticmethod
    def l2(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__l2[0])
        PSVG.__l2[1].update_pos(center)
        PSVG.__l2[1].draw_to(surface)

    @staticmethod
    def l3(surface, center):
        PSVG.__outline(surface, center)
        pygame.draw.circle(
            surface,
            PSVG.__color,
            center,
            PSVG.__size * 0.75,
            PSVG.__linewidth,
        )
        PSVG.__l3.update_pos(center)
        PSVG.__l3.draw_to(surface)

    @staticmethod
    def r1(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__r1[0])
        PSVG.__r1[1].update_pos(center)
        PSVG.__r1[1].draw_to(surface)

    @staticmethod
    def r2(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__r2[0])
        PSVG.__r2[1].update_pos(center)
        PSVG.__r2[1].draw_to(surface)

    @staticmethod
    def r3(surface, center):
        PSVG.__outline(surface, center)
        pygame.draw.circle(
            surface,
            PSVG.__color,
            center,
            PSVG.__size * 0.75,
            PSVG.__linewidth,
        )
        PSVG.__r3.update_pos(center)
        PSVG.__r3.draw_to(surface)

    @staticmethod
    def ps(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__ps[0])
        PSVG.__ps[1].update_pos(center)
        PSVG.__ps[1].draw_to(surface)

    @staticmethod
    def options(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__options[0])
        PSVG.__options[1].update_pos(center)
        PSVG.__options[1].draw_to(surface)

    @staticmethod
    def share(surface, center):
        PSVG.__draw_lines(surface, center, PSVG.__share[0])
        PSVG.__share[1].update_pos(center)
        PSVG.__share[1].draw_to(surface)
