import sys

import pygame

import common.color
import game.land
from game import hero
from common import xiuxian_state


class Number(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.rect.Rect(0, 0, 50, 50)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()


def start():
    pygame.init()
    fps = 60
    win_size = (600, 600)
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption("修仙投资")

    # number_group = pygame.sprite.Group()
    # number_group.add()

    # font = pygame.font.Font(None, 20)
    font = pygame.font.SysFont("SimHei", 20)
    samil_font = pygame.font.SysFont("SimHei", 10)

    # 角色修炼事件
    hero_exp_event = pygame.USEREVENT + 1
    pygame.time.set_timer(hero_exp_event, 1000)

    surface2 = screen.convert_alpha()  # 关键是这里！！！
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == hero_exp_event:
                hero.update_exp()

        screen.fill((255, 255, 255))
        surface2.fill((255, 255, 255, 0))

        for item in game.land.Lands:
            pygame.draw.rect(surface2, item.five_element.value["color"], (item.x, item.y, item.length, item.length), 3)

            number = font.render(str(item.index), True, (255, 10, 10))
            text_pos = number.get_rect(center=(item.x + 15, item.y + 15))
            screen.blit(number, text_pos)

            five_element = font.render(item.five_element.value["type"], True, (255, 10, 10))
            type_pos = five_element.get_rect(center=(item.x + 75, item.y + 15))
            screen.blit(five_element, type_pos)

        for item in hero.Heroes:
            pygame.draw.circle(surface2, item.five_element.value["color"], (item.x, item.y), 15, 2)

            five_element = font.render(item.five_element.value["type"], True, (255, 10, 10))
            type_pos = five_element.get_rect(center=(item.x, item.y))
            screen.blit(five_element, type_pos)

            state_str = "%s%d层" % (xiuxian_state.State[item.state]["name"], item.level)
            state = samil_font.render(state_str, True, (255, 10, 10))
            state_pos = five_element.get_rect(center=(item.x - 10, item.y - 20))
            screen.blit(state, state_pos)

            if item.log != "":
                log = samil_font.render(item.log, True, (0, 0, 0))
                log_pos = five_element.get_rect(center=(item.x - 20, item.y - 30))
                screen.blit(log, log_pos)

        screen.blit(surface2, (0, 0))
        pygame.display.flip()
        clock.tick(fps)