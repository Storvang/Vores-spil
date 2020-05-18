import pygame, math, os, glob
import miscClasses, Guns

jump_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'jump2.wav'))

MarkAnimation = []
for i in range(8):
    MarkAnimation.append(pygame.image.load(os.path.join('Assets', 'MarkFrames', 'Running', 'Mark Body Running' + str(i) + ".png")))


class Player(pygame.sprite.Sprite, miscClasses.GameObject):
    def __init__(self, position, speed, size, gun, channel, colliders, obstacles, coins):
        self.speed = pygame.Vector2(speed)
        self.channel = channel
        self.colliders = colliders
        self.obstacles = obstacles
        self.coins = coins
        self.coin_rects = []
        for coin in coins:
            self.coin_rects.append(coin.rect)
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

        self.coin_collected = False
        self.dead = False

        gun_type = {'shotgun': Guns.Shotgun}[gun]
        self.gun = gun_type(self.position)


    def update(self, delta_time, speed, jump_pressed):
        # jump
        if self.grounded:
            self.air_jumps = self.max_air_jumps

        if jump_pressed and self.grounded:
            self.speed.y = -self.jump_power
            self.g = self.jump_g
            self.channel.play(jump_sound)

        elif jump_pressed and self.air_jumps > 0:
            self.speed.y = -self.double_jump_power
            self.g = self.jump_g
            self.channel.play(jump_sound)
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
            foot_collider = pygame.Rect(math.ceil(self.position.x),
                                        math.ceil(pre_y + self.size.y),
                                        math.ceil(self.size.y),
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
            head_collider = pygame.Rect(math.ceil(self.position.x),
                                        math.ceil(pre_y),
                                        math.ceil(self.size.y),
                                        math.ceil(self.position.y - pre_y))

            collision = head_collider.collidelist(self.colliders)   # Collision er -1 hvis der ikke er nogen kollisioner
            was_under = pre_y >= self.colliders[collision].top
            if collision != -1 and was_under:
                self.position.y = self.colliders[collision].bottom
                self.speed.y = 0

        # coins
        body_collider = pygame.Rect(math.ceil(self.position.x),
                                    math.ceil(self.position.y),
                                    math.ceil(self.size.x),
                                    math.ceil(self.size.y))

        collision = body_collider.collidelist(self.coin_rects)
        if collision != -1:
            self.coin_collected = True
            del self.coin_rects[collision]

            collided_coin = self.coins[collision]
            collided_coin.collect()
        else:
            self.coin_collected = False

        # death
        collision = body_collider.collidelist(self.obstacles)
        if collision != -1 or self.position.y > 1130:
            self.dead = True

        # gun
        self.gun.update(self.position, self.anim, False, delta_time)

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

        # animate
        if self.anim is not None:
            anim_function = {'running': running}[self.anim]
            anim_function()

        # render player and gun
        miscClasses.GameObject.draw(self, screen, scroll, scale)
        self.gun.draw(screen, scroll, scale)
