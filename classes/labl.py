import pygame

from __main__ import screen, labels


class Label(pygame.sprite.Sprite):
    def __init__(self, text_text, color, x, y, group=labels, angle=0, font_size=30):
        super().__init__(group)
        self.default(text_text, x, y, angle, font_size)
        self.make_text(self.text, color, 'white')

    def default(self, text_text, x, y, angle, font_size):
        self.width, self.height = self.get_size(text_text, font_size)
        if angle == 270:
            self.rect = pygame.Rect(x, y, self.height, self.width)
        else:
            self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y
        self.text = text_text.strip()

    def get_size(self, text_text, font_size):
        self.font = pygame.font.Font('font.ttf', font_size)
        return pygame.font.Font.size(self.font, text_text)

    def make_text(self, text, color, bg_color):
        words = text.split()
        space = self.font.size(' ')[0]
        max_width = 200
        screen.fill(pygame.Color(bg_color))
        x, y = 0, 0
        for word in words:
            word_surface = self.font.render(word, 1, pygame.color.Color(color))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = 0
                y += word_height
            screen.blit(word_surface, (x, y))
            x += word_width + space
        self.image = screen.subsurface((0, 0, 200, y + 31)).copy()
