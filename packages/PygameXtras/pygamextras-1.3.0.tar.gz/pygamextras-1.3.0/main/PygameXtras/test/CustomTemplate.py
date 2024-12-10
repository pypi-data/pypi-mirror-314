from src.classes.CustomTemplate import CustomTemplate
from src.classes.Colors import Colors

import pygame
import sys
c = Colors()
c1 = {
    'black': (0,0,0),
    'white': (255,255,255),
    'cyan': (0,255,255),
    'magenta': (255,0,255),
    'yellow': (255,255,0),
    'red': (255,0,0),
    'green': (0,255,0),
    'blue': (0,0,255)
}

pygame.init()
screen = pygame.display.set_mode((500,500))
fpsclock = pygame.time.Clock()
fps = 60

def circle(xy, color, radius=3, width=0):
    color = c1[color] if isinstance(color, str) else color
    pygame.draw.circle(screen, color, xy, radius, width)

def line(xy1, xy2, color, width=1):
    color = c1[color] if isinstance(color, str) else color
    pygame.draw.line(screen, color, xy1, xy2, width)

def rect(r, color, width=0):
    color = c1[color] if isinstance(color, str) else color
    pygame.draw.rect(screen, color, r, width)

center = (250, 250)

ct = CustomTemplate(surface=screen, size=80, anchor="topleft")
l = ct.label(text="new label", xy=center, size=10)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    screen.fill((100,100,100))
    l.draw()

    pygame.display.flip()
    fpsclock.tick(fps)