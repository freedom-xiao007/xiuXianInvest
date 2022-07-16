import random

import pygame.sprite

from common.five_element import FiveElementType
from common import config
from common import five_element
from game import land
from common import xiuxian_state


class Hero(pygame.sprite.Sprite):
    def __init__(self, index: int, x: int, y: int, five_element: FiveElementType):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 15
        self.image = pygame.Surface((40, 40))
        pygame.draw.circle(self.image, five_element.value["color"], (x, y), self.radius, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x - 15
        self.rect.y = y - 20
        self.collide_type = "hero"
        self.x = x
        self.y = y
        self.five_element = five_element
        self.state = 0
        self.exp = 0
        self.level = 1
        self.log = ""
        self.is_top = False
        self.is_moving = False
        self.target_x = None
        self.target_y = None
        self.speed = 1
        self.index = index

    def update(self):
        if self.is_moving:
            self.moving()

    def moving(self):
        x_direct = 1
        if (self.target_x - self.rect.x) < 0:
            x_direct = -1
        y_direct = 1
        if (self.target_y - self.rect.y) < 0:
            y_direct = -1

        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.is_moving = False
            return

        if self.rect.x != self.target_x:
            self.rect.x = self.rect.x + self.speed * x_direct
        if self.rect.y != self.target_y:
            self.rect.y = self.rect.y + self.speed * y_direct

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x + self.radius > config.WIN_WIDTH:
            self.rect.x = config.WIN_WIDTH - self.radius * 2
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y + self.radius > config.WIN_HEIGHT:
            self.rect.y = config.WIN_HEIGHT - self.radius

    def get_exp(self):
        if self.is_top or self.is_moving:
            return

        self.log = ""

        y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
        i = int((self.x - 50) / config.UNIT_LENGTH)
        j = int((self.y - 75) / config.UNIT_LENGTH)
        land_index = i * y_count + j
        cur_land = land.Lands[land_index]
        add_exp = cur_land.exp
        if self.five_element == cur_land.five_element:
            add_exp = add_exp * 2
        self.exp = self.exp + add_exp
        self.log = "修炼+%d" % add_exp

        if self.state >= len(xiuxian_state.State):
            return

        while self.exp >= xiuxian_state.State[self.state]["exp"]:
            self.exp = self.exp - xiuxian_state.State[self.state]["exp"]
            self.level = self.level + 1

            if self.level >= xiuxian_state.State[self.state]["level"]:
                self.state = self.state + 1
                self.level = 1

            if self.state < len(xiuxian_state.State):
                self.log = "突破：%s%d层" % (xiuxian_state.State[self.state]["name"], self.level)
            else:
                self.is_top = True
                self.state = self.state - 1
                self.level = xiuxian_state.State[self.state]["level"]
                break

    def collide(self, grp):
        if pygame.sprite.spritecollideany(self, grp):
            target = pygame.sprite.spritecollideany(self, grp)
            if target.collide_type == 'hero':
                if self.index == target.index:
                    return
                # print("发生碰撞")


def create_heroes():
    x_count = int(config.WIN_WIDTH / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    list = []
    for i in range(x_count):
        for j in range(y_count):
            x = i * config.UNIT_LENGTH + 50
            y = j * config.UNIT_LENGTH + 75
            list.append(Hero(i * y_count + j, x, y, five_element.get_random_five_element()))
    return list


def random_move():
    x_count = int(config.WIN_WIDTH / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    for item in Heroes:
        random_x = random.randint(0, x_count-1) * config.UNIT_LENGTH + 30
        random_y = random.randint(0, y_count-1) * config.UNIT_LENGTH + 55
        print("random:", random_x, random_y)
        item.is_moving = True
        item.target_x = random_x
        item.target_y = random_y


def update_exp():
    for item in Heroes:
        item.get_exp()


def collide():
    for item in Heroes:
        item.collide(Hero_groups)


Heroes = create_heroes()
Hero_groups = pygame.sprite.Group()
for hero in Heroes:
    Hero_groups.add(hero)
