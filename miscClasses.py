import pygame
import os
import math


class GameObject:
    def __init__(self, position, size, image, direction=0):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.image = image

        self.direction = direction

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(round((self.position.x - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        render_img = pygame.transform.scale(self.image, render_rect.size)
        render_img = pygame.transform.rotate(render_img, self.direction)
        screen.blit(render_img, render_rect.topleft)


spike_img = pygame.image.load(os.path.join('Assets', 'Spike.png'))


class Spike(GameObject):
    def __init__(self, position, spikes):
        size = (50, 50)
        self.spikes = spikes
        GameObject.__init__(self, position, size, spike_img)

        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))
        self.spikes.append(self)


coin_animation = []
for i in range(8):
    coin_animation.append(pygame.image.load(os.path.join('Assets', 'Coin', 'coin_' + str(i) + '.png')))
coin_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'coin.wav'))


class Coin(GameObject):
    def __init__(self, position, coins, global_coins):
        size = (100, 100)
        self.coins = coins
        self.global_coins = global_coins
        GameObject.__init__(self, position, size, coin_animation[0])

        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))
        self.coins.append(self)

        self.anim_time = 0

    def collect(self, sound_on):
        if sound_on:
            coin_sound.play()
        self.coins.remove(self)
        self.global_coins.remove(self)

    def update(self, delta_time):
        self.anim_time += delta_time

    def draw(self, screen, scroll, scale):
        self.image = coin_animation[math.floor((self.anim_time % 0.64) / 0.08)]
        GameObject.draw(self, screen, scroll, scale)
