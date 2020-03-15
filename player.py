import pygame
import math


class Player:
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

    def update(self, delta_time, speed, space_pressed):

        # jump
        if space_pressed and self.grounded:
            self.speed.y = -self.jump_power
            self.g = self.jump_g
            self.air_jumps = self.max_air_jumps

        elif space_pressed and self.air_jumps > 0:
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

        pygame.draw.rect(screen, self.color, render_rect)
