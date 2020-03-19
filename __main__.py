import pygame
import text_input
import io
from request_image import load_map
from request_coordinate import get_coordinates, get_toponym
from math import cos, radians

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 300

SCALES = [-79.5, 21.8, 70.225, 80.112, 82.992, 84.15, 84.61, 84.85, 84.972, 85.027,
          85.055, 85.065, 85.07, 85.074, 85.077, 85.079, 85.08, 85.0805]


class Map:
    def __init__(self):
        self.scale = 2
        self.center = [56.188484, 58.007144]
        self.map_type = 'map'
        self.pt = None
        self.render()

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (0, 45), (700, 45), 5)
        self.image = pygame.image.load(
            io.BytesIO(load_map([str(self.center[0]), str(self.center[1])],
                                self.scale,
                                self.map_type,
                                pt=self.pt if self.pt else None)))

    def search(self, request):
        result = get_toponym(request)
        if result:
            result = get_coordinates(result)
            self.center = [float(result[0]), float(result[1])]
            self.pt = self.center.copy()


cur_map = Map()

text_input = text_input.TextInput(font_family='font.ttf', font_size=30,
                                  repeat_keys_initial_ms=300, repeat_keys_interval_ms=30)

clock = pygame.time.Clock()
running = True
pygame.key.set_repeat(10)
pressed = False


def make_labels(text_text, color, rotate=True):
    font = pygame.font.Font('font.ttf', 30)
    text = font.render("{}".format(text_text), 1, pygame.Color(color))
    screen.fill(pygame.Color('white'))
    screen.blit(text, (0, 0))
    image = screen.subsurface((0, 0, 80, 30)).copy()
    if rotate:
        return pygame.transform.rotate(image, 270)
    return image


scheme = make_labels('Схема', 'red')
sputnik = make_labels('Спутник', 'blue')
hybrid = make_labels('Гибрид', 'green')
search = make_labels('Искать', 'black', rotate=False)

while running:
    pygame.key.set_repeat(10)
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
                cur_map.center[1] -= scale * cos(radians(cur_map.center[1]))
            elif event.key == pygame.K_UP:
                cur_map.center[1] += scale * cos(radians(cur_map.center[1]))
            elif event.key == pygame.K_LEFT:
                cur_map.center[0] -= scale
            elif event.key == pygame.K_RIGHT:
                cur_map.center[0] += scale
            if event.key == pygame.K_KP_ENTER:
                cur_map.search(text_input.get_text())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if event.pos[0] in range(610, 710) and event.pos[1] in range(0, 40):
                    cur_map.search(text_input.get_text())
                elif event.pos[0] in range(650, 680):
                    if event.pos[1] in range(130, 210):
                        cur_map.map_type = 'map'
                    elif event.pos[1] in range(235, 315):
                        cur_map.map_type = 'sat'
                    elif event.pos[1] in range(370, 450):
                        cur_map.map_type = 'sat,skl'
                else:
                    pressed = True
                    start_pos = event.pos
            if event.button == pygame.BUTTON_WHEELUP:
                if cur_map.scale < 17:
                    cur_map.scale += 1
            if event.button == pygame.BUTTON_WHEELDOWN:
                if cur_map.scale > 1:
                    cur_map.scale -= 1

        if event.type == pygame.MOUSEMOTION and pressed:
            cur_map.center[0] += 0.02 * 18 / 2 ** (cur_map.scale - 2) * (start_pos[0] - event.pos[0])
            cur_map.center[1] -= cos(radians(cur_map.center[1])) * 0.02 * 18 / 2 ** \
                                 (cur_map.scale - 2) * (start_pos[1] - event.pos[1])
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            pressed = False

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

    screen.fill(pygame.Color('white'))
    cur_map.render()
    screen.blit(cur_map.image, (0, 50))

    screen.blit(scheme, (650, 110))
    screen.blit(sputnik, (650, 235))
    screen.blit(hybrid, (650, 370))

    pygame.key.set_repeat(0)
    text_input.update(events)
    screen.blit(text_input.get_surface(), (10, 10))

    pygame.draw.rect(screen, pygame.color.Color('white'), (610, 0, 100, 40))
    pygame.draw.rect(screen, pygame.color.Color('black'), (610, 0, 100, 40), 1)
    screen.blit(search, (620, 5))

    pygame.display.update()

pygame.quit()
