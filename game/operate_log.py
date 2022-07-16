import pygame.sprite


class OperateLog(pygame.sprite.Sprite):
    def __init__(self, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((250, 400))
        self.rect = self.image.get_rect()
        self.rect.x = 1655
        self.rect.y = 450
        self.font = font
        self.update()

    def update(self):
        self.image.fill((0, 0, 0))
        title = self.font.render("玩家交互与操作日志", True, (255, 0, 0), (0, 0, 0))
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
