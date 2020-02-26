import pygame
import time
import player

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
scroll_y = 0


class Platform:
    def __init__(self, position, size, colliders):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)
        self.colliders = colliders
        self.colliders.append(self.rect)

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (52, 64, 235), self.rect)

    def __del__(self):
        self.colliders.remove(self.rect)


# init main loop
colliders = []
Mark = player.Player((300, 500), (0, 0), (25, 25), (66, 135, 245), colliders)
Ground = Platform((0, 600), (1280, 120), colliders)

min_delta_time = 0.003
delta_time = 0
pre_time = pygame.time.get_ticks() / 1000

quit_game = False

# main loop
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

    # update
    Ground.update(delta_time)
    Mark.update(delta_time)

    # draw
    screen.fill((255, 255, 255))
    Ground.draw(screen)
    Mark.draw(screen)
    pygame.display.flip()

    # delta time
    delta_time = (pygame.time.get_ticks() / 1000) - pre_time
    pre_time = (pygame.time.get_ticks() / 1000)
    if delta_time < min_delta_time:
        time.sleep(min_delta_time - delta_time)
        delta_time += (pygame.time.get_ticks() / 1000) - pre_time
        pre_time = (pygame.time.get_ticks() / 1000)
