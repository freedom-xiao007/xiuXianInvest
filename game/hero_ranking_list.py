import pygame.sprite
from game import hero
from common import xiuxian_state


class HeroRankingList(pygame.sprite.Sprite):
    def __init__(self, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 400))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.font = font

        self.title = font.render("当前游戏修士排行榜", True, (255, 0, 0), (0, 0, 0))
        self.image.blit(self.title, [40, 5])

        self.info = font.render("当前无排行信息", True, (255, 0, 0), (0, 0, 0))
        self.image.blit(self.info, [10, 25])

    def update(self):
        self.image.fill((0, 0, 0))
        self.title = self.font.render("当前游戏修士排行榜", True, (255, 0, 0), (0, 0, 0))
        self.image.blit(self.title, [40, 5])

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
