import random

import pygame.sprite

from common.five_element import FiveElementType
from common import config
from common import five_element
from game import land
from common import xiuxian_state
from game import hero as hero_set


hero_names = [
    "东皇",
    "太一",
    "昊天",
    "女娲",
    "伏羲",
    "神农",
    "轩辕",
    "句龙",
    "祝融",
    "共工",
    "飞廉",
    "夸父",
    "蚩尤",
    "刑天",
    "仓颉",
    "喾",
    "尧",
    "舜",
    "禹",
    "后羿",
    "羲和",
    "嫦娥",
    "常羲",
    "应龙",
    "女魃",
    "旱魃",
    "烛龙",
    "元始",
    "通天",
    "太上",
    "紫微",
    "青华",
    "西王母",
    "东王公",
    "真武",
    "玉虚",
    "佑圣",
    "斗姆",
    "汉锺离",
    "吕洞宾",
    "张果老",
    "韩湘子",
    "铁拐李",
    "何仙姑",
    "蓝采和",
    "曹国舅",
    "鬼谷子",
    "张道陵",
    "许逊",
    "葛玄",
    "萨守坚",
    "魏伯阳",
    "魏华存",
    "葛洪",
    "寇谦之",
    "陆修静",
    "郭璞",
    "陶弘景",
    "王文卿",
    "刘海蟾",
    "张伯端",
    "王重阳",
    "丘处机",
    "张三丰",
    "太白",
    "毕方",
    "二郎神",
    "赵公明",
    "温元帅",
    "康元帅",
    "马天君",
    "王天君",
    "钟馗",
    "孟婆",
    "陆压",
    "接引",
    "准提",
    "广成子",
    "赤精子",
    "云中子",
    "雷震子",
    "韦护",
    "李靖",
    "金吒",
    "木吒",
    "哪吒",
    "牛郎",
    "织女",
    "千里眼",
    "顺风耳",
    "月老",
    "镇元大仙",
    "菩提祖师",
    "天蓬",
    "卷帘",
    "三藏",
    "孙悟空",
    "牛魔王",
    "蛟魔王",
    "鹏魔王",
    "狮狔王",
    "猕猴王",
    "禺狨王",
    "六耳",
    "鲲鹏",
    "白泽",
    "石矶",
    "太乙",
    "姜尚",
    "申公豹",
    "云霄",
    "碧霄",
    "琼霄",
    "金光仙",
    "乌云仙",
    "毗卢仙",
    "灵牙仙",
    "虬首仙",
    "金箍仙",
    "定光仙",
    "多宝道人",
    "金灵圣母",
    "无当圣母",
    "龟灵圣母",
    "秦完",
    "赵江",
    "董全",
    "袁角",
    "金光圣母",
    "孙良",
    "白礼",
    "姚宾",
    "王奕",
    "张绍",
    "九曜星官",
    "闻仲",
    "鸿均",
]


