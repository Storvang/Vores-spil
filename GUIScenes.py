import pygame, os
import GUIElementClasses


def load_button_imgs(list, prefix, path):
    for i in range(3):
        list.append(pygame.image.load(os.path.join(path, prefix + str(i) + '.png')))


play_button_imgs = []
load_button_imgs(play_button_imgs, 'Play Button', os.path.join('Assets', 'UI', 'Play Button v2'))

replay_button_imgs = []
load_button_imgs(replay_button_imgs, 'Replay Button', os.path.join('Assets', 'UI', 'Replay Button'))

wide_replay_button_imgs = []
load_button_imgs(wide_replay_button_imgs, 'Wide Replay Button', os.path.join('Assets', 'UI', 'Wide Replay Button'))

home_button_imgs = []
load_button_imgs(home_button_imgs, 'Home Button', os.path.join('Assets', 'UI', 'Home Button'))

flscrn_button_imgs = []
load_button_imgs(flscrn_button_imgs, 'Fullscreen Button', os.path.join('Assets', 'UI', 'Fullscreen Button'))

sound_on_button_imgs = []
load_button_imgs(sound_on_button_imgs, 'Sound Button_on', os.path.join('Assets', 'UI', 'Sound Button off and on'))

sound_off_button_imgs = []
load_button_imgs(sound_off_button_imgs, 'Sound Button_off', os.path.join('Assets', 'UI', 'Sound Button off and on'))

music_on_button_imgs = []
load_button_imgs(music_on_button_imgs, 'Music button on', os.path.join('Assets', 'UI', 'Music button on and off'))

music_off_button_imgs = []
load_button_imgs(music_off_button_imgs, 'Music button off', os.path.join('Assets', 'UI', 'Music button on and off'))

coin_img = pygame.image.load(os.path.join('Assets', 'Dogecoin.png'))
pause_title_img = pygame.image.load(os.path.join('Assets', 'UI', 'Paused Title.png'))
death_title_img = pygame.image.load(os.path.join('Assets', 'UI', 'Death Title.png'))

pixel_font = pygame.font.Font(os.path.join('Assets', 'UI', 'Pixeled.ttf'), 35)


class GUIScene:
    def __init__(self):
        self.GUIElements = []

    def update(self, mouse_pos, mouse_down, delta_time):
        pass

    def draw(self, screen, scale, offset):
        for Element in self.GUIElements:
            Element.draw(screen, scale, offset)


class Game(GUIScene):
    def __init__(self, coin_count):
        self.coin_count = coin_count
        GUIScene.__init__(self)
        self.coin_logo = GUIElementClasses.Image((25, 25), (50, 50), coin_img, self.GUIElements)
        self.coin_counter = GUIElementClasses.Text((90, -4), str(self.coin_count[0]), pixel_font, (217, 182, 11), self.GUIElements)

    def update(self, mouse_pos, mouse_down, delta_time):
        self.coin_counter.set_text(str(self.coin_count[0]))


class StartMenu(GUIScene):
    def __init__(self, sound_on, music_on):
        sound_button_imgs = sound_on_button_imgs if sound_on else sound_off_button_imgs
        self.sound_on = sound_on

        music_button_imgs = music_on_button_imgs if music_on else music_off_button_imgs
        self.music_on = music_on

        GUIScene.__init__(self)

        self.play_button = GUIElementClasses.Button((773, 478), (250, 125), play_button_imgs, self.GUIElements)
        self.fullscreen_button = GUIElementClasses.Button((1050, 478), (113, 125), flscrn_button_imgs, self.GUIElements)
        self.sound_button = GUIElementClasses.Button((1757, 905), (113, 125), sound_button_imgs, self.GUIElements)
        self.music_button = GUIElementClasses.Button((1594, 905), (113, 125), music_button_imgs, self.GUIElements)

    def update(self, mouse_pos, mouse_down, delta_time):

        if self.play_button.update(mouse_pos, mouse_down, delta_time):
            return 'play'

        elif self.fullscreen_button.update(mouse_pos, mouse_down, delta_time):
            return 'switch_fullscreen'

        elif self.sound_button.update(mouse_pos, mouse_down, delta_time):
            self.sound_on = not self.sound_on
            self.sound_button.images = sound_on_button_imgs if self.sound_on else sound_off_button_imgs
            return 'switch_sound'

        elif self.music_button.update(mouse_pos, mouse_down, delta_time):
            self.music_on = not self.music_on
            self.music_button.images = music_on_button_imgs if self.music_on else music_off_button_imgs
            return 'switch_music'


class PauseMenu(GUIScene):
    def __init__(self, sound_on, music_on):
        sound_button_imgs = sound_on_button_imgs if sound_on else sound_off_button_imgs
        self.sound_on = sound_on

        music_button_imgs = music_on_button_imgs if music_on else music_off_button_imgs
        self.music_on = music_on
        GUIScene.__init__(self)

        # den mørke baggrund
        black_img = pygame.Surface((1, 1))
        pygame.draw.rect(black_img, (0, 0, 0), (0, 0, 1, 1))
        self.fade_background = GUIElementClasses.Image((0, 0), (1920, 1080), black_img, self.GUIElements, 100)

        self.pause_title = GUIElementClasses.Image((610, 243), (700, 180), pause_title_img, self.GUIElements)
        self.resume_button = GUIElementClasses.Button((835, 541), (250, 125), play_button_imgs, self.GUIElements)
        self.replay_button = GUIElementClasses.Button((650, 541), (113, 125), replay_button_imgs, self.GUIElements)
        self.home_button = GUIElementClasses.Button((1157, 541), (113, 125), home_button_imgs, self.GUIElements)
        self.sound_button = GUIElementClasses.Button((1757, 905), (113, 125), sound_button_imgs, self.GUIElements)
        self.music_button = GUIElementClasses.Button((1594, 905), (113, 125), music_button_imgs, self.GUIElements)









    def update(self, mouse_pos, mouse_down, delta_time):

        if self.resume_button.update(mouse_pos, mouse_down, delta_time):
            return 'resume'

        elif self.replay_button.update(mouse_pos, mouse_down, delta_time):
            return 'replay'

        elif self.home_button.update(mouse_pos, mouse_down, delta_time):
            return 'go_home'

        elif self.sound_button.update(mouse_pos, mouse_down, delta_time):
            self.sound_on = not self.sound_on
            self.sound_button.images = sound_on_button_imgs if self.sound_on else sound_off_button_imgs
            return 'switch_sound'

        elif self.music_button.update(mouse_pos, mouse_down, delta_time):
            self.music_on = not self.music_on
            self.music_button.images = music_on_button_imgs if self.music_on else music_off_button_imgs
            return 'switch_music'


class DeathMenu(GUIScene):
    def __init__(self):
        GUIScene.__init__(self)

        self.death_title = GUIElementClasses.Image((540, 243), (840, 180), death_title_img, self.GUIElements)
        self.replay_button = GUIElementClasses.Button((835, 541), (250, 125), wide_replay_button_imgs, self.GUIElements)
        self.home_button = GUIElementClasses.Button((1157, 541), (113, 125), home_button_imgs, self.GUIElements)

    def update(self, mouse_pos, mouse_down, delta_time):

        if self.replay_button.update(mouse_pos, mouse_down, delta_time):
            return 'replay'

        elif self.home_button.update(mouse_pos, mouse_down, delta_time):
            return 'go_home'
