import pygame
import sys

class PerformanceGraph:
    def __init__(self, desired_fps: int, fps_list: list[float]):
        win_w, win_h = 1200, 600
        border = 50


        pygame.init()
        screen = pygame.display.set_mode((win_w, win_h))
        fpsclock = pygame.time.Clock()
        fps = 60

        pygame.draw.line(screen, (0,0,255), (border, 100), (win_w - border, 100), 1)
        pygame.draw.line(screen, (255,255,255), (border, border), (border, win_h-border), 1)
        pygame.draw.line(screen, (255,255,255), (border, win_h - border), (win_w - border, win_h-border), 1)

        x = [2+border+i*((win_w-2*border)/len(fps_list)) for i in range(len(fps_list))]
        y = [win_h-border-((win_h-border*3)/desired_fps)*item for item in fps_list]
        # for x_, y_ in zip(x, y):
        #     pygame.draw.circle(screen, (255,0,0), (x_, y_), 1)
        for x_, y_ in zip(range(len(x)-1), range(len(y)-1)):
            pygame.draw.line(screen, (255,0,0), (x[x_], y[y_]), (x[x_+1], y[y_+1]))
        

        pygame.display.flip()

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

            fpsclock.tick(fps)