class Hero(pygame.sprite.Sprite):
    def __init__(self, index: int, x: int, y: int, five_element: FiveElementType):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x - 20
        self.rect.y = y - 30
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
        self.speed = 3
        self.index = index
        self.bleed = 100
        self.alive = True
        self.name = "无名"
        if self.index < len(hero_names):
            self.name = hero_names[self.index]

    def update(self):
        if self.is_moving:
            self.moving()

    def update_info(self, font):
        self.image.fill((255, 255, 255, 0))

        state_str = "%s%d层" % (xiuxian_state.State[self.state]["name"], self.level)
        title = font.render(state_str, True, (255, 0, 0), (0, 0, 0))
        self.image.blit(title, [0, 20])

        if self.log != "":
            log = font.render(self.log, True, (0, 255, 0))
            self.image.blit(log, [0, 0])

        name = font.render(self.name, True, (255, 0, 0), (0, 0, 0))
        self.image.blit(name, [15, 35])
        pygame.draw.circle(self.image, self.five_element.value["color"], (25, 40), self.radius, 2)

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

    def get_exp(self, font):
        if self.is_top or self.is_moving:
            return

        self.log = ""

        y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
        i = int((self.rect.x - 50 - 20 - config.LEFT_WIDTH) / config.UNIT_LENGTH)
        j = int((self.rect.y - 75 - 30) / config.UNIT_LENGTH)
        land_index = i * y_count + j
        if land_index >= len(land.Lands):
            return
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

        self.bleed = 100 * self.state
        self.update_info(font)

    def collide(self, grp):
        if pygame.sprite.spritecollideany(self, grp):
            target = pygame.sprite.spritecollideany(self, grp)
            if target.collide_type == 'hero':
                if self.index == target.index:
                    return
                cur_hero = "%s%d层" % (xiuxian_state.State[self.state]["name"], self.level)
                target_hero = "%s%d层" % (xiuxian_state.State[target.state]["name"], target.level)
                print("发生碰撞:", self.index, target.index, cur_hero, target_hero)
                self.fire(target)

    def fire(self, target):
        if self.state < target.state:
            reduce = random.randint(0, 10) * (target.state - self.state)
            self.bleed = self.bleed - reduce
            print(self.index, "不敌", target.index, "，减血：", reduce)
        elif self.state > target.state:
            reduce = random.randint(0, 10) * (self.state - target.state)
            target.bleed = target.bleed - reduce
            print(target.index, "不敌", self.index, "，减血：", reduce)
        elif self.state == target.state:
            if self.level <= target.level:
                reduce = random.randint(0, 10)
                self.bleed = self.bleed - reduce
                print(self.index, "不敌", target.index, "，减血：", reduce)
            else:
                reduce = random.randint(0, 10)
                target.bleed = target.bleed - reduce
                print(target.index, "不敌", self.index, "，减血：", reduce)

        dead_check(self)
        dead_check(target)


def dead_check(hero: Hero):
    if hero.bleed < 1:
        if random.randint(0, 10) < 5:
            hero.kill()
            hero.alive = False
            print(hero.index, "被击杀")
        else:
            if hero.state > 1:
                hero.state = hero.state - 1
        x_count = int(config.WIN_WIDTH / config.UNIT_LENGTH)
        y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
        random_x = random.randint(0, x_count - 1) * config.UNIT_LENGTH + 30
        random_y = random.randint(0, y_count - 1) * config.UNIT_LENGTH + 55
        hero.target_x = random_x
        hero.target_y = random_y


def create_heroes():
    x_count = int((config.WIN_WIDTH - config.LEFT_WIDTH - config.RIGHT_WIDTH) / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    list = []
    for i in range(x_count):
        for j in range(y_count):
            x = i * config.UNIT_LENGTH + 50 + config.LEFT_WIDTH
            y = j * config.UNIT_LENGTH + 75
            list.append(Hero(i * y_count + j, x, y, five_element.get_random_five_element()))
    return list


def random_move(font):
    x_count = int((config.WIN_WIDTH - config.LEFT_WIDTH - config.RIGHT_WIDTH) / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    for item in Heroes:
        if not item.alive:
            continue
        random_x = random.randint(0, x_count-1) * config.UNIT_LENGTH + 30 + config.LEFT_WIDTH
        random_y = random.randint(0, y_count-1) * config.UNIT_LENGTH + 45
        item.is_moving = True
        item.log = ""
        item.update_info(font)
        item.target_x = random_x
        item.target_y = random_y


def update_exp(font):
    for item in Heroes:
        if not item.alive:
            continue
        item.get_exp(font)


def collide():
    for item in Heroes:
        if not item.alive:
            continue
        item.collide(Hero_groups)


def reset():
    for item in hero_set.Heroes:
        item.kill()
    hero_set.Heroes.clear()
    hero_set.Heroes = create_heroes()
    hero_set.Hero_groups = pygame.sprite.Group()
    for hero in hero_set.Heroes:
        hero_set.Hero_groups.add(hero)


Heroes = create_heroes()
Hero_groups = pygame.sprite.Group()
for hero in Heroes:
    Hero_groups.add(hero)
