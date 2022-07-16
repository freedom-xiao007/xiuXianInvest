import pygame.sprite
from game import hero
from common import xiuxian_state


class PlayInfo(pygame.sprite.Sprite):
    def __init__(self, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 400))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 450
        self.font = font
        self.show_player_rank = False

    def update(self):
        if self.show_player_rank:
            self.show_rank()
            self.show_player_rank = False
        else:
            self.show_play_tourist()
            self.show_player_rank = True

    def show_play_tourist(self):
        self.image.fill((0, 0, 0))
        title = self.font.render("游戏入门教程", True, (255, 0, 0), (0, 0, 0))
        self.image.blit(title, [40, 5])

        info = [
            "洪荒不断轮回，选择中意的角色",
            "角色存活到最后，获得奖励",
            "金币用于购买卡牌，能干扰游戏世界",
            "修炼点用于提升文件修仙等级",
            "游戏角色死亡后，可重新投资",
            "",
            "指令说明：",
            "选择中意投资角色：t + 角色编号",
            "如：t12 (投资12号东皇太一)",
            "对角色使用卡牌：j + 角色编号 + . + 卡牌编号",
            "如：j12.2 对东皇太一使用修炼卡",
            "对角色使用卡牌：d + 区域编号 + . + 卡牌编号",
            "如：d23.3 对区域23使用地形卡",
        ]
        for i in range(len(info)):
            t = self.font.render(info[i], True, (255, 0, 0), (0, 0, 0))
            self.image.blit(t, [10, 25 * (i + 1)])

    def show_rank(self):
        self.image.fill((0, 0, 0))
        title = self.font.render("当前游戏修士排行榜", True, (255, 0, 0), (0, 0, 0))
        self.image.blit(title, [40, 5])

        rank_info = get_rank_info()
        for i in range(len(rank_info)):
            t = self.font.render(str(i + 1) + " " + rank_info[i], True, (255, 0, 0), (0, 0, 0))
            self.image.blit(t, [10, 25 * (i + 1)])


def get_rank_info():
    rank = {}
    for item in hero.Heroes:
        if not item.alive:
            continue
        key = "%d %s%d层" % (item.index, xiuxian_state.State[item.state]["name"], item.level)
        rank[key] = "%d:%d" % (item.state, item.level)

    info = []
    top = 15
    for value in sorted(rank.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if top < 0:
            break
        top = top - 1
        info.append(value[0])
    return info
