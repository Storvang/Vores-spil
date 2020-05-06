Cloud1 = pygame.image.load(os.path.join("Assets", "Baggrund", "Cloud_1.png"))
Cloud2 = pygame.image.load(os.path.join("Assets", "Baggrund", "Cloud_2.png"))
Cloud3 = pygame.image.load(os.path.join("Assets", "Baggrund", "Cloud_3.png"))
import random

import random




  class GameObject:
    def __init__(self, position, size, image):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.image = image

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(round((self.position.x - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        render_img = pygame.transform.scale(self.image, render_rect.size)
        screen.blit(render_img, render_rect.topleft)

class Cloud_(GameObject):
    def __init__(self, position):
        self.number = random.randint(1,4)
        if self.number==1:
            size = (32,32)
            GameObject.__init__(self, position, size, Cloud1)
        elif self.number==2:
            size = (32,32)
            GameObject.__init__(self, position, size, Cloud2)
        elif self.number==2:
            size = (32,32)
            GameObject.__init__(self, position, size, Cloud3)



#        GameObject.__init__(self, position, size, Cloud)

        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))