import pygame
import time
import os

import player
import misc_classes


# init main loop
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'icon.png')))
pygame.display.set_caption('Vores spil der bare sparker røv')

scroll = 0
cam_speed = 400

colliders = []
Mark = player.Player((300, 500), (400, 0), (25, 25), (66, 135, 245), colliders)
Ground = misc_classes.Platform((0, 600), (1280, 120), colliders)

min_delta_time = 0.003
delta_time = 0
pre_time = pygame.time.get_ticks() / 1000

quit_game = False
paused = False

# main loop
while not quit_game:

    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    key_input = pygame.key.get_pressed()

    # update
    if not paused:
        Ground.update(delta_time)
        Mark.update(delta_time, key_input)
        scroll += cam_speed * delta_time

    # draw
    screen.fill((255, 255, 255))
    Ground.draw(screen, scroll)
    Mark.draw(screen, scroll)
    pygame.display.flip()

    # delta time
    delta_time = (pygame.time.get_ticks() / 1000) - pre_time
    pre_time = pygame.time.get_ticks() / 1000
    if delta_time < min_delta_time:
        time.sleep(min_delta_time - delta_time)
        delta_time += (pygame.time.get_ticks() / 1000) - pre_time
        pre_time = pygame.time.get_ticks() / 1000
#oh yeah yeah