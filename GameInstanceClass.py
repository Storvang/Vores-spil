import random
from playerClass import Player
import background
import stageGeneration

# with open('stage performance log.txt', 'w') as file:
#     file.write("stage generation time:")
#
# with open('player performance log.txt', 'w') as file:
#     file.write("player generation time:")
#
# with


class GameInstance:

    def __init__(self):
        self.scroll = 0
        self.cam_speed = 700

        self.clouds = []
        self.projectiles = []

        self.stage = stageGeneration.Stage()

        y = random.randint(-100, 100)
        x = random.randint(0, 2500)
        background.Cloud(position=(x, y), clouds=self.clouds)

        self.Mark = Player(position=(300, -200),
                           speed=(self.cam_speed, 0),
                           size=(83, 111),
                           gun='shotgun',
                           platforms=self.stage.platforms,
                           spikes=self.stage.spikes,
                           coins=self.stage.coins,
                           projectiles=self.projectiles)

    def update(self, delta_time, jump_pressed, shoot_pressed, sound_on):
        self.scroll += self.cam_speed * delta_time

        self.stage.update(self.scroll)

        for projectile in self.projectiles:
            projectile.update(delta_time)
        self.Mark.update(delta_time, self.cam_speed, jump_pressed, shoot_pressed, sound_on)
        return self.Mark.coin_collected, self.Mark.dead

    def draw(self, screen, screen_scale):
        screen.fill((74, 228, 255))

        for cloud in self.clouds:
            cloud.draw(screen, self.scroll, screen_scale)

        for platform in self.stage.platforms:
            platform.draw(screen, self.scroll, screen_scale)

        for spike in self.stage.spikes:
            spike.draw(screen, self.scroll, screen_scale)

        for coin in self.stage.coins:
            coin.draw(screen, self.scroll, screen_scale)

        for projectile in self.projectiles:
            projectile.draw(screen, self.scroll, screen_scale)

        self.Mark.draw(screen, self.scroll, screen_scale)
