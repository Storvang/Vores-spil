import pygame, os, math
from miscClasses import GameObject


# findes kun for at have en navngivet liste af animationer
class GunAnimationCollection:
    def __init__(self, running):
        self.running = running


class Gun(GameObject):
    def __init__(self, player_position, size, animations, cooldown_time, offset):
        self.animations = animations
        self.offset = pygame.Vector2(offset)
        GameObject.__init__(self, player_position + self.offset, size, animations.running[0])

        self.shooting = False
        self.cool_down = cooldown_time
        self.current_cool_down = 0.0

        self.anim = "running"
        self.pre_anim = None
        self.anim_time = 0

    def shoot(self):
        pass

    def update(self, player_position, player_animation, shoot_pressed, delta_time):
        self.position = player_position + self.offset

        if shoot_pressed and not self.shooting:
            self.shooting = True
            self.current_cool_down = self.cool_down
            self.shoot()

        elif self.shooting:
            if self.current_cool_down <= 0:
                self.shooting = True
            else:
                self.current_cool_down -= delta_time

        # animation time
        if self.anim != self.pre_anim:
            self.anim_time = 0
        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

    def draw(self, screen, scroll, scale):
        # animations
        def running():
            self.image = self.animations.running[math.floor((self.anim_time % 0.64) / 0.08)]

        # animate
        if self.anim is not None:
            anim_function = {'running': running}[self.anim]
            anim_function()

        # render
        GameObject.draw(self, screen, scroll, scale)


shotgun_running = []
for i in range(8):
    path = os.path.join('Assets', 'Guns', 'Shotgun', 'Running', 'Shotgun Running' + str(i) + '.png')
    shotgun_running.append(pygame.image.load(path))

shotgun_animations = GunAnimationCollection(shotgun_running)


class Shotgun(Gun):
    def __init__(self, player_position):
        Gun.__init__(self, player_position, (159, 44), shotgun_animations, 1, pygame.Vector2(-12, 32))
