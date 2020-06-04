import pygame
import random
import os
import miscClasses

Cloud1 = pygame.image.load(os.path.join("Assets", "Background", "Cloud_1.png"))
Cloud2 = pygame.image.load(os.path.join("Assets", "Background", "Cloud_2.png"))
Cloud3 = pygame.image.load(os.path.join("Assets", "Background", "Cloud_3.png"))


class Cloud(miscClasses.GameObject):
    def __init__(self, position, clouds):
        self.number = random.randint(1, 3)
        self.clouds = clouds
        size = (500, 500)
        if self.number == 1:
            miscClasses.GameObject.__init__(self, position, size, Cloud1)
        elif self.number == 2:
            miscClasses.GameObject.__init__(self, position, size, Cloud2)
        elif self.number == 3:
            miscClasses.GameObject.__init__(self, position, size, Cloud3)

        self.clouds.append(self)
