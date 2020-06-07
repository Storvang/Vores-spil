import pygame
import time
import os
import ctypes
import platform
import math
import json

# init pygame and mixer
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.init()

# Mixeren bliver nødt til at blive inittet før der kan indlæses lydfiler
import GUIClass
import GUIScenes
import GameInstanceClass


# init screen
def make_screen(fullscreen, window_scale, monitor_dim):
    if fullscreen:
        screen_scale = monitor_dim[0] / 1920
        screen = pygame.display.set_mode(monitor_dim, pygame.FULLSCREEN)
    else:
        screen_scale = window_scale
        screen = pygame.display.set_mode((round(1920 * screen_scale), round(1080 * screen_scale)))
    return screen, screen_scale


if platform.system() == "Windows":
    ctypes.windll.user32.SetProcessDPIAware()   # ignorer Windows skærm-skalering

fullscreen = False
window_scale = 0.7  # bliver kun brugt hvis fullscreen er deaktiveret
monitor_dim = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

icon_img = pygame.image.load(os.path.join('Assets', 'icon.png'))
pygame.display.set_icon(icon_img)
pygame.display.set_caption('Vores spil der bare sparker røv')

# init sound
sound_on = True
music_on = True
pygame.mixer.music.load(os.path.join('Assets', 'Sounds', 'en for alle.mp3'))
pygame.mixer.music.play(-1)

# init timing
max_delta_time = 1/15   # den lavest tilladte framerate svarer til 15 fps
delta_time = 0
pre_time = pygame.time.get_ticks() / 1000
FPS_low_img = pygame.image.load(os.path.join('Assets', 'FPS Low.png'))
FPS_low = False

# init GUI
GUI = GUIClass.GUI()
GameInstance = GameInstanceClass.GameInstance()

# load saved data
with open('saveData.json', 'r') as saveDataFile:
    saveData = json.load(saveDataFile)

    score = 0
    highscore = saveData['highscore']
    coin_count = saveData['coin_count']


# main loop
quit_game = False
while not quit_game:

    # collect input
    jump_pressed = False
    shoot_pressed = False

    for event in pygame.event.get():
        shoot_pressed = event.type == pygame.MOUSEBUTTONDOWN

        if event.type == pygame.QUIT:
            quit_game = True

        elif event.type == pygame.KEYDOWN:

            def jump():
                global jump_pressed
                jump_pressed = True

            def shoot():
                global shoot_pressed
                shoot_pressed = True

            def pause():
                global GUI

                if GUI.transition is None:
                    if isinstance(GUI.scene, GUIScenes.PauseMenu):
                        GUI.scene = GUIScenes.Game(coin_count, highscore)
                    elif isinstance(GUI.scene, GUIScenes.Game):
                        GUI.scene = GUIScenes.PauseMenu(sound_on, music_on)

            def switch_fullscreen():
                global fullscreen, screen, screen_scale

                fullscreen = not fullscreen
                screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

            action_dict = {pygame.K_SPACE: jump,
                           pygame.K_w: jump,
                           pygame.K_i: shoot,
                           pygame.K_ESCAPE: pause,
                           pygame.K_f: switch_fullscreen}

            if event.key in action_dict:
                action = action_dict[event.key]
                action()

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / screen_scale
    mouse_down = pygame.mouse.get_pressed()[0]

    # update GUI
    GUI_action = GUI.update(mouse_pos, mouse_down, coin_count, score, highscore, sound_on, music_on, delta_time)

    def restart_game():
        global GameInstance
        GameInstance = GameInstanceClass.GameInstance()

    def switch_fullscreen():
        global fullscreen, screen, screen_scale

        fullscreen = not fullscreen
        screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

    def switch_music():
        global music_on
        music_on = not music_on
        if music_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def switch_sound():
        global sound_on
        sound_on = not sound_on


    if GUI_action is not None:
        GUI_action_function = {'restart_game': restart_game,
                               'switch_fullscreen': switch_fullscreen,
                               'switch_music': switch_music,
                               'switch_sound': switch_sound}[GUI_action]
        GUI_action_function()

    # update game
    if isinstance(GUI.scene, GUIScenes.Game):   # Tjek at man ikke er på en menu
        coin_collected, dead, score = GameInstance.update(delta_time, jump_pressed, shoot_pressed, sound_on)
        if coin_collected:
            coin_count += 1
        if dead:
            GUI.scene = GUIScenes.DeathMenu()
        if score > highscore:
            highscore = score

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

    if delta_time > max_delta_time:
        delta_time = max_delta_time
        FPS_low = True

# save data
with open('saveData.json', 'w') as saveDataFile:
    saveData = {'highscore': highscore, 'coin_count': coin_count}
    json.dump(saveData, saveDataFile, indent=4)

# oh yeah yeah
