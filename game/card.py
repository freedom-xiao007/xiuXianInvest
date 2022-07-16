import pygame.sprite
from common import color


class Card(pygame.sprite.Sprite):
    def __init__(self, big_font, small_font):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r"C:\Users\lw\Pictures\Saved Pictures\alpha.png").convert_alpha()
        self.image = pygame.transform.scale(img, (250, 400))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 450
        self.big_font = big_font
        self.small_font = small_font

    def update(self):
        self.show_play_tourist()

    def show_play_tourist(self):
        title = self.big_font.render("游戏卡牌列表", True, color.RED1)
        self.image.blit(title, [10, 0])

        info = [
            "提示：括号内为所需金币",
            "移动卡(10)：指定人物移动到特定格子进行停留",
            "加速卡(10)： 修炼速度翻倍",
            "屏蔽卡(10):屏蔽后续其他玩家卡牌影响",
            "扰乱卡(10):制定格子上的修炼速度随机降低",
            "心魔卡(10):制定格子上的角色下次突破失败",
            "静止卡(10):角色下阶段不移动",
            "护身卡(10):战败时无损伤败走：",
        ]
        for i in range(len(info)):
            t = self.small_font.render(info[i], True, color.BLACK)
            self.image.blit(t, [10, 27 * (i + 1)])