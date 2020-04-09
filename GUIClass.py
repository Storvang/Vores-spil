import pygame, os
import GUIElementClasses


def load_button_imgs(list, prefix, path):
    for i in range(3):
        list.append(pygame.image.load(os.path.join(path, prefix + str(i) + '.png')))


play_button_imgs = []
load_button_imgs(play_button_imgs, 'Play Button', os.path.join('Assets', 'UI', 'Play Button v2'))

replay_button_imgs = []
load_button_imgs(replay_button_imgs, 'Replay Button', os.path.join('Assets', 'UI', 'Replay Button'))

home_button_imgs = []
load_button_imgs(home_button_imgs, 'Home Button', os.path.join('Assets', 'UI', 'Home Button'))

fullscreen_button_imgs = []
load_button_imgs(fullscreen_button_imgs, 'Fullscreen Button', os.path.join('Assets', 'UI', 'Fullscreen Button'))

pause_title_img = pygame.image.load(os.path.join('Assets', 'UI', 'Paused Title.png'))


class GUI:
    def __init__(self):
        self.scene = 'start_menu'
        self.pre_scene = None

        self.fullscreen = False
        self.game_reset = False

        self.transition = None
        self.pre_transition = None
        self.transition_time = 0
        self.transition_offset = pygame.Vector2(0, 0)
        self.transition_stage = 0

        # init start menu
        self.play_button = GUIElementClasses.Button((773, 478), (250, 125), play_button_imgs)
        self.fullscreen_button = GUIElementClasses.Button((1050, 478), (113, 125), fullscreen_button_imgs)

        # init pause menu
        self.black_img = pygame.Surface((1, 1))
        pygame.draw.rect(self.black_img, (0, 0, 0), (0, 0, 1, 1))
        self.fade_background = GUIElementClasses.Image((0, 0), (1920, 1080), self.black_img, 100)
        self.fade_foreground = GUIElementClasses.Image((0, 0), (1920, 1080), self.black_img, 0)
        self.fade_foreground.show = False

        self.pause_title = GUIElementClasses.Image((610, 180), (700, 180), pause_title_img)
        self.resume_button = GUIElementClasses.Button((835, 478), (250, 125), play_button_imgs)
        self.replay_button = GUIElementClasses.Button((650, 478), (113, 125), replay_button_imgs)
        self.home_button = GUIElementClasses.Button((1157, 478), (113, 125), home_button_imgs)

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
            elif self.replay_button.update(mouse_pos, mouse_down, delta_time):
                self.transition = 'restart_game'
            elif self.home_button.update(mouse_pos, mouse_down, delta_time):
                self.transition = 'go_home'

        if self.transition is None:
            scene_function = {'game': game,
                              'start_menu': start_menu,
                              'pause_menu': pause_menu}[self.scene]
            scene_function()

        # animation time
        if self.transition != self.pre_transition:
            self.transition_time = 0
            self.transition_stage = 0
        else:
            self.transition_time += delta_time
        self.pre_transition = self.transition

    def draw(self, screen, scale):

        # transitions
        def start_game():
            if self.transition_time <= 1:
                self.transition_offset.y = -540 * ((self.transition_time / 0.5) ** 2 - (self.transition_time / 0.5))
            else:
                self.scene = 'game'
                self.transition = None

        def restart_game():
            self.fade_foreground.show = True

            if self.transition_stage == 0 and self.transition_time <= 0.5:
                self.fade_foreground.alpha = 510 * self.transition_time
            elif self.transition_stage == 0:
                self.game_reset = True
                self.transition_stage = 1
                self.scene = 'game'

            elif self.transition_stage == 1 and self.transition_time <= 1:
                self.fade_foreground.alpha = -510 * (self.transition_time - 0.5) + 255
            elif self.transition_stage == 1:
                self.transition = None
                self.fade_foreground.show = False

        def go_home():
            self.fade_foreground.show = True

            if self.transition_stage == 0 and self.transition_time <= 0.5:
                self.fade_foreground.alpha = 510 * self.transition_time
            elif self.transition_stage == 0:
                self.game_reset = True
                self.transition_stage = 1
                self.scene = 'start_menu'

            elif self.transition_stage == 1 and self.transition_time <= 1:
                self.fade_foreground.alpha = -510 * (self.transition_time - 0.5) + 255
            elif self.transition_stage == 1:
                self.transition = None
                self.fade_foreground.show = False

        # animate
        if self.transition is not None:
            transition_function = {'start_game': start_game,
                                   'restart_game': restart_game,
                                   'go_home': go_home}[self.transition]
            transition_function()
        else:
            self.transition_offset = pygame.Vector2(0, 0)

        # render
        def game():
            self.fade_foreground.draw(screen, scale, self.transition_offset)

        def start_menu():
            self.play_button.draw(screen, scale, self.transition_offset)
            self.fullscreen_button.draw(screen, scale, self.transition_offset)
            self.fade_foreground.draw(screen, scale, self.transition_offset)

        def pause_menu():
            self.fade_background.draw(screen, scale, self.transition_offset)
            self.pause_title.draw(screen, scale, self.transition_offset)
            self.resume_button.draw(screen, scale, self.transition_offset)
            self.replay_button.draw(screen, scale, self.transition_offset)
            self.home_button.draw(screen, scale, self.transition_offset)
            self.fade_foreground.draw(screen, scale, self.transition_offset)

        scene_function = {'game': game,
                          'start_menu': start_menu,
                          'pause_menu': pause_menu}[self.scene]
        scene_function()
