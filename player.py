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
        self.jump_g = 8000.0
        self.fall_g = 9000.0
        self.g = self.fall_g
        self.max_double_jumps = 3   # antal hop i luften
        self.double_jumps = self.max_double_jumps
        self.jump_power = 2000
        self.double_jump_power = 2000

    def update(self, delta_time, space_pressed):
        pre_y = self.position.y

        self.speed.y += self.g/2 * delta_time
        self.position += self.speed * delta_time    # spilleren skal kun bevæge sig med den gennemsnitlige fart
        self.speed.y += self.g/2 * delta_time

        if self.speed.y > 0:
            self.g = self.fall_g

            # Tjek om den er landet på noget
            foot_collider = pygame.Rect(round(self.position.x), round(pre_y + self.size.y), round(self.size.y), 0)
            foot_collider.height = math.ceil((self.position.y + self.size.y) - (pre_y + self.size.y))
            collision = foot_collider.collidelist(self.colliders)   # Collision er -1 hvis der ikke er nogen kollisioner
            if collision != -1 and (pre_y + self.size.y <= self.colliders[collision].top):
                self.position.y = self.colliders[collision].top - self.size.y
                self.speed.y = 0
                self.grounded = True
            else:
                self.grounded = False

        elif self.speed.y < 0:
            self.grounded = False

            # Tjek om den har stødt hovedet mod noget
            head_collider = pygame.Rect(round(self.position.x), round(pre_y), round(self.size.y), 0)
            head_collider.height = math.ceil(self.position.y - pre_y)
            collision = head_collider.collidelist(self.colliders)   # Collision er -1 hvis der ikke er nogen kollisioner
            if not collision == -1 and (pre_y >= self.colliders[collision].top):
                self.position.y = self.colliders[collision].bottom
                self.speed.y = 0

        # jump
        if space_pressed and self.grounded:
            self.speed.y = -self.jump_power
            self.g = self.jump_g
            self.double_jumps = self.max_double_jumps

        elif space_pressed and self.double_jumps > 0:
            self.speed.y = -self.double_jump_power
            self.g = self.jump_g
            self.double_jumps -= 1

        #if key_input[pygame.K_SPACE] and self.grounded:
        #    self.speed.y = -self.jump_power
        #    self.g = self.jump_g
        #elif not key_input[pygame.K_SPACE]:
        #    self.g = self.fall_g

    def draw(self, screen, scroll, scale):

        render_rect = pygame.Rect(round((self.position.x - scroll) * scale),
                                  round(self.position.y * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        pygame.draw.rect(screen, self.color, render_rect)
