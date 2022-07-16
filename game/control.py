import sys
import time

import pygame

import game.land
from game import hero
from common import config
from game import hero_ranking_list
from game import play
from game import card
from game import operate_log
from common import xiuxian_state


end_game_stamp = None
game_pre_stamp = None


def start():
    fps = 20
    pygame.init()
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
    pygame.time.set_timer(hero_move_event, 1000 * 30)

    # 游戏角色排行榜
    hero_ranking = hero_ranking_list.HeroRankingList(samil_font)
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

    # 灵气潮汐：修炼速度加快
    reiki_event = pygame.USEREVENT + 5
    pygame.time.set_timer(reiki_event, 1000 * 5)

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
            if event.type == play_info_event:
                play_info_group.update()
            if event.type == reiki_event:
                game.land.upgrade()

        screen.fill((255, 255, 255))
        surface2.fill((255, 255, 255, 0))

        if game.control.game_pre_stamp is not None:
            pre_game(screen, surface2, font, clock, fps)
            continue

        if is_end():
            end(screen, surface2, font, clock, fps)
            continue

        for item in game.land.Lands:
            pygame.draw.rect(surface2, item.five_element.value["color"], (item.x, item.y, item.length, item.length), 3)

            number = font.render(str(item.index), True, (255, 10, 10))
            text_pos = number.get_rect(center=(item.x + 15, item.y + 15))
            screen.blit(number, text_pos)

            five_element = font.render(item.five_element.value["type"], True, (255, 10, 10))
            type_pos = five_element.get_rect(center=(item.x + 15, item.y + 80))
            screen.blit(five_element, type_pos)

            exp = samil_font.render("exp:" + str(item.exp), True, (255, 10, 10))
            exp_pos = five_element.get_rect(center=(item.x + 60, item.y + 20))
            screen.blit(exp, exp_pos)

        hero_ranking.update()
        hero.Hero_groups.update()
        hero.collide(samil_font)
        hero.Hero_groups.draw(surface2)

        hero_ranking_group.draw(surface2)
        play_info_group.draw(surface2)
        card_info_group.draw(surface2)
        operate_group.draw(surface2)

        screen.blit(surface2, (0, 0))
        pygame.display.flip()
        clock.tick(fps)


def pre_game(screen, surface2, font, clock, fps):
    interval = int(time.time()) - int(game.control.game_pre_stamp)
    if interval > 30:
        game.control.game_pre_stamp = None
        hero.reset()
        game.land.reset()

    text = [
        "新的轮回开始了，当前阶段盲选，成功登顶后，奖励翻10倍",
        "输入 t + 角色编号进行投资吧",
        "当前角色编号范围：0-125",
        "%d秒后，开始游戏" % (30-interval),
    ]
    for i in range(len(text)):
        end_info = font.render(text[i], True, (255, 10, 10))
        text_pos = end_info.get_rect(center=(800, 400 + 20 * i))
        screen.blit(end_info, text_pos)

    screen.blit(surface2, (0, 0))
    pygame.display.flip()
    clock.tick(fps)


def is_end():
    alive = 0
    has_top = False
    for item in hero.Heroes:
        if item.alive:
            alive = alive + 1
            if item.state == (len(xiuxian_state.State) - 1):
                has_top = True
                break
    if has_top or alive <= 1:
        return True
    return False


def end(screen, surface2, font, clock, fps):
    if game.control.end_game_stamp is None:
        game.control.end_game_stamp = time.time()
    elif int(time.time()) - int(game.control.end_game_stamp) > 5:
        game.control.game_pre_stamp = time.time()

    text = [
        "此轮游戏结束，将开始下次轮回",
        "修仙之巅：" + get_win_hero(),
    ]
    for i in range(len(text)):
        end_info = font.render(text[i], True, (255, 10, 10))
        text_pos = end_info.get_rect(center=(800, 400 + 20 * i))
        screen.blit(end_info, text_pos)

    screen.blit(surface2, (0, 0))
    pygame.display.flip()
    clock.tick(fps)


def get_win_hero():
    for item in hero.Heroes:
        if item.alive:
            return item.name
    return ""
