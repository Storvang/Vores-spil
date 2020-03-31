import pygame, os
import GUIElementClasses

play_button_imgs = [pygame.image.load(os.path.join('Assets', 'UI', 'Play Button v2', 'Play Button0.png')),
                    pygame.image.load(os.path.join('Assets', 'UI', 'Play Button v2', 'Play Button1.png')),
                    pygame.image.load(os.path.join('Assets', 'UI', 'Play Button v2', 'Play Button2.png'))]

fullscreen_button_imgs = [pygame.image.load(os.path.join('Assets', 'UI', 'Fullscreen Button', 'Fullscreen Button0.png')),
                          pygame.image.load(os.path.join('Assets', 'UI', 'Fullscreen Button', 'Fullscreen Button1.png')),
                          pygame.image.load(os.path.join('Assets', 'UI', 'Fullscreen Button', 'Fullscreen Button2.png'))]

pause_title_img = pygame.image.load(os.path.join('Assets', 'UI', 'Paused Title.png'))


class GUI:
    def __init__(self):
        self.scene = 'start_menu'
        self.pre_scene = None

        self.fullscreen = False

        self.transition = None
        self.pre_transition = None
        self.transition_time = 0
        self.transition_offset = pygame.Vector2(0, 0)

        # init start menu
        self.play_button = GUIElementClasses.Button((773, 478), (250, 125), play_button_imgs)
        self.fullscreen_button = GUIElementClasses.Button((1050, 478), (113, 125), fullscreen_button_imgs)

        # init pause menu
        self.fade_background_img = pygame.Surface((1, 1))
        pygame.draw.rect(self.fade_background_img, (0, 0, 0), (0, 0, 1, 1))
        self.fade_background_img.set_alpha(100)
        self.fade_background = GUIElementClasses.Image((0, 0), (1920, 1080), self.fade_background_img)
        self.pause_title = GUIElementClasses.Image((610, 180), (700, 180), pause_title_img)
        self.resume_button = GUIElementClasses.Button((835, 478), (250, 125), play_button_imgs)

    def update(self, mouse_pos, mouse_down, delta_time):
        # scenes
        def game():
            pass

        def start_menu():
            if self.play_button.update(mouse_pos, mouse_down, delta_time):
                self.transition = 'start_game'

            if self.fullscreen_button.update(mouse_pos, mouse_down, delta_time):
                self.fullscreen = not self.fullscreen

        def pause_menu():
            if self.resume_button.update(mouse_pos, mouse_down, delta_time):
                self.scene = 'game'

        if self.transition is None:
            scene_function = {'game': game,
                              'start_menu': start_menu,
                              'pause_menu': pause_menu}[self.scene]
            scene_function()

        # animation time
        if self.transition != self.pre_transition:
            self.transition_time = 0
        else:
            self.transition_time += delta_time
        self.pre_transition = self.transition

    def draw(self, screen, scale):
        # transitions
        def start_game():
            if self.transition_time <= 1:
                self.transition_offset = pygame.Vector2(0, -540 * ((self.transition_time / 0.5) ** 2 - (self.transition_time / 0.5)))
            else:
                self.scene = 'game'
                self.transition = None

        # animate
        if self.transition is not None:
            transition_function = {"start_game": start_game}[self.transition]
            transition_function()
        else:
            self.transition_offset = pygame.Vector2(0, 0)

        # render
        def game():
            pass

        def start_menu():
            self.play_button.draw(screen, scale, self.transition_offset)
            self.fullscreen_button.draw(screen, scale, self.transition_offset)

        def pause_menu():
            self.fade_background.draw(screen, scale, self.transition_offset)
            self.pause_title.draw(screen, scale, self.transition_offset)
            self.resume_button.draw(screen, scale, self.transition_offset)

        scene_function = {'game': game,
                          'start_menu': start_menu,
                          'pause_menu': pause_menu}[self.scene]
        scene_function()
