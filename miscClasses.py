import pygame, os


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


spike_img = pygame.image.load(os.path.join('Assets', 'Spike.png'))


class Spike(GameObject):
    def __init__(self, position, obstacles):
        size = (50, 50)
        self.obstacles = obstacles
        GameObject.__init__(self, position, size, spike_img)

        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))
        self.obstacles.append(self.rect)

    def __del__(self):
        self.obstacles.remove(self.rect)


class Coin:
    def __init__(self, position):
        pass

    def update(self):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Enemy:
    def __init__(self, position):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Gun:
    def __init__(self):
        pass

    def update(self, position, shoot_pressed):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Projectile:
    def __init__(self, position, rotation):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen, scroll, scale):
        pass
