import pygame
import time
import os
import ctypes
import platform

# Vores egne
import player
import misc_classes


def make_screen(fullscreen, window_scale, monitor_dim):
    if fullscreen:
        screen_scale = monitor_dim[0] / 1920
        screen = pygame.display.set_mode(monitor_dim, pygame.FULLSCREEN)
    else:
        screen_scale = window_scale
        screen = pygame.display.set_mode((round(1920 * screen_scale), round(1080 * screen_scale)))
    return screen, screen_scale


# init main loop
pygame.init()

if platform.system() == "Windows":
    ctypes.windll.user32.SetProcessDPIAware()   # ignorer Windows skærm-skalering

fullscreen = False
window_scale = 0.7  # bliver kun brugt hvis fullscreen er deaktiveret
monitor_dim = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'CoolDaniel.png')))
pygame.display.set_caption('Vores spil der bare sparker røv, ps daniel er en monke')

scroll = 0
cam_speed = 1000

colliders = []
Mark = player.Player(position=(300, 500), speed=(cam_speed, 0), size=(40, 40), color=(66, 135, 245), colliders=colliders)
Ground = misc_classes.Platform(position=(0, 880), size=(1920, 200), colliders=colliders)
Ground2 = misc_classes.Platform(position=(1920, 700), size=(3000, 50), colliders=colliders)

min_delta_time = 0.003
delta_time = 0
pre_time = pygame.time.get_ticks() / 1000

quit_game = False
paused = False

# main loop
while not quit_game:

    # input
    space_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        elif event.type == pygame.KEYDOWN:

            # jump
            if event.key == pygame.K_SPACE:
                space_pressed = True

            # pause
            if event.key == pygame.K_ESCAPE:
                paused = not paused

            # toggle fullscreen
            if event.key == pygame.K_TAB:
                fullscreen = not fullscreen
                _, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

    key_input = pygame.key.get_pressed()

    # update
    if not paused:
        Ground.update(delta_time)
        Ground2.update(delta_time)
        Mark.update(delta_time, space_pressed)
        scroll += cam_speed * delta_time

    # draw
    screen.fill((255, 255, 255))
    Ground.draw(screen, scroll, screen_scale)
    Ground2.draw(screen, scroll, screen_scale)
    Mark.draw(screen, scroll, screen_scale)
    pygame.display.flip()

    # delta time
    delta_time = (pygame.time.get_ticks() / 1000) - pre_time
    pre_time = pygame.time.get_ticks() / 1000
    if delta_time < min_delta_time:
        time.sleep(min_delta_time - delta_time)
        delta_time += (pygame.time.get_ticks() / 1000) - pre_time
        pre_time = pygame.time.get_ticks() / 1000
#oh yeah yeah