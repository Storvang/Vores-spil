import pygame, os, math
from miscClasses import GameObject

projectile_img = pygame.image.load(os.path.join('Assets', 'Guns', 'Projectile', 'Projectile.png'))
fading_projectile_img = pygame.image.load(os.path.join('Assets', 'Guns', 'Projectile', 'Fading Projectile.png'))
collision_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'projectile to ground.wav'))

projectile_hit = []
for i in range(5):
    path = os.path.join('Assets', 'Guns', 'Projectile', 'Projectile Hit', 'Projectile Hit' + str(i) + '.png')
    projectile_hit.append(pygame.image.load(path))


class Projectile(GameObject):
    def __init__(self, position, direction, speed, range, projectiles, colliders):
        self.speed = speed
        GameObject.__init__(self, position, (40, 20), projectile_img, direction)

        self.projectiles = projectiles
        self.projectiles.append(self)

        self.colliders = colliders

        self.range = range
        self.travelled = 0.0

        self.anim = 'flying'
        self.pre_anim = None
        self.anim_time = 0

    def collide_line(self, start_point, end_point):
        start_point = pygame.Vector2(start_point)
        end_point = pygame.Vector2(end_point)

        intersection = pygame.Vector2()

        if start_point.x == end_point.x and self.pre_position.x == self.position.x:
            return False, None

        elif start_point.x == end_point.x:
            intersection.x = start_point.x

            a1 = (self.position.y - self.pre_position.y) / (self.position.x - self.pre_position.x)
            b1 = self.pre_position.y - a1 * self.pre_position.x

            intersection.y = a1 * intersection.x + b1

            valid_1 = min(start_point.y, end_point.y) <= intersection.y <= max(start_point.y, end_point.y)
            valid_2 = (min(self.pre_position.y, self.position.y) <= intersection.y
                       <= max(self.pre_position.y, self.position.y))

        elif self.pre_position.x == self.position.x:
            intersection.x = self.position.x

            a2 = (end_point.y - start_point.y) / (end_point.x - start_point.x)
            b2 = start_point.y - a2 * start_point.x

            intersection.y = a2 * intersection.x + b2

            valid_1 = min(start_point.x, end_point.x) <= intersection.x <= max(start_point.x, end_point.x)
            valid_2 = (min(self.pre_position.x, self.position.x) <= intersection.x
                       <= max(self.pre_position.x, self.position.x))

        else:
            a1 = (self.position.y - self.pre_position.y) / (self.position.x - self.pre_position.x)
            b1 = self.pre_position.y - a1 * self.pre_position.x

            a2 = (end_point.y - start_point.y) / (end_point.x - start_point.x)
            b2 = start_point.y - a2 * start_point.x

            if a1 == a2:
                return False, None

            intersection.x = (b1 - b2) / (a2 - a1)
            intersection.y = intersection.x * a1 + b1

            valid_1 = min(start_point.x, end_point.x) <= intersection.x <= max(start_point.x, end_point.x)
            valid_2 = (min(self.pre_position.x, self.position.x) <= intersection.x
                       <= max(self.pre_position.x, self.position.x))

        valid = valid_1 and valid_2

        return valid, intersection

    def collide_rect(self, rect):
        hit_side = 0
        intersections = [None]*4

        if self.position.x > self.pre_position.x:
            vert_side, intersections[0] = self.collide_line(rect.topleft, rect.bottomleft)
            if vert_side:
                hit_side = 0
        elif self.position.x < self.pre_position.x:
            vert_side, intersections[2] = self.collide_line(rect.topright, rect.bottomright)
            if vert_side:
                hit_side = 2
        else:
            vert_side = False

        if self.position.y > self.pre_position.y:
            horiz_side, intersections[1] = self.collide_line(rect.topleft, rect.topright)
            if horiz_side:
                hit_side = 1
        elif self.position.y < self.pre_position.y:
            horiz_side, intersections[3] = self.collide_line(rect.bottomleft, rect.bottomright)
            if horiz_side:
                hit_side = 3
        else:
            horiz_side = False

        hit = vert_side or horiz_side
        return hit, hit_side, intersections[hit_side]

        # side1 = self.collide_line(rect.topleft, rect.bottomleft)
        # side2 = self.collide_line(rect.bottomleft, rect.bottomright)
        # side3 = self.collide_line(rect.bottomright, rect.topright)
        # side4 = self.collide_line(rect.topright, rect.topleft)
        #
        # return side1 or side2 or side3 or side4

    def update(self, delta_time):

        # update position
        travel = pygame.Vector2(self.speed * delta_time * math.cos(math.radians(-self.direction)),
                                self.speed * delta_time * math.sin(math.radians(-self.direction)))

        self.travelled += travel.length()

        if self.travelled >= self.range:
            self.projectiles.remove(self)

        self.pre_position = pygame.Vector2(self.position)
        self.position += travel

        # collisions
        for collider in self.colliders:
            hit, hit_side, intersection = self.collide_rect(collider)
            if hit:
                self.position = intersection + pygame.Vector2([(-32, 0), (0, -32), (0, 0), (0, 0)][hit_side])
                self.direction = hit_side * -90
                self.speed = 0
                self.anim = 'hit'

        # anim time
        if self.anim != self.pre_anim:
            self.anim_time = 0
        else:
            self.anim_time += delta_time
        self.pre_anim = self.anim

    def draw(self, screen, scroll, scale):

        # animations
        def flying():
            if self.travelled >= self.range / 2:
                self.image = fading_projectile_img

        def hit():
            self.size = pygame.Vector2(32, 44)
            if self.anim_time >= 0.25:
                self.projectiles.remove(self)
            else:
                self.image = projectile_hit[math.floor((self.anim_time % 0.25) / 0.05)]

        # animate
        if self.anim is not None:
            anim_function = {'flying': flying,
                             'hit': hit}[self.anim]
            anim_function()

        # render
        GameObject.draw(self, screen, scroll, scale)
