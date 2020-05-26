import pygame, os, math


class GameObject:
    def __init__(self, position, size, image, direction=0):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.image = image

        self.direction = direction

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(round((self.position.x + - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        render_img = pygame.transform.scale(self.image, render_rect.size)
        render_img = pygame.transform.rotate(render_img, self.direction)
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


coin_img = pygame.image.load(os.path.join('Assets', 'Dogecoin.png'))
coin_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'coin.wav'))


class Coin(GameObject):
    def __init__(self, position, channel, coins):
        size = (100, 100)
        self.coins = coins
        GameObject.__init__(self, position, size, coin_img)

        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))
        self.coins.append(self)

        self.channel = channel

    def collect(self):
        self.channel.play(coin_sound)
        self.coins.remove(self)


class Enemy:
    def __init__(self, position):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen, scroll, scale):
        pass
