import sys

import pygame
from src.classes.PlayStationVectorGraphics.psvg import PSVG

WIN_W, WIN_H = 1100, 500
INDEXES = 9
LINE_INDEXES = 2

screen = pygame.display.set_mode((WIN_W, WIN_H))
fpsclock = pygame.time.Clock()
fps = 60

center = (screen.get_width() // 2, screen.get_height() // 2)


def pos(index: int, line_index: int):
    return (
        int(WIN_W / (INDEXES + 1) * (index + 1)),
        int(WIN_H / (LINE_INDEXES + 1) * (line_index + 1)),
    )


while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    PSVG.up(screen, pos(0, 0))
    PSVG.right(screen, pos(1, 0))
    PSVG.down(screen, pos(2, 0))
    PSVG.left(screen, pos(3, 0))
    PSVG.slash(screen, pos(4, 0))
    PSVG.triangle(screen, pos(5, 0))
    PSVG.circle(screen, pos(6, 0))
    PSVG.cross(screen, pos(7, 0))
    PSVG.square(screen, pos(8, 0))

    PSVG.l1(screen, pos(0, 1))
    PSVG.l2(screen, pos(1, 1))
    PSVG.l3(screen, pos(2, 1))
    PSVG.r1(screen, pos(3, 1))
    PSVG.r2(screen, pos(4, 1))
    PSVG.r3(screen, pos(5, 1))
    PSVG.ps(screen, pos(6, 1))
    PSVG.options(screen, pos(7, 1))
    PSVG.share(screen, pos(8, 1))

    pygame.display.flip()
    fpsclock.tick(fps)
