import os
import json
import random
from collections import deque

import miscClasses
from platformClass import Platform

segment_dicts = []
for i in range(2):
    with open(os.path.join('Stage segments', 'Stage segment' + str(i) + '.txt'), 'r') as segment_file:
        segment_dicts.append(json.load(segment_file))


class StageSegment:
    def __init__(self, segment_id, start_point, platforms, spikes, coins):
        self.position = start_point

        self.platforms = platforms
        self.spikes = spikes
        self.coins = coins

        self.my_platforms = []
        self.my_spikes = []
        self.my_coins = []

        segment_dict = segment_dicts[segment_id]
        self.length = segment_dict['length']

        for platform in segment_dict['platforms']:
            Platform((platform['x'] + self.position, platform['y']), platform['length'], self.my_platforms)

        for spike in segment_dict['spikes']:
            miscClasses.Spike((spike['x'] + self.position, spike['y']), self.my_spikes)

        for coin in segment_dict['coins']:
            miscClasses.Coin((coin['x'] + self.position, coin['y']), self.my_coins, self.coins)

        for platform in self.my_platforms:
            self.platforms.append(platform)
        for spike in self.my_spikes:
            self.spikes.append(spike)
        for coin in self.my_coins:
            self.coins.append(coin)

    def __del__(self):
        for _ in self.my_platforms:
            self.platforms.popleft()
        for _ in self.my_spikes:
            self.spikes.popleft()
        for _ in self.my_coins:
            self.coins.popleft()


class Stage:
    def __init__(self):

        # deque står for 'double ended queue', og er lister hvor man
        # hurtigt og effektivt kan tilføje og fjerne elementer fra begge ender

        self.platforms = deque()
        self.spikes = deque()
        self.coins = deque()

        self.segment_amount = 1

        self.segments = deque([StageSegment(0, 0, self.platforms, self.spikes, self.coins)])

    def update(self, scroll):
        # remove segment when out of frame
        if self.segments[0].position + self.segments[0].length < scroll:
            self.segments.popleft()

        # add new segment
        if self.segments[-1].position + self.segments[-1].length < scroll + 1920:
            segment_id = random.randint(1, self.segment_amount)
            start_point = self.segments[-1].position + self.segments[-1].length + 300
            self.segments.append(StageSegment(segment_id, start_point, self.platforms, self.spikes, self.coins))
