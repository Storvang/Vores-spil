import pygame
import miscClasses
from playerClass import Player
from platformClass import Platform
import background

class GameInstance:
    def __init__(self, sfx):
        self.scroll = 0
        self.cam_speed = 700

        self.clouds = []
        self.colliders = []
        self.obstacles = []
        self.coins = []
        self.projectiles = []
        self.Ground = Platform(position=(0, 880), length=38, colliders=self.colliders)
        self.Ground2 = Platform(position=(1920, 700), length=60, colliders=self.colliders)
        self.Spike = miscClasses.Spike(position=(2000, 650), obstacles=self.obstacles)
        miscClasses.Coin(position=(2200, 500), channel=sfx, coins=self.coins)
        background.Cloud(position=(2200, 700), Clouds=self.clouds)

        self.Mark = Player(position=(300, -200),
                           speed=(self.cam_speed, 0),
                           size=(83, 111),
                           gun='shotgun',
                           channel=sfx,
                           colliders=self.colliders,
                           obstacles=self.obstacles,
                           coins=self.coins,
                           projectiles=self.projectiles)

    def update(self, delta_time, jump_pressed, shoot_pressed, sound_on):
        self.scroll += self.cam_speed * delta_time

        for projectile in self.projectiles:
            projectile.update(delta_time)
        self.Mark.update(delta_time, self.cam_speed, jump_pressed, shoot_pressed, sound_on)
        return self.Mark.coin_collected, self.Mark.dead


    def draw(self, screen, screen_scale):
        screen.fill((74, 228, 255))
        self.Ground.draw(screen, self.scroll, screen_scale)
        self.Ground2.draw(screen, self.scroll, screen_scale)
        self.Spike.draw(screen, self.scroll, screen_scale)
        for coin in self.coins:
            coin.draw(screen, self.scroll, screen_scale)
        for projectile in self.projectiles:
            projectile.draw(screen, self.scroll, screen_scale)
        for cloud in self.clouds:
            cloud.draw(screen, self.scroll, screen_scale)
        self.Mark.draw(screen, self.scroll, screen_scale)
