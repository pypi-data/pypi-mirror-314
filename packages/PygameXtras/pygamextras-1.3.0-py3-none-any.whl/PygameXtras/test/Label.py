from src.classes.Label import Label

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

pos1 = (50, 50)
pos2 = (450, 50)
pos3 = center
pos4 = (50, 450)
pos5 = (450, 450)

# l1 = Label(screen, "Test Label 1", 25, pos1, "topleft", bw=1, fd=(120, 60), p=5)
# l2 = Label(screen, "Test Label 2", 25, pos2, "topright", bw=1, fd=(120, 60), p=5)
l3 = Label(screen, "Test Label 3", 25, pos3, "center", bw=1, fd=(300, 160), p=5, bgc=(200,80,80))
# l4 = Label(screen, "Test Label 4", 25, pos4, "bottomleft", bw=1, fd=(120, 60), p=5)
# l5 = Label(screen, "Test Label 5", 25, pos5, "bottomright", bw=1, fd=(120, 60), p=5)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    screen.fill((100,100,200))
    # for l in [l1,l2,l3,l4,l5]:
        # l.draw()
    l3.draw()
    r = pygame.Rect(0,0,300,160)
    r.center = center
    rect(r, "red", 1)

    pygame.display.flip()
    fpsclock.tick(fps)