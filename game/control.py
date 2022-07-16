import sys

import pygame

import game.land
from game import hero
from common import config
from game import hero_ranking_list
from game import play
from game import card
from game import operate_log


def start():
    pygame.init()
    fps = 60
    win_size = (config.WIN_WIDTH, config.WIN_HEIGHT)
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption("修仙投资")

    font = pygame.font.SysFont("SimHei", 20)
    samil_font = pygame.font.SysFont("SimHei", 10)

    # 角色修炼事件
    hero_exp_event = pygame.USEREVENT + 1
    pygame.time.set_timer(hero_exp_event, 1000)

    # 角色气运劫：角色开始移动，期间膨胀发送战斗
    hero_move_event = pygame.USEREVENT + 2
    pygame.time.set_timer(hero_move_event, 1000 * 10)

    # 游戏角色排行榜
    hero_rank_event = pygame.USEREVENT + 3
    pygame.time.set_timer(hero_rank_event, 1000)
    hero_ranking = hero_ranking_list.HeroRankingList(font)
    hero_ranking_group = pygame.sprite.Group()
    hero_ranking_group.add(hero_ranking)

    # 玩家排行和教程显示
    play_info_event = pygame.USEREVENT + 4
    pygame.time.set_timer(play_info_event, 1000 * 10)
    play_info = play.PlayInfo(samil_font)
    play_info_group = pygame.sprite.Group()
    play_info_group.add(play_info)
    play_info_group.update()

    # 卡牌详情展示
    card_info = card.Card(samil_font)
    card_info_group = pygame.sprite.Group()
    card_info_group.add(card_info)
    card_info_group.update()

    # 操作日志显示
    operate_group = pygame.sprite.Group()
    operate_group.add(operate_log.OperateLog(samil_font))

    surface2 = screen.convert_alpha()  # 关键是这里！！！
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == hero_move_event:
                hero.random_move(samil_font)
            elif event.type == hero_exp_event:
                hero.update_exp(samil_font)
            if event.type == hero_rank_event:
                hero_ranking.update()
            if event.type == play_info_event:
                play_info_group.update()

        if is_end():
            break

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

        hero.Hero_groups.update()
        hero.collide()
        hero.Hero_groups.draw(surface2)

        hero_ranking_group.draw(surface2)
        play_info_group.draw(surface2)
        card_info_group.draw(surface2)
        operate_group.draw(surface2)

        screen.blit(surface2, (0, 0))
        pygame.display.flip()
        clock.tick(fps)


def is_end():
    alive = 0
    for item in hero.Heroes:
        if item.alive:
            alive = alive + 1
    if alive <= 1:
        return True
    return False