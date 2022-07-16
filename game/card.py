import pygame.sprite


class Card(pygame.sprite.Sprite):
    def __init__(self, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 400))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 450
        self.font = font

    def update(self):
        self.show_play_tourist()

    def show_play_tourist(self):
        self.image.fill((0, 0, 0))
        title = self.font.render("游戏卡牌列表::括号内为所需金币", True, (255, 0, 0), (0, 0, 0))
        self.image.blit(title, [40, 5])

        info = [
            "移动卡(10)：指定人物移动到特定格子进行停留",
            "加速卡(10)： 修炼速度翻倍",
            "屏蔽卡(10):屏蔽后续其他玩家卡牌影响",
            "扰乱卡(10):制定格子上的修炼速度随机降低",
            "心魔卡(10):制定格子上的角色下次突破失败",
            "静止卡(10):角色下阶段不移动",
            "护身卡(10):战败时无损伤败走：",
        ]
        for i in range(len(info)):
            t = self.font.render(info[i], True, (255, 0, 0), (0, 0, 0))
            self.image.blit(t, [10, 25 * (i + 1)])