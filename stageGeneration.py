import os
import json
import random
import pathlib
from collections import deque
from EnemyClass import Enemy

import miscClasses
from platformClass import Platform

segment_dicts = []
for file in pathlib.Path('Stage segments').iterdir():
    with open(file, 'r') as segment_file:
        segment_dicts.append(json.load(segment_file))


class StageSegment:
    def __init__(self, segment_id, start_point, platforms, spikes, coins, enemies, projectiles):
        self.position = start_point

        self.platforms = platforms
        self.spikes = spikes
        self.coins = coins
        self.enemies = enemies

        self.my_platforms = []
        self.my_spikes = []
        self.my_coins = []
        self.my_enemies = []

        segment_dict = segment_dicts[segment_id]
        self.length = segment_dict['length']

        for platform in segment_dict['platforms']:
            Platform((platform['x'] + self.position, platform['y']), platform['length'], self.my_platforms)

        for spike in segment_dict['spikes']:
            miscClasses.Spike((spike['x'] + self.position, spike['y']), self.my_spikes)

        for coin in segment_dict['coins']:
            miscClasses.Coin((coin['x'] + self.position, coin['y']), self.my_coins, self.coins)

        for enemy in segment_dict['enemies']:
            Enemy((enemy['x'] + self.position, enemy['y']), self.my_enemies, self.enemies, projectiles)

        for platform in self.my_platforms:
            self.platforms.append(platform)
        for spike in self.my_spikes:
            self.spikes.append(spike)
        for coin in self.my_coins:
            self.coins.append(coin)
        for enemy in self.my_enemies:
            self.enemies.append(enemy)

    def update(self, delta_time):
        for enemy in self.my_enemies:
            enemy.update(delta_time)

        for coin in self.my_coins:
            coin.update(delta_time)

    def __del__(self):
        for _ in self.my_platforms:
            self.platforms.popleft()
        for _ in self.my_spikes:
            self.spikes.popleft()
        for _ in self.my_coins:
            self.coins.popleft()
        for _ in self.my_enemies:
            self.enemies.popleft()


class Stage:
    def __init__(self, projectiles):

        self.projectiles = projectiles

        # deque står for 'double ended queue', og er lister hvor man
        # hurtigt og effektivt kan tilføje og fjerne elementer fra begge ender

        self.platforms = deque()
        self.spikes = deque()
        self.coins = deque()
        self.enemies = deque()

        self.segments = deque([StageSegment(0, 0, self.platforms, self.spikes, self.coins, self.enemies, self.projectiles)])

    def update(self, scroll, delta_time):
        # remove segment when out of frame
        if self.segments[0].position + self.segments[0].length < scroll:
            self.segments.popleft()

        # add new segment
        if self.segments[-1].position + self.segments[-1].length < scroll + 1920:
            segment_id = random.randint(1, len(segment_dicts) - 1)
            start_point = self.segments[-1].position + self.segments[-1].length + 300
            new_segment = StageSegment(segment_id, start_point, self.platforms, self.spikes, self.coins, self.enemies, self.projectiles)
            self.segments.append(new_segment)

        # update segments
        for segment in self.segments:
            segment.update(delta_time)
