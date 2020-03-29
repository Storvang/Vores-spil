import pygame, os
import buttonClass

play_button_imgs = [pygame.image.load(os.path.join('Assets', 'UI', 'Play Button v2', 'Play Button0.png')),
                    pygame.image.load(os.path.join('Assets', 'UI', 'Play Button v2', 'Play Button1.png')),
                    pygame.image.load(os.path.join('Assets', 'UI', 'Play Button v2', 'Play Button2.png'))]

fullscreen_button_imgs = [pygame.image.load(os.path.join('Assets', 'UI', 'Fullscreen Button', 'Fullscreen Button0.png')),
                          pygame.image.load(os.path.join('Assets', 'UI', 'Fullscreen Button', 'Fullscreen Button1.png')),
                          pygame.image.load(os.path.join('Assets', 'UI', 'Fullscreen Button', 'Fullscreen Button2.png'))]


class GUI:
    def __init__(self):
        self.scene = 'start_menu'
        self.pre_scene = None

        self.fullscreen = False

        self.play_button = buttonClass.Button((773, 478), (250, 125), play_button_imgs)
        self.fullscreen_button = buttonClass.Button((1050, 478), (113, 125), fullscreen_button_imgs)
        self.play_pressed = False

        self.anim = None
        self.pre_anim = None
        self.anim_time = 0
        self.anim_offset = pygame.Vector2(0, 0)

    def update(self, mouse_pos, mouse_down, delta_time):
        if self.scene == 'start_menu' and self.anim is None:
            if self.play_button.update(mouse_pos, mouse_down, delta_time):
                play_pressed = True
                self.anim = 'start_game'

            if self.fullscreen_button.update(mouse_pos, mouse_down, delta_time):
                self.fullscreen = not self.fullscreen

        # animation time
        if self.anim != self.pre_anim:
            self.anim_time = 0
        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

    def start_game_anim(self):
        if self.anim_time <= 1:
            self.anim_offset = pygame.Vector2(0, -1080 * 0.5 * ((self.anim_time / 0.5) ** 2 - (self.anim_time / 0.5)))
        elif self.anim_time > 1:
            self.scene = 'game'
            self.anim = None

    def draw(self, screen, scale):

        # animate
        if self.anim is not None:
            anim_function = {"start_game": self.start_game_anim}[self.anim]
            anim_function()

        self.play_button.draw(screen, scale, self.anim_offset)
        self.fullscreen_button.draw(screen, scale, self.anim_offset)
