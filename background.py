import pygame
import random
import os
import miscClasses

Cloud1 = pygame.image.load(os.path.join("Assets", "Background", "Cloud_1.png"))
Cloud2 = pygame.image.load(os.path.join("Assets", "Background", "Cloud_2.png"))
Cloud3 = pygame.image.load(os.path.join("Assets", "Background", "Cloud_3.png"))






class Cloud(miscClasses.GameObject):
    def __init__(self, position, Clouds):
        self.number = random.randint(1,4)
        self.Clouds = Clouds
        if self.number==1:
            size = (32,32)
            miscClasses.GameObject.__init__(self, position, size, Cloud1)
        elif self.number==2:
            size = (32,32)
            miscClasses.GameObject.__init__(self, position, size, Cloud2)
        elif self.number==2:
            size = (32,32)
            miscClasses.GameObject.__init__(self, position, size, Cloud3)




#        GameObject.__init__(self, position, size, Cloud)

