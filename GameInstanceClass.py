import random
from playerClass import Player
import background
import stageGeneration


class GameInstance:

    def __init__(self):
        self.score = 0
        self.scroll = 0
        self.cam_speed = 700

        self.clouds = []
        self.projectiles = []

        self.stage = stageGeneration.Stage(self.projectiles)

        cloud_amount = 3
        for i in range(cloud_amount):
            min_x = i * (1920/cloud_amount)
            max_x = min_x+(1920/cloud_amount-500)
            x = random.randrange(min_x, max_x)
            y = random.randrange(-100, 100)
            background.Cloud((x, y), self.clouds)

        self.Mark = Player(position=(300, -200),
                           speed=(self.cam_speed, 0),
                           size=(83, 111),
                           gun='shotgun',
                           platforms=self.stage.platforms,
                           spikes=self.stage.spikes,
                           coins=self.stage.coins,
                           projectiles=self.projectiles,
                           enemies=self.stage.enemies)

    def update(self, delta_time, jump_pressed, shoot_pressed, sound_on):
        self.scroll += self.cam_speed * delta_time
        self.score = round(self.scroll / 200)

        for Cloud in self.clouds:
            Cloud.update(self.scroll)

        self.stage.update(self.scroll, delta_time)

        for projectile in self.projectiles:
            projectile.update(delta_time)

        self.Mark.update(delta_time, self.cam_speed, jump_pressed, shoot_pressed, sound_on)
        return self.Mark.coin_collected, self.Mark.dead, self.score

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

        for enemy in self.stage.enemies:
            enemy.draw(screen, self.scroll, screen_scale)

        for projectile in self.projectiles:
            projectile.draw(screen, self.scroll, screen_scale)

        self.Mark.draw(screen, self.scroll, screen_scale)
