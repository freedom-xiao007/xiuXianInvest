import random

import pygame.sprite

from common.five_element import FiveElementType
from common import config
from common import five_element
from game import land
from common import xiuxian_state


hero_names = [
    "东皇太一",
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
    "紫微大帝",
    "青华大帝",
    "西王母",
    "东王公",
    "真武大帝",
    "玉虚真人",
    "佑圣真人",
    "斗姆帝君",
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
    "太白金星",
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
    "天蓬元帅",
    "卷帘大将",
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
    def __init__(self, index: int, x: int, y: int, five_element: FiveElementType, images):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.img = images.get_all_alpha_img()
        self.image = pygame.transform.scale(self.img, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x - 10
        self.rect.y = y - 40
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
        self.bleed = 100
        self.alive = True
        self.attack = 1 * self.level + 10 * self.state
        self.is_attack = False
        self.name = "无名"
        self.font = pygame.font.SysFont("SimHei", 10)
        if self.index < len(hero_names):
            self.name = hero_names[self.index]

    def update(self):
        if self.is_moving:
            self.moving()

    def update_info(self, font):
        self.image.fill((255, 255, 255, 0))

        color = self.five_element.value["color"]
        pygame.draw.circle(self.image, color, (10, 50), self.radius, 10)

        if self.five_element == five_element.FiveElementType.METAL:
            color = (0, 0, 0)
            number = self.font.render(str(self.index), True, (0, 0, 0))
        else:
            number = self.font.render(str(self.index), True, (255, 255, 255))
        self.image.blit(number, [2, 45])

        state_str = "%s%d层" % (xiuxian_state.State[self.state]["name"], self.level)
        title = self.font.render(state_str, True, color)
        self.image.blit(title, [0, 20])

        if self.log != "":
            log = font.render(self.log, True, color)
            self.image.blit(log, [0, 0])

        name = self.font.render(self.name, True, color)
        self.image.blit(name, [20, 45])

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
        if self.is_top or self.is_moving or self.is_attack:
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

        self.bleed = 1000 * (self.state + 1)
        self.attack = 1 * self.level + 10 * self.state
        self.update_info(font)

    def collide(self, grp, font):
        self.is_attack = False
        if pygame.sprite.spritecollideany(self, grp):
            target = pygame.sprite.spritecollideany(self, grp)
            if target.collide_type == 'hero':
                if self.index == target.index:
                    return
                cur_hero = "%s%d层" % (xiuxian_state.State[self.state]["name"], self.level)
                target_hero = "%s%d层" % (xiuxian_state.State[target.state]["name"], target.level)
                # print("发生碰撞:", self.index, target.index, cur_hero, target_hero)
                self.fire(target, font)
                self.is_attack = True

    def fire(self, target, font):
        reduce = random.randint(0, target.attack)
        self.bleed = self.bleed - reduce
        self.log = "血量-%d" % reduce

        reduce = random.randint(0, self.attack)
        target.bleed = target.bleed - reduce
        target.log = "血量-%d" % reduce

        self.update_info(font)
        target.update_info(font)
        dead_check(self)
        dead_check(target)


def dead_check(hero: Hero):
    if hero.bleed < 1:
        if random.randint(0, 10) == 5:
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


def create_heroes(images):
    x_count = int((config.WIN_WIDTH - config.LEFT_WIDTH - config.RIGHT_WIDTH) / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    list = []
    group = pygame.sprite.Group()
    for i in range(x_count):
        for j in range(y_count):
            x = i * config.UNIT_LENGTH + 50 + config.LEFT_WIDTH
            y = j * config.UNIT_LENGTH + 75
            sprite = Hero(i * y_count + j, x, y, five_element.get_random_five_element(), images)
            list.append(sprite)
            group.add(sprite)
    return list, group


def random_move(font):
    x_count = int((config.WIN_WIDTH - config.LEFT_WIDTH - config.RIGHT_WIDTH) / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    for item in Heroes:
        if not item.alive:
            continue
        random_x = random.randint(0, x_count-1) * config.UNIT_LENGTH + 40 + config.LEFT_WIDTH
        random_y = random.randint(0, y_count-1) * config.UNIT_LENGTH + 35
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


def collide(font):
    for item in Heroes:
        if not item.alive:
            continue
        item.collide(Hero_groups, font)


def add_hero_rel_player(hero_no, player_name):
    if hero_no not in hero_rel_player:
        hero_rel_player[hero_no] = []
    if player_name not in hero_rel_player[hero_no]:
        hero_rel_player[hero_no].append(player_name)


def has_invest(player_name):
    for hero_no in hero_rel_player:
        for name in hero_rel_player[hero_no]:
            if name == player_name:
                if hero_no in Heroes and Heroes[hero_no].alive:
                    return True, hero_names[hero_no]
    return False, ""


hero_rel_player = {}
Heroes, Hero_groups = [], None
