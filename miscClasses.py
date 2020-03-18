class Coin:
    def __init__(self, position):
        pass

    def update(self):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Obstacle:
    def __init__(self, position):
        pass

    def update(self):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Enemy:
    def __init__(self, position):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Gun:
    def __init__(self):
        pass

    def update(self, position, shoot_pressed):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Projectile:
    def __init__(self, position, rotation):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen, scroll, scale):
        pass


class Button:
    def __init__(self, position, scale, images):
        pass

    def update(self, mouse_pos, mouse_clicked):
        pass

    def draw(self, screen, scale):
        pass
