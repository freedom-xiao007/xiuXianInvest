import pygame.sprite
from game import hero
from common import xiuxian_state
from common import color


class HeroRankingList(pygame.sprite.Sprite):
    def __init__(self, big_font, small_font):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r"C:\Users\lw\Pictures\Saved Pictures\alpha.png").convert_alpha()
        self.image = pygame.transform.scale(img, (250, 420))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.big_font = big_font
        self.small_font = small_font
        self.update()

    def update(self):
        self.image.fill(color.BLUE1)
        self.title = self.big_font.render("当前游戏修士排行榜", True, color.RED1)
        self.image.blit(self.title, [10, 0])

        rank_info = get_rank_info()
        for i in range(len(rank_info)):
            t = self.small_font.render(str(i + 1) + " " + rank_info[i], True, color.BLACK)
            self.image.blit(t, [10, 27 * (i + 1)])


def get_rank_info():
    rank = {}
    for item in hero.Heroes:
        if not item.alive:
            continue
        key = "编号:%d %s %s%d层 血量:%d" % (item.index, item.name, xiuxian_state.State[item.state]["name"], item.level, item.bleed)
        rank[key] = item.state * 100 + item.level

    info = []
    top = 15
    for value in sorted(rank.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if top < 0:
            break
        top = top - 1
        info.append(value[0])
    return info
