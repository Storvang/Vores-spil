#
#
#
#
#       Under ombygning
#
#
#
#

import pygame, math, os, glob
import miscClasses


MarkAnimation = []
for i in range(8):
    MarkAnimation.append(pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW_'+str(i)+".png")))


class Player(pygame.sprite.Sprite, miscClasses.GameObject):


    def __init__(self, position, speed, size, color, colliders, obstacles):
        self.jumb_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'jumb.ogg'))
        self.speed = pygame.Vector2(speed)
        self.color = color
        self.colliders = colliders
        self.obstacles = obstacles
        miscClasses.GameObject.__init__(self, position, size, MarkAnimation[1])

        self.anim = "running"
        self.pre_anim = None
        self.anim_time = 0


        self.grounded = False
        self.jump_g = 0.0080
        self.fall_g = 0.0090
        self.g = self.fall_g
        self.max_air_jumps = 1   # antal hop i luften
        self.air_jumps = self.max_air_jumps
        self.jump_power = 2
        self.double_jump_power = 2.1

        self.dead = False



        # self.Mark_img = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        # self.Mark_img = self.Mark_img.convert_alpha()
        # for i in range(8):
        #     MarkAnimation.append(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)' + str(i)))
        #     self.Mark_img.blit, (i, 0)






    def update(self, delta_time, speed, jump_pressed):


        # jump

        if self.grounded:
            self.air_jumps = self.max_air_jumps


        if jump_pressed and self.grounded:
            self.speed.y = -self.jump_power
            self.g = self.jump_g
            pygame.mixer.Sound.play(self.jumb_sound)

        elif jump_pressed and self.air_jumps > 0:
            self.speed.y = -self.double_jump_power
            self.g = self.jump_g
            self.air_jumps -= 1




        # update speed/position
        pre_y = self.position.y

        self.speed.x = speed
        self.position.x += self.speed.x * delta_time

        self.speed.y += self.g/2 * delta_time * speed
        self.position.y += self.speed.y * delta_time * speed # spilleren skal kun bevæge sig med den gennemsnitlige fart
        self.speed.y += self.g/2 * delta_time * speed

        # collisions
        if self.speed.y > 0:
            self.g = self.fall_g

            # Tjek om den er landet på noget
            foot_collider = pygame.Rect(round(self.position.x),
                                        round(pre_y + self.size.y),
                                        round(self.size.y),
                                        math.ceil((self.position.y + self.size.y) - (pre_y + self.size.y)))

            collision = foot_collider.collidelist(self.colliders)   # Collision er -1 hvis der ikke er nogen kollisioner
            was_over = pre_y + self.size.y <= self.colliders[collision].top
            if collision != -1 and was_over:
                self.position.y = self.colliders[collision].top - self.size.y
                self.speed.y = 0
                self.grounded = True
            else:
                self.grounded = False

        elif self.speed.y < 0:
            self.grounded = False

            # Tjek om den har stødt hovedet mod noget
            head_collider = pygame.Rect(round(self.position.x),
                                        round(pre_y),
                                        round(self.size.y),
                                        math.ceil(self.position.y - pre_y))

            collision = head_collider.collidelist(self.colliders)   # Collision er -1 hvis der ikke er nogen kollisioner
            was_under = pre_y >= self.colliders[collision].top
            if collision != -1 and was_under:
                self.position.y = self.colliders[collision].bottom
                self.speed.y = 0

        # death
        body_collider = pygame.Rect(round(self.position.x),
                                    round(self.position.y),
                                    round(self.size.x),
                                    round(self.size.y))

        collision = body_collider.collidelist(self.obstacles)
        if collision != -1 or self.position.y > 1130:
            self.dead = True

        # animation time
        if self.anim != self.pre_anim:
            self.anim_time = 0
        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

    def draw(self, screen, scroll, scale):

        # animations
        def running():
            self.image = MarkAnimation[math.floor((self.anim_time % 0.64) / 0.08)]

            # if self.image == MarkAnimation[0] or MarkAnimation[4]:
            #     pygame.mixer.music.load(os.path.join('Assets', 'Sounds', 'Footsteps', 'Footstep2.mp3'))

        # animate
        if self.anim is not None:
            anim_function = {'running': running}[self.anim]
            anim_function()

        miscClasses.GameObject.draw(self, screen, scroll, scale)





       # pygame.draw.rect(screen, self.color, render_rect)


