import pygame


class Platform:
    def __init__(self, position, size, colliders):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))
        self.colliders = colliders
        self.colliders.append(self.rect)

    def update(self, delta_time):
        pass

    def draw(self, screen, scroll):
        render_rect = pygame.Rect((round(self.rect.x - scroll), round(self.rect.y)), self.rect.size)
        pygame.draw.rect(screen, (52, 64, 235), render_rect)

    def __del__(self):
        self.colliders.remove(self.rect)
