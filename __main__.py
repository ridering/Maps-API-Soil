import pygame
import text_input


class Map:
    def __init__(self):
        pass

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (480, 0), (480, 500), 5)
        pygame.draw.line(screen, pygame.Color("red"), (0, 45), (700, 45), 5)


# if __name__ == "__main__":

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 80

cur_map = Map()

# Create TextInput-object
text_input = text_input.TextInput()

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('white'))

    # Feed it with events every frame
    text_input.update(events)
    # Blit its surface onto the screen
    screen.blit(text_input.get_surface(), (10, 10))
    # pygame.display.flip()
    cur_map.render()

    pygame.display.update()

pygame.quit()
