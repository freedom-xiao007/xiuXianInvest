import pygame.sprite
from common import color


class OperateLog(pygame.sprite.Sprite):
    def __init__(self, big_font, small_font):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r"C:\Users\lw\Pictures\Saved Pictures\alpha.png").convert_alpha()
        self.image = pygame.transform.scale(img, (250, 420))
        self.rect = self.image.get_rect()
        self.rect.x = 1655
        self.rect.y = 450
        self.big_font = big_font
        self.small_font = small_font
        self.update()

    def update(self):
        title = self.big_font.render("玩家交互与操作日志", True, color.RED1)
        self.image.blit(title, [10, 0])

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
            t = self.small_font.render(info[i], True, color.BLACK)
            self.image.blit(t, [10, 27 * (i + 1)])
