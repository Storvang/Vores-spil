import pygame
import os, pygame

platformmiddle = pygame.image.load(os.path.join("Assets","Platforms","Platform(Middle).png"))

class Platform:
    def __init__(self, position, size, colliders):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))

        self.colliders = colliders
        self.colliders.append(self.rect)

    def update(self, delta_time):
        pass

    #def draw():
        #win.blit(platformmiddle)

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(round((self.position.x - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        pygame.draw.rect(screen, (52, 64, 235), render_rect)


    def __del__(self):
        self.colliders.remove(self.rect)
