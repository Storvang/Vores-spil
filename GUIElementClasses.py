import pygame, math


class Image:
    def __init__(self, position, size, image):
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.image = image

    def draw(self, screen, scale, offset):
        render_rect = pygame.Rect(round((self.position.x + offset.x) * scale),
                                  round((self.position.y + offset.y) * scale),
                                  round(self.size.x * scale),
                                  round(self.size.y * scale))

        render_img = pygame.transform.scale(self.image, render_rect.size)
        screen.blit(render_img, render_rect.topleft)


class Button(Image):
    def __init__(self, position, size, images):
        self.images = images
        Image.__init__(self, position, size, images[0])

        self.anim = None
        self.pre_anim = None
        self.anim_time = 0  # tid siden animationen gik igang
        self.anim_offset = pygame.Vector2(0, 0)     # positionen i animationen

    def update(self, mouse_pos, mouse_down, delta_time):
        mouse_over_x = self.position.x < mouse_pos.x < self.position.x + self.size.x
        mouse_over_y = self.position.y < mouse_pos.y < self.position.y + self.size.y
        mouse_over = mouse_over_x and mouse_over_y

        button_clicked = False
        if mouse_over and mouse_down:
            self.image = self.images[2]
            button_clicked = True
        elif mouse_over and not mouse_down:
            self.image = self.images[1]
            self.anim = 'mouse_over'
        elif not mouse_over:
            self.image = self.images[0]
            self.anim = 'mouse_not_over'

        # animation time
        if self.anim != self.pre_anim:
            self.anim_time = 0
        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

        return button_clicked

    def draw(self, screen, scale, offset):
        # animations
        def mouse_over():
            if self.anim_time <= 0.1:
                self.anim_offset = pygame.Vector2(0, self.anim_time * -100)

        def mouse_not_over():
            if self.anim_time <= 0.1:
                self.anim_offset = pygame.Vector2(0, self.anim_time * 100 - 10)

        # animate
        if self.anim is not None:
            anim_function = {'mouse_over': mouse_over,
                             'mouse_not_over': mouse_not_over}[self.anim]
            anim_function()

        # render
        Image.draw(self, screen, scale, offset + self.anim_offset)
