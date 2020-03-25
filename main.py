import pygame, time, os, ctypes, platform

# Vores egne
import playerClass, platformClass, buttonClass, GUIClass, miscClasses


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

icon_img = pygame.image.load(os.path.join('Assets', 'icon.png'))
pygame.display.set_icon(icon_img)
pygame.display.set_caption('Vores spil der bare sparker røv')

scroll = 0
cam_speed = 700

GUI = GUIClass.GUI()

colliders = []
Ground = platformClass.Platform(position=(0, 880), length=38, colliders=colliders)
Ground2 = platformClass.Platform(position=(1920, 700), length=60, colliders=colliders)

Mark = playerClass.Player(position=(300, -50),
                          speed=(cam_speed, 0),
                          size=(40, 40),
                          color=(255, 0, 242),
                          colliders=colliders)


min_delta_time = 0.003
max_delta_time = 0.066
delta_time = 0
pre_time = pygame.time.get_ticks() / 1000
FPS_low_img = pygame.image.load(os.path.join('Assets', 'FPS Low.png'))
FPS_low = False


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
            if event.key == pygame.K_ESCAPE and GUI.scene == 'game':
                paused = not paused

            # toggle fullscreen
            if event.key == pygame.K_TAB:
                fullscreen = not fullscreen
                GUI.fullscreen = fullscreen
                screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) / screen_scale
    mouse_down = pygame.mouse.get_pressed()[0]

    # update
    GUI.update(mouse_pos, mouse_down, delta_time)

    if GUI.fullscreen != fullscreen:
        fullscreen = GUI.fullscreen
        screen, screen_scale = make_screen(fullscreen, window_scale, monitor_dim)

    if GUI.scene == 'game' and not paused:
        Mark.update(delta_time, cam_speed, space_pressed)
        scroll += cam_speed * delta_time

    # draw
    screen.fill((74, 228, 255))
    Ground.draw(screen, scroll, screen_scale)
    Ground2.draw(screen, scroll, screen_scale)
    Mark.draw(screen, scroll, screen_scale)
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
# oh yeah yeah
