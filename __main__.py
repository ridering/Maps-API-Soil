import pygame
import text_input
import io
from request_image import load_map

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 80


class Map:
    def __init__(self):
        self.scale = 2
        self.center = [58, -50]
        self.render()

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (480, 0), (480, 500), 5)
        pygame.draw.line(screen, pygame.Color("red"), (0, 45), (700, 45), 5)
        self.image = pygame.image.load(io.BytesIO(load_map([str(self.center[0]), str(self.center[1])], self.scale)))



cur_map = Map()

# Create TextInput-object
text_input = text_input.TextInput()

clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(10)

while running:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            scale = 0.1 ** (cur_map.scale // 4) * (17 - cur_map.scale + 3)
            if event.key == pygame.K_PAGEDOWN:
                if cur_map.scale > 0:
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
    cur_map.center[0] %= 180
    cur_map.center[1] %= 90
    screen.fill(pygame.Color('white'))
    screen.blit(cur_map.image, (10, 50))

    # Feed it with events every frame
    # text_input.update(events)
    # Blit its surface onto the screen
    # screen.blit(text_input.get_surface(), (10, 10))
    # pygame.display.flip()
    cur_map.render()

    pygame.display.update()

pygame.quit()
