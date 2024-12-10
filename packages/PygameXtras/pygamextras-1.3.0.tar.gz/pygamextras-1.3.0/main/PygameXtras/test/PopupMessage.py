from src.classes.PopupMessage import PopupMessage

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

msg = PopupMessage((250,  320), (250, 180), screen, 32, "center", fh=40, xad=10, bw=1)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("showing test message")
            msg.show("Test message", 4)
    
    msg.update()

    screen.fill((20,20,200))

    line((75, 250), (425, 250), (0,0,0), 3)
    line((210, 200), (290, 200), (0,0,0), 3)
    line((210, 300), (290, 300), (0,0,0), 3)

    msg.draw()


    pygame.display.flip()
    fpsclock.tick(fps)