import pygame, time, os, ctypes, platform

# init pygame and mixer
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.init()

import GUIClass, GUIScenes, GameInstanceClass   # Mixeren bliver nødt til at blive inittet før der kan indlæses lydfiler


def make_screen(fullscreen, window_scale, monitor_dim):
    if fullscreen:
        screen_scale = monitor_dim[0] / 1920
        screen = pygame.display.set_mode(monitor_dim, pygame.FULLSCREEN)
    else:
        screen_scale = window_scale
        screen = pygame.display.set_mode((round(1920 * screen_scale), round(1080 * screen_scale)))
    return screen, screen_scale


# init main loop
pygame.mixer.music.load(os.path.join('Assets', 'Sounds', 'en for alle.mp3'))
pygame.mixer.music.play(-1)

if platform.system() == "Windows":
    ctypes.windll.user32.SetProcessDPIAware()   # ignorer Windows skærm-skalering

sfx = pygame.mixer.Channel(1)


sound_on = True
music_on = True
fullscreen = False
window_scale = 0.7  # bliver kun brugt hvis fullscreen er deaktiveret
monitor_dim = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

icon_img = pygame.image.load(os.path.join('Assets', 'icon.png'))
pygame.display.set_icon(icon_img)
pygame.display.set_caption('Vores spil der bare sparker røv')

min_delta_time = 0.003
max_delta_time = 0.066
delta_time = 0
pre_time = pygame.time.get_ticks() / 1000
FPS_low_img = pygame.image.load(os.path.join('Assets', 'FPS Low.png'))
FPS_low = False

coin_count = 0
quit_game = False

GUI = GUIClass.GUI()
GameInstance = GameInstanceClass.GameInstance(sfx)

# main loop
while not quit_game:

    # input
    space_pressed = False
    mouse_pressed = False

    for event in pygame.event.get():
        mouse_pressed = event.type == pygame.MOUSEBUTTONDOWN

        if event.type == pygame.QUIT:
            quit_game = True

        elif event.type == pygame.KEYDOWN:

            # jump
            if event.key == pygame.K_SPACE:
                space_pressed = True

            # pause
            elif event.key == pygame.K_ESCAPE and GUI.transition is None:
                if isinstance(GUI.scene, GUIScenes.PauseMenu):
                    GUI.scene = GUIScenes.Game(GUI.coin_count)
                elif isinstance(GUI.scene, GUIScenes.Game):
                    GUI.scene = GUIScenes.PauseMenu(GUI.sound_on, GUI.music_on)

            # toggle fullscreen
            elif event.key == pygame.K_TAB:
                fullscreen = not fullscreen
                GUI.fullscreen = fullscreen
                screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / screen_scale
    mouse_down = pygame.mouse.get_pressed()[0]

    GUI.update(mouse_pos, mouse_down, coin_count, delta_time)

    # init new game
    if GUI.game_reset:
        GameInstance = GameInstanceClass.GameInstance(sfx)
        GUI.game_reset = False

    # update
    if GUI.fullscreen != fullscreen:
        fullscreen = GUI.fullscreen
        screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

    if GUI.music_on != music_on:
        music_on = GUI.music_on
        if music_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    if GUI.sound_on != sound_on:
        sound_on = GUI.sound_on


    if isinstance(GUI.scene, GUIScenes.Game):   # Tjek at man ikke er på en menu
        coin_collected, dead = GameInstance.update(delta_time, space_pressed, mouse_pressed, sound_on)
        if coin_collected:
            coin_count += 1
        if dead:
            GUI.scene = GUIScenes.DeathMenu()

    # draw
    GameInstance.draw(screen, screen_scale)
    GUI.draw(screen, screen_scale)

    if FPS_low:
        FPS_low_img = pygame.transform.scale(FPS_low_img, (round(192 * screen_scale), round(36 * screen_scale)))
        screen.blit(FPS_low_img, (round(1723 * screen_scale), round(5 * screen_scale)))

    pygame.display.flip()

    # delta time
    FPS_low = False
    delta_time = (pygame.time.get_ticks() / 1000) - pre_time
    pre_time = pygame.time.get_ticks() / 1000

    if delta_time < min_delta_time:
        time.sleep(min_delta_time - delta_time)
        delta_time += (pygame.time.get_ticks() / 1000) - pre_time
        pre_time = pygame.time.get_ticks() / 1000

    elif delta_time > max_delta_time:
        delta_time = max_delta_time
        FPS_low = True

    # delta_time = delta_time * 0.25

    # print(1 / delta_time)
# oh yeah yeah
