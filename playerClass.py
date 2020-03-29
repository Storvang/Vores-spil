import pygame, math, os



MarkFrame1 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW1.png'))
MarkFrame1 = pygame.transform.scale(MarkFrame1, (40, 40))

MarkFrame2 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW2.png'))
MarkFrame2 = pygame.transform.scale(MarkFrame2, (40, 40))

MarkFrame3 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW3.png'))
MarkFrame3 = pygame.transform.scale(MarkFrame3, (40, 40))

MarkFrame4 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW4.png'))
MarkFrame4 = pygame.transform.scale(MarkFrame4, (40, 40))

MarkFrame5 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW5.png'))
MarkFrame5 = pygame.transform.scale(MarkFrame5, (40, 40))

MarkFrame6 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW6.png'))
MarkFrame6 = pygame.transform.scale(MarkFrame6, (40, 40))

MarkFrame7 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW7.png'))
MarkFrame7 = pygame.transform.scale(MarkFrame7, (40, 40))

MarkFrame8 = pygame.image.load(os.path.join('Assets', 'MarkFrames', 'RunningMark(NW)', 'MarkNW8.png'))
MarkFrame8 = pygame.transform.scale(MarkFrame8, (40, 40))

MarkAnimantion = [MarkFrame1, MarkFrame2, MarkFrame3, MarkFrame4, MarkFrame5, MarkFrame6, MarkFrame7, MarkFrame8]



class Player(pygame.sprite.Sprite):
    def __init__(self, position, speed, size, color, colliders):
        self.position = pygame.Vector2(position)
        self.speed = pygame.Vector2(speed)
        self.size = pygame.Vector2(size)
        self.color = color
        self.colliders = colliders


        self.grounded = False
        self.jump_g = 0.0080
        self.fall_g = 0.0090
        self.g = self.fall_g
        self.max_air_jumps = 1   # antal hop i luften
        self.air_jumps = self.max_air_jumps
        self.jump_power = 2
        self.double_jump_power = 2.1


        for M in MarkAnimantion:
                self.Mark_img = pygame.Surface(self.size, pygame.SRCALPHA, 32)
                self.Mark_img = self.Mark_img.convert_alpha()
                self.Mark_img.blit(M, (0, 0))









    def update(self, delta_time, speed, jump_pressed):

        # jump
        if self.grounded:
            self.air_jumps = self.max_air_jumps

        if jump_pressed and self.grounded:
            self.speed.y = -self.jump_power
            self.g = self.jump_g

        elif jump_pressed and self.air_jumps > 0:
            self.speed.y = -self.double_jump_power
            self.g = self.jump_g
            self.air_jumps -= 1

        # update speed/position
        pre_y = self.position.y

        self.speed.x = speed
        self.position.x += self.speed.x * delta_time

        self.speed.y += self.g/2 * delta_time * speed
        self.position.y += self.speed.y * delta_time * speed   # spilleren skal kun bevæge sig med den gennemsnitlige fart
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
            if not collision == -1 and was_under:
                self.position.y = self.colliders[collision].bottom
                self.speed.y = 0

    def draw(self, screen, scroll, scale):
        render_rect = pygame.Rect(round((self.position.x - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        render_img = pygame.transform.scale(self.Mark_img, render_rect.size)
        screen.blit(render_img, render_rect.topleft)



        #pygame.draw.rect(screen, self.color, render_rect)


