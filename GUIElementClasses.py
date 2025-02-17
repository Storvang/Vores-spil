import pygame


class Image:
    def __init__(self, position, size, image, list, alpha=255):
        list.append(self)
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(size)
        self.image = image
        self.alpha = alpha

        self.show = True

    def draw(self, screen, scale, offset):
        if self.show:
            render_rect = pygame.Rect(round((self.position.x + offset.x) * scale),
                                      round((self.position.y + offset.y) * scale),
                                      round(self.size.x * scale),
                                      round(self.size.y * scale))

            render_img = pygame.transform.scale(self.image, render_rect.size)
            render_img.set_alpha(self.alpha)
            screen.blit(render_img, render_rect.topleft)


class Button(Image):
    def __init__(self, position, size, images, list, alpha=255):
        self.images = images
        self.pre_mouse_down = False
        self.pre_mouse_over = False
        Image.__init__(self, position, size, images[0], list, alpha)

        self.anim = None
        self.pre_anim = None
        self.anim_time = 0  # tid siden animationen gik igang
        self.anim_offset = pygame.Vector2(0, 0)     # positionen i animationen

    def anim_reset(self):
        self.pre_mouse_over = False
        self.image = self.images[0]
        self.anim = None
        self.pre_anim = None
        self.anim_time = 0
        self.anim_offset = pygame.Vector2(0, 0)

    # returnerer hvorvidt knappen er blevet aktiveret (trykket ned og sluppet igen)
    def update(self, mouse_pos, mouse_down, delta_time):
        mouse_lifted = self.pre_mouse_down and not mouse_down
        self.pre_mouse_down = mouse_down

        mouse_over_x = self.position.x < mouse_pos.x < self.position.x + self.size.x
        mouse_over_y = self.position.y < mouse_pos.y < self.position.y + self.size.y
        mouse_over = mouse_over_x and mouse_over_y

        if mouse_over and mouse_lifted:
            return True
        elif mouse_over and mouse_down:
            self.image = self.images[2]
        elif mouse_over and not mouse_down:
            self.image = self.images[1]
        elif not mouse_over:
            self.image = self.images[0]

        if mouse_over:
            self.anim = 'mouse_over'
        elif not mouse_over and self.pre_mouse_over:
            self.anim = 'mouse_not_over'

        self.pre_mouse_over = mouse_over

        # animation time
        if self.anim != self.pre_anim:
            self.anim_time = 0
        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

    def draw(self, screen, scale, offset):
        # animations
        def mouse_over():
            if self.anim_time <= 0.1:
                self.anim_offset.y = self.anim_time * -100
            else:
                self.anim_offset.y = -10

        def mouse_not_over():
            if self.anim_time <= 0.1:
                self.anim_offset.y = self.anim_time * 100 - 10
            else:
                self.anim_offset.y = 0

        # animate
        if self.anim is not None:
            anim_function = {'mouse_over': mouse_over,
                             'mouse_not_over': mouse_not_over}[self.anim]
            anim_function()

        # render
        Image.draw(self, screen, scale, offset + self.anim_offset)


class Text(Image):
    def __init__(self, position, text, font, color, list, anti_aliasing=False, alpha=255):
        self.font = font
        self.color = color
        self.anti_aliasing = anti_aliasing

        image = self.font.render(text, self.anti_aliasing, self.color)
        size = image.get_size()
        Image.__init__(self, position, size, image, list, alpha)

    def set_text(self, new_text):
        image = self.font.render(new_text, self.anti_aliasing, self.color)

        self.size = pygame.Vector2(image.get_size())
        self.image = image
