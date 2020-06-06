import pygame

import GUIElementClasses
import GUIScenes


class GUI:
    def __init__(self):
        self.coin_count = [0]

        self.sound_on = True
        self.music_on = True
        self.fullscreen = False
        self.game_reset = False

        self.scene = self.start_menu = GUIScenes.StartMenu(self.sound_on, self.music_on)
        self.pre_scene = None

        self.transition = None
        self.pre_transition = None
        self.transition_time = 0
        self.transition_offset = pygame.Vector2(0, 0)
        self.transition_stage = 0

        black_img = pygame.Surface((1, 1))
        pygame.draw.rect(black_img, (0, 0, 0), (0, 0, 1, 1))
        self.fade_foreground = GUIElementClasses.Image((0, 0), (1920, 1080), black_img, [], 0)
        self.fade_foreground.show = False

    def update(self, mouse_pos, mouse_down, coin_count, delta_time):
        self.coin_count[0] = coin_count

        # funktioner som bliver kaldt af knapperne
        def play():
            self.transition = 'start_game'

        def replay():
            self.transition = 'restart_game'

        def resume():
            self.scene = GUIScenes.Game(self.coin_count)

        def go_home():
            self.transition = 'go_home'

        def switch_sound():
            self.sound_on = not self.sound_on

        def switch_music():
            self.music_on = not self.music_on

        def switch_fullscreen():
            self.fullscreen = not self.fullscreen

        if self.transition is None:
            update_return = self.scene.update(mouse_pos, mouse_down, delta_time)

            if update_return is not None:
                function = {'play': play,
                            'replay': replay,
                            'resume': resume,
                            'go_home': go_home,
                            'switch_sound': switch_sound,
                            'switch_music': switch_music,
                            'switch_fullscreen': switch_fullscreen}[update_return]
                function()

        # animation time
        if self.transition != self.pre_transition:
            self.transition_time = 0
            self.transition_stage = 0
        else:
            self.transition_time += delta_time
        self.pre_transition = self.transition

        # transitions
        def start_game():
            if self.transition_time <= 1:
                self.transition_offset.y = -540 * ((self.transition_time / 0.5) ** 2 - (self.transition_time / 0.5))
            else:
                self.scene = GUIScenes.Game(self.coin_count)
                self.transition = 'enter_game'

        def enter_game():
            if self.transition_time <= 0.5:
                self.transition_offset.y = -100 * ((self.transition_time / 0.5) - 1) ** 2
            else:
                self.transition = None

        def restart_game():
            self.fade_foreground.show = True

            if self.transition_stage == 0 and self.transition_time <= 0.5:
                self.fade_foreground.alpha = 510 * self.transition_time
            elif self.transition_stage == 0:
                self.game_reset = True
                self.transition_stage = 1
                self.scene = GUIScenes.Game(self.coin_count)

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
                self.scene = GUIScenes.StartMenu(self.sound_on, self.music_on)

            elif self.transition_stage == 1 and self.transition_time <= 1:
                self.fade_foreground.alpha = -510 * (self.transition_time - 0.5) + 255
            elif self.transition_stage == 1:
                self.transition = None
                self.fade_foreground.show = False

        def die():
            self.scene = GUIScenes.DeathMenu()
            self.transition = None

        # animate
        if self.transition is not None:
            transition_function = {'start_game': start_game,
                                   'enter_game': enter_game,
                                   'restart_game': restart_game,
                                   'go_home': go_home,
                                   'die': die}[self.transition]
            transition_function()
        else:
            self.transition_offset = pygame.Vector2(0, 0)

    def draw(self, screen, scale):
        self.scene.draw(screen, scale, self.transition_offset)
        self.fade_foreground.draw(screen, scale, self.transition_offset)

        self.pre_scene = self.scene
