import pygame


pygame.init()
screen = pygame.display.set_mode((400, 300))
done = false
scroll_y = 0


class Player:
    def __init__(self, pos, weapon):
        pass

    def update(self, delta_time):
        pass


class Platform:
    def __init__(self, y_pos, length):
        pass

    def update(self, delta_time):
        pass


Mark = Player((0, 0), 0)

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            True

    Mark.update

XXXX

# Bare lige for at tjekke om git virker... Jaaa det virkede...ogsåfor mig