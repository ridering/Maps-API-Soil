import pygame
import text_input
import io
from request_image import load_map

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 80

SCALES = [-79.5, 21.8, 70.225, 80.112, 82.992, 84.15, 84.61, 84.85, 84.972, 85.027,
          85.055, 85.065, 85.07, 85.074, 85.077, 85.079, 85.08, 85.0805]


class Map:
    def __init__(self):
        self.scale = 2
        self.center = [56.188484, 58.007144]
        self.render()

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (0, 45), (700, 45), 5)
        self.image = pygame.image.load(
            io.BytesIO(load_map([str(self.center[0]), str(self.center[1])], self.scale)))


cur_map = Map()

text_input = text_input.TextInput()

clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(10)

while running:
    clock.tick(FPS)
    events = pygame.event.get()
    scale = 0.1 ** (cur_map.scale // 4) * (17 - cur_map.scale + 3)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if cur_map.scale > 1:
                    cur_map.scale -= 1
            elif event.key == pygame.K_PAGEUP:
                if cur_map.scale < 17:
                    cur_map.scale += 1
            elif event.key == pygame.K_DOWN:
                cur_map.center[1] -= scale
            elif event.key == pygame.K_UP:
                cur_map.center[1] += scale
            elif event.key == pygame.K_LEFT:
                cur_map.center[0] -= scale
            elif event.key == pygame.K_RIGHT:
                cur_map.center[0] += scale
    screen.fill(pygame.Color('white'))
    screen.blit(cur_map.image, (10, 50))

    if cur_map.center[0] > 180:
        cur_map.center[0] -= 360
    elif cur_map.center[0] < -180:
        cur_map.center[0] += 360

    if cur_map.center[1] >= 0:
        if cur_map.center[1] > SCALES[cur_map.scale]:
            cur_map.center[1] = SCALES[cur_map.scale]
    else:
        if cur_map.center[1] < -SCALES[cur_map.scale]:
            cur_map.center[1] = -SCALES[cur_map.scale]

    cur_map.render()
    pygame.display.update()

pygame.quit()
