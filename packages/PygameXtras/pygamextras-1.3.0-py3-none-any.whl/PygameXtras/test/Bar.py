from src.classes.Bar import Bar

import pygame
import sys

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

b = Bar(screen, (80,300), center,
           bgc=[80 for i in range(3)],
           fc=(40,40,220),
           bc=(0,0,0),
           borderwidth=3,
           br=15,
           fs="bottom"
           )

val = 50
max_val = 100

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    mk = pygame.mouse.get_pressed()
    if mk[0]:
        val = max(val - 1, 0)
    if mk[2]:
        val = min(val + 1, max_val)

    if mk[1]:
        b.update_pos(pygame.mouse.get_pos())

    b.update(val, max_val)

    screen.fill((100,100,255))
    b.draw()

    pygame.display.flip()
    fpsclock.tick(fps)