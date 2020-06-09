import pygame
import os
import math

from miscClasses import GameObject

Enemy1_idle = []
for i in range(8):
    Enemy1_idle.append(pygame.image.load(os.path.join('Assets', 'Enemies', 'Enemy1', 'Enemy1_'+str(i)+".png")))


class Enemy(GameObject):
    def __init__(self, position, enemies, global_enemies, projectiles):
        self.enemies = enemies
        self.global_enemies = global_enemies
        self.enemies.append(self)

        self.projectiles = projectiles

        size = (100, 100)
        GameObject.__init__(self, position, size, Enemy1_idle[0])

        self.rect = pygame.Rect(round(self.position.x), round(self.position.y), round(self.size.x), round(self.size.y))

        # animation
        self.anim = "idle"
        self.pre_anim = None
        self.anim_time = 0

    def update(self, delta_time):
        for projectile in self.projectiles:
            hit, hit_side, intersection = projectile.collide_rect(self.rect)
            if hit:
                self.enemies.remove(self)
                self.global_enemies.remove(self)
                break

        # anim time
        if self.anim != self.pre_anim:
            self.anim_time = 0

        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

    def draw(self, screen, scroll, scale):

        # animations
        def idle():
            self.image = Enemy1_idle[math.floor((self.anim_time % 0.64) / 0.08)]

        # animate
        if self.anim is not None:
            anim_function = {'idle': idle}[self.anim]
            anim_function()

        GameObject.draw(self, screen, scroll, scale)
