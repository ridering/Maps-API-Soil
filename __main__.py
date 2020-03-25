import pygame
import text_input
import io
from request_image import load_map
from request_coordinate import get_coordinates, get_toponym
from math import cos, radians

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 60

SCALES = [-79.5, 21.8, 70.225, 80.112, 82.992, 84.15, 84.61, 84.85, 84.972, 85.027,
          85.055, 85.065, 85.07, 85.074, 85.077, 85.079, 85.08, 85.0805]
clock = pygame.time.Clock()
running = True
pressed = False
buttons = pygame.sprite.Group()


class Map:
    def __init__(self):
        self.scale = 2
        self.center = [56.188484, 58.007144]
        self.map_type = 'map'
        self.pt = None
        self.render()

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (0, 45), (width, 45), 5)
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


class Button(pygame.sprite.Sprite):
    def __init__(self, text_text, color, x, y, bg_color='white', angle=0, font_size=30):
        super().__init__(buttons)

        self.width, self.height = self.get_size(text_text, font_size)
        if angle == 270:
            self.rect = pygame.Rect(x, y, self.height, self.width)
        else:
            self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

        self.static = self.make_button(text_text, color, bg_color, angle, self.width, self.height)
        self.active = self.make_button(text_text, color, 'yellow', angle, self.width, self.height)
        self.image = self.static

        self.text = text_text.strip()

    def get_size(self, text_text, font_size):
        self.font = pygame.font.Font('font.ttf', font_size)
        return pygame.font.Font.size(self.font, text_text)

    def make_button(self, text_text, color, bg_color, angle, but_width, but_height):
        text = self.font.render("{}".format(text_text), 1, pygame.Color(color))
        screen.fill(pygame.Color(bg_color))
        screen.blit(text, (0, 0))
        pygame.draw.rect(screen, pygame.color.Color(color), (0, 0, but_width, but_height), 1)
        image = screen.subsurface((0, 0, but_width, but_height)).copy()
        return pygame.transform.rotate(image, angle)


cur_map = Map()
scheme = Button('  Схема  ', 'red', width - 50, height - 390, angle=270)
sputnik = Button('  Спутник  ', 'blue', width - 50, height - 265, angle=270)
hybrid = Button('  Гибрид  ', 'green', width - 50, height - 130, angle=270)
search = Button('  Искать  ', 'black', width - 90, 5)
cancel = Button('  Сброс поискового результата  ', 'black', width - 287, 50)
text_input = text_input.TextInput(font_family='font.ttf', font_size=30,
                                  repeat_keys_initial_ms=400, repeat_keys_interval_ms=30)


def make_action(button):
    if button == 'Искать':
        cur_map.search(text_input.get_text())
        search.image = search.active
    if button == 'Схема':
        cur_map.map_type = 'map'
        scheme.image = scheme.active
    if button == 'Спутник':
        cur_map.map_type = 'sat'
        sputnik.image = sputnik.active
    if button == 'Гибрид':
        cur_map.map_type = 'sat,skl'
        hybrid.image = hybrid.active
    if button == 'Сброс поискового результата':
        cancel.image = cancel.active
        cur_map.pt = None


while running:
    clock.tick(FPS)
    events = pygame.event.get()

    text_input.update(events)
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
                for button in buttons:
                    if button.rect.collidepoint(*event.pos):
                        make_action(button.text)
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
            for button in buttons:
                button.image = button.static

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
    screen.blit(cur_map.image, (width - 700, 50))

    screen.blit(text_input.get_surface(), (10, 10))
    buttons.draw(screen)
    buttons.update()

    pygame.display.update()

pygame.quit()
