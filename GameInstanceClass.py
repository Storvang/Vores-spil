import pygame
import miscClasses
from playerClass import Player
from platformClass import Platform


class GameInstance:
    def __init__(self, ):
        self.scroll = 0
        self.cam_speed = 700

        self.colliders = []
        self.obstacles = []
        self.coins = []
        self.Ground = Platform(position=(0, 880), length=38, colliders=self.colliders)
        self.Ground2 = Platform(position=(1920, 700), length=60, colliders=self.colliders)
        self.Spike = miscClasses.Spike(position=(2000, 650), obstacles=self.obstacles)
        miscClasses.Coin(position=(2200, 500), coins=self.coins)

        self.Mark = Player(position=(300, -200),
                           speed=(self.cam_speed, 0),
                           size=(95, 115),
                           color=(255, 0, 242),
                           colliders=self.colliders,
                           obstacles=self.obstacles,
                           coins=self.coins)

    def update(self, delta_time, space_pressed):
        self.scroll += self.cam_speed * delta_time

        self.Mark.update(delta_time, self.cam_speed, space_pressed)
        return self.Mark.coin_collected, self.Mark.dead

    def draw(self, screen, screen_scale):
        screen.fill((74, 228, 255))
        self.Ground.draw(screen, self.scroll, screen_scale)
        self.Ground2.draw(screen, self.scroll, screen_scale)
        self.Spike.draw(screen, self.scroll, screen_scale)
        for coin in self.coins:
            coin.draw(screen, self.scroll, screen_scale)
        self.Mark.draw(screen, self.scroll, screen_scale)
