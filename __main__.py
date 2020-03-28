from math import cos, radians

import pygame

import text_input
from distance import lonlat_distance
from request_coordinate import get_toponym, get_org_pos, get_organization

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
labels = pygame.sprite.Group()

from classes.button import Button
from classes.labl import Label
from classes.map import Map

cur_map = Map()
result = Label('', 'black', 10, 60)
scheme = Button('  Схема  ', 'red', width - 50, height - 390, angle=270)
sputnik = Button('  Спутник  ', 'blue', width - 50, height - 265, angle=270)
hybrid = Button('  Гибрид  ', 'green', width - 50, height - 130, angle=270)
search = Button('  Искать  ', 'black', width - 90, 5, )
post = Button('  Почтовый индекс  ', 'black', width - 470, 50)

cancel = Button('  Сброс поискового результата  ', 'black', width - 287, 50)
text_input = text_input.TextInput(font_family='font.ttf', font_size=30,
                                  repeat_keys_initial_ms=400, repeat_keys_interval_ms=30)


def make_action(button):
    if button == 'Искать':
        cur_map.search(text_input.get_text())
        search.image = search.active
        result.make_text(cur_map.address, 'black', 'white')
    if button == 'Почтовый индекс':
        if post.p:
            post.p = False
            result.make_text(cur_map.address, 'black', 'white')
            post.image = post.active
        else:
            result.make_text(cur_map.address + ' ' + cur_map.postal_code, 'black', 'white')
            post.image = post.active
            post.p = True
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
        cur_map.address = None
        cur_map.postal_code = ''
        text_input.clear_text()


def new_coor(pos):
    x, y = pix_to_rad(pos)
    cur_map.pt = [x, y]
    top = get_toponym(str(x) + ',' + str(y))
    if top:
        cur_map.show_address(top)
    if post.p:
        result.make_text(cur_map.address, 'black', 'white')
    else:
        result.make_text(cur_map.address + ' ' + cur_map.postal_code, 'black', 'white')


def check_coor():
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


def pix_to_rad(pos):
    pix_x = pos[0] - 650 / 2
    pix_y = pos[1] - 50 - 450 / 2
    x = cur_map.center[0] + pix_x * scale_x / 650
    y = cur_map.center[1] - pix_y * scale_y / 450 * cos(radians(cur_map.center[1]))
    return x, y


def find_org(pos):
    x, y = pix_to_rad(pos)
    org = get_organization((str(x), str(y)), text_input.get_text())
    org_x, org_y = get_org_pos(org)
    distance = lonlat_distance((x, y), (org_x, org_y))
    if distance <= 50:
        cur_map.pt = [org_x, org_y]
        top = get_toponym(str(org_x) + ',' + str(org_y))
        if top:
            cur_map.show_address(top)
        if post.p:
            result.make_text(org['properties']['name'] + ' ' + cur_map.address, 'black', 'white')
        else:
            result.make_text(org['properties']['name'] + ' ' + cur_map.address + ' ' + cur_map.postal_code, 'black',
                             'white')


while running:
    clock.tick(FPS)
    events = pygame.event.get()

    text_input.update(events)
    scale_x = 360 / (2 ** (cur_map.scale + 8)) * 650
    scale_y = 360 / (2 ** (cur_map.scale + 8)) * 450
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
                cur_map.center[1] -= scale_y * cos(radians(cur_map.center[1]))
            elif event.key == pygame.K_UP:
                cur_map.center[1] += scale_y * cos(radians(cur_map.center[1]))
            elif event.key == pygame.K_LEFT:
                cur_map.center[0] -= scale_x
            elif event.key == pygame.K_RIGHT:
                cur_map.center[0] += scale_x
            if event.key == pygame.K_KP_ENTER:
                cur_map.search(text_input.get_text())
                result.make_text(cur_map.address, 'black', 'white')

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                flag = False
                for button in buttons:
                    if button.rect.collidepoint(*event.pos):
                        make_action(button.text)
                        flag = True
                pressed = True
                start_pos = event.pos
                if not flag and event.pos[0] < 650 and event.pos[1] > 50:
                    new_coor(event.pos)
            if event.button == pygame.BUTTON_RIGHT:
                if event.pos[0] < 650 and event.pos[1] > 50 and text_input.get_text() != '':
                    find_org(event.pos)

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

    check_coor()

    screen.fill(pygame.Color('white'))
    cur_map.render()
    screen.blit(cur_map.image, (width - 700, 50))

    screen.blit(text_input.get_surface(), (10, 10))
    buttons.draw(screen)
    buttons.update()
    if cur_map.address:
        # pygame.draw.rect(screen, pygame.color.Color('white'), (10, 60, 200, 430))
        labels.draw(screen)
        labels.update()

    pygame.display.update()

pygame.quit()
