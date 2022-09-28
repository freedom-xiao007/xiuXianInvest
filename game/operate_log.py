import pygame.sprite
from common import color
from game import player_commond


class OperateLog(pygame.sprite.Sprite):
    def __init__(self, big_font, small_font):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r".\img\alpha.png").convert_alpha()
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
        logs = player_commond.player_instance.get_log_cache()
        for i in range(len(logs)):
            t = self.small_font.render(logs[i], True, color.BLACK)
            self.image.blit(t, [10, 27 * (i + 1)])
