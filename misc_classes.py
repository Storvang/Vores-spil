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

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(0, 0, 0, 0)
        render_rect.x = round((self.position.x - scroll) * scale)
        render_rect.y = round(self.position.y * scale)
        render_rect.width = round(self.size.x * scale)
        render_rect.height = round(self.size.y * scale)

        pygame.draw.rect(screen, (52, 64, 235), render_rect)

    def __del__(self):
        self.colliders.remove(self.rect)
