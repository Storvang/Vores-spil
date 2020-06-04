import pygame, os
import miscClasses

platform_left_img = pygame.image.load(os.path.join("Assets", "Platforms", "Platform(Left end).png"))
platform_left_img = pygame.transform.scale(platform_left_img, (50, 50))

platform_middle_img = pygame.image.load(os.path.join("Assets", "Platforms", "Platform(Middle).png"))
platform_middle_img = pygame.transform.scale(platform_middle_img, (50, 50))

platform_right_img = pygame.image.load(os.path.join("Assets", "Platforms", "Platform(Right end).png"))
platform_right_img = pygame.transform.scale(platform_right_img, (50, 50))


class Platform(miscClasses.GameObject):
    def __init__(self, position, length, platforms):
        size = pygame.Vector2(length * 50, 50)

        # construct platform image
        image = pygame.Surface(size, pygame.SRCALPHA, 32)
        image = image.convert_alpha(image)
        image.blit(platform_left_img, (0, 0))
        for i in range(50, round(size.x - 50), 50):
            image.blit(platform_middle_img, (i, 0))
        image.blit(platform_right_img, (size.x - 50, 0))

        miscClasses.GameObject.__init__(self, position, size, image)
        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))

        self.platforms = platforms
        self.platforms.append(self)
