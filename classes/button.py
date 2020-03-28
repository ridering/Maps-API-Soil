import pygame

from __main__ import screen, buttons
from classes.labl import Label


class Button(Label):
    def __init__(self, text_text, color, x, y, bg_color='white', angle=0, font_size=30):
        super().__init__(text_text, color, x, y, group=buttons)
        self.default(text_text, x, y, angle, font_size)
        self.p = False
        self.static = self.make_image(text_text, color, bg_color, angle, self.width, self.height)
        self.active = self.make_image(text_text, color, 'yellow', angle, self.width, self.height)
        self.image = self.static

    def make_image(self, text_text, color, bg_color, angle, but_width, but_height):
        text = self.font.render("{}".format(text_text), 1, pygame.Color(color))
        screen.fill(pygame.Color(bg_color))
        screen.blit(text, (0, 0))
        pygame.draw.rect(screen, pygame.color.Color(color), (0, 0, but_width, but_height), 1)
        image = screen.subsurface((0, 0, but_width, but_height)).copy()
        return pygame.transform.rotate(image, angle)
