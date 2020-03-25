import pygame, os

platform_left_img = pygame.image.load(os.path.join("Assets", "Platforms", "Platform(Left end).png"))
platform_left_img = pygame.transform.scale(platform_left_img, (50, 50))

platform_middle_img = pygame.image.load(os.path.join("Assets", "Platforms", "Platform(Middle).png"))
platform_middle_img = pygame.transform.scale(platform_middle_img, (50, 50))

platform_right_img = pygame.image.load(os.path.join("Assets", "Platforms", "Platform(Right end).png"))
platform_right_img = pygame.transform.scale(platform_right_img, (50, 50))


class Platform:
    def __init__(self, position, length, colliders):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(length * 50, 50)
        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))

        self.colliders = colliders
        self.colliders.append(self.rect)

        # construct platform image
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.image.blit(platform_left_img, (0, 0))
        for i in range(50, self.rect.width - 50, 50):
            self.image.blit(platform_middle_img, (i, 0))
        self.image.blit(platform_right_img, (self.size.x - 50, 0))

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(round((self.position.x - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        render_img = pygame.transform.scale(self.image, render_rect.size)
        screen.blit(render_img, render_rect.topleft)

    def __del__(self):
        self.colliders.remove(self.rect)
