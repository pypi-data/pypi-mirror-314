import pygame
import sys
from .Label import Label
from .Button import Button
from .Functions import vect_sum
from .Colors import Colors
from .Paragraph import Paragraph

class Messagebox:
    def __init__(
            self, surface, pygame_clock: pygame.time.Clock, fps: int, screen_center: tuple, textsize=25,
            textcolor: tuple = (0, 0, 0), backgroundcolor: tuple = (128, 128, 128)):
        self.surface = surface
        self.pygame_clock = pygame_clock
        self.fps = fps
        self.screen_center = screen_center
        self.textsize = textsize
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor

        assert fps >= 10
        assert 20 <= textsize <= 40
        assert type(textcolor) in [tuple, list]
        assert type(backgroundcolor) in [tuple, list]

    def askokcancel(self, text, dim_background=True):

        if dim_background:
            self.surface.fill([60 for i in range(3)], special_flags=pygame.BLEND_MULT)

        test = Label(self.surface, text, self.textsize, (0, 0), xad=25)
        width = min(max(test.background_rect.width, 294), 900)
        height = test.rect.height * 5

        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.screen_center

        surface = pygame.Surface((width, height))
        surface.fill(self.backgroundcolor)

        width = min(max(width, 100), 150)
        height = int(test.rect.height * 1.75)
        l_text = Label(self.surface, text, self.textsize, vect_sum(
            self.screen_center, (0, -5)), "midbottom", tc=self.textcolor)

        b_cancel_premade = Button(
            self.surface, "Cancel", self.textsize, vect_sum(rect.midbottom, (3, 0)),
            "bottomright", tc=self.textcolor, bgc=Colors.dark_red, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0))
        b_cancel = Button(
            self.surface, "Cancel", self.textsize, vect_sum(rect.midbottom, (3, 0)),
            "bottomright", tc=self.textcolor, bgc=Colors.dark_red, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0),
            aA=vect_sum(b_cancel_premade.rect, (3, 3, -6, -6)))

        b_ok_premade = Button(
            self.surface, "OK", self.textsize, vect_sum(rect.midbottom, (-3, 0)),
            "bottomleft", tc=self.textcolor, bgc=Colors.green, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0))
        b_ok = Button(
            self.surface, "OK", self.textsize, vect_sum(rect.midbottom, (-3, 0)),
            "bottomleft", tc=self.textcolor, bgc=Colors.green, hl=True, bR=1, fd=(width, height),
            bw=4, br=1, bc=(0, 0, 0),
            aA=vect_sum(b_ok_premade.rect, (3, 3, -6, -6)))

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

            if b_cancel.update(mouse_events):
                return False
            if b_ok.update(mouse_events):
                return True

            self.surface.blit(surface, rect)
            l_text.draw()
            b_cancel.draw()
            b_ok.draw()

            pygame.draw.rect(self.surface, (0, 0, 0), rect, 4, 1, 1, 1, 1)
            pygame.display.flip()
            self.pygame_clock.tick(self.fps)

    def show_message(self, text, dim_background=True, multiline=False):

        if dim_background:
            self.surface.fill([60 for i in range(3)], special_flags=pygame.BLEND_MULT)

        if multiline:
            test = Paragraph(self.surface, text, self.textsize, (0, 0), xad=25, yad=3)
            width = min(max(test.rect.width, 200), 800)
            height = test.rect.height + 100
        else:
            test = Label(self.surface, text, self.textsize, (0, 0), xad=25)
            width = min(max(test.rect.width, 200), 800)
            height = test.rect.height * 5

        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.screen_center

        surface = pygame.Surface((width, height))
        surface.fill(self.backgroundcolor)

        height = int(test.rect.height * 1.75)
        if multiline:
            lines = len([1 for char in text if char == "\n"])
            jump = self.textsize//2
            l_text = Paragraph(self.surface, text, self.textsize, vect_sum(
                self.screen_center, (0, -lines*jump)), "midbottom", tc=self.textcolor, yad=3)
        else:
            l_text = Label(self.surface, text, self.textsize, vect_sum(
                self.screen_center, (0, -5)), "midbottom", tc=self.textcolor)

        b_ok = Button(
            self.surface, "OK", self.textsize, vect_sum(rect.bottomright, (-10, -10)),
            "bottomright", tc=self.textcolor, bgc=Colors.green, hl=True, bR=1, xad=20, yad=6, to=(0,1),
            bw=4, br=1, bc=(0, 0, 0))

        run = True
        while run:
            event_list = pygame.event.get()
            mouse_events = [event for event in event_list if event.type == pygame.MOUSEBUTTONUP]
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            if b_ok.update(mouse_events):
                run = False

            self.surface.blit(surface, rect)
            l_text.draw()
            b_ok.draw()

            pygame.draw.rect(self.surface, (0, 0, 0), rect, 4, 1, 1, 1, 1)
            pygame.display.flip()
            self.pygame_clock.tick(self.fps)
