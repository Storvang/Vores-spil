import pygame, os, math, random
import miscClasses, projectileClass


# findes kun for at have en navngivet liste af animationer
class GunAnimationCollection:
    def __init__(self, shooting, running):
        self.shooting = shooting
        self.running = running


class Gun(miscClasses.GameObject):
    def __init__(self, player_position, size, animations, cool_down, socket_offset, colliders):
        self.animations = animations
        self.socket_offset = pygame.Vector2(socket_offset)
        self.colliders = colliders
        miscClasses.GameObject.__init__(self, player_position + self.socket_offset, size, animations.running[0])

        self.shooting = False
        self.cool_down = cool_down
        self.current_cool_down = 0.0

        self.anim = "running"
        self.pre_anim = None
        self.anim_time = 0
        self.anim_duration = 0.05 * len(self.animations.shooting)

    def shoot(self, projectile_list):
        projectileClass.Projectile(position=self.position + pygame.Vector2(159, 10),
                                   direction=0,
                                   speed=3500,
                                   range=1000,
                                   projectiles=projectile_list,
                                   colliders=self.colliders)

    def update(self, player_position, player_animation, player_anim_time, shoot_pressed, projectile_list, delta_time):
        self.position = player_position + self.socket_offset

        if shoot_pressed and not self.shooting:
            self.shooting = True
            self.anim = 'shooting'
            self.current_cool_down = self.cool_down
            self.shoot(projectile_list)

        elif self.shooting:
            if self.current_cool_down <= 0:
                self.shooting = False
            else:
                self.current_cool_down -= delta_time

        # animation time
        if self.anim == 'shooting':
            if self.pre_anim != 'shooting':
                self.anim_time = 0
            else:
                self.anim_time += delta_time
                if self.anim_time >= self.anim_duration:
                    self.anim = player_animation
                    self.anim_time = player_anim_time
        else:
            self.anim_time = player_anim_time
        self.pre_anim = self.anim

    def draw(self, screen, scroll, scale):
        # animations
        def shooting():
            self.image = self.animations.shooting[math.floor(self.anim_time / 0.05)]

        def running():
            self.image = self.animations.running[math.floor((self.anim_time % 0.64) / 0.08)]

        # animate
        if self.anim is not None:
            anim_function = {'shooting': shooting,
                             'running': running}[self.anim]
            anim_function()

        # render
        miscClasses.GameObject.draw(self, screen, scroll, scale)


shotgun_shooting = []
for i in range(9):
    path = os.path.join('Assets', 'Guns', 'Shotgun', 'Shooting', 'Shotgun Shooting' + str(i) + '.png')
    shotgun_shooting.append(pygame.image.load(path))

shotgun_running = []
for i in range(8):
    path = os.path.join('Assets', 'Guns', 'Shotgun', 'Running', 'Shotgun Running' + str(i) + '.png')
    shotgun_running.append(pygame.image.load(path))

shotgun_animations = GunAnimationCollection(shotgun_shooting, shotgun_running)

shotgun_shot_sfx = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'Guns', 'Shotgun Shot.wav'))


class Shotgun(Gun):
    def __init__(self, player_position, channel, colliders):
        Gun.__init__(self, player_position, (159, 44), shotgun_animations, 0.5, (-12, 32), colliders)
        self.channel = channel

    def shoot(self, projectile_list):
        shotgun_shot_sfx.play()

        for _ in range(7):
            projectileClass.Projectile(position=self.position + pygame.Vector2(159, 10),
                                       direction=random.randint(-20, 20),
                                       speed=random.randint(3000, 4000),
                                       range=random.randint(1000, 1100),
                                       channel=self.channel,
                                       projectiles=projectile_list,
                                       colliders=self.colliders)
