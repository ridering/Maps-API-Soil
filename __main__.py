import pygame
import text_input
import os
import sys

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 80


class Map:
    def __init__(self):
        pass

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (500, 0), (500, 500), 5)
        pygame.draw.line(screen, pygame.Color("red"), (0, 500 - 15), (700, 500 - 15), 5)


cur_map = Map()
text = text_input.TextInput()

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('black'))

    text.update(events)
    screen.blit(text.get_surface(), (10, 10))

    cur_map.render()
    pygame.display.flip()

pygame.quit()