# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame

import game.control
from game import hero
from common import image_source
from common import config
from game import land


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    fps = 20
    win_size = (config.WIN_WIDTH, config.WIN_HEIGHT)
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption("修仙投资")

    font = pygame.font.SysFont("SimHei", 20)
    samil_font = pygame.font.SysFont("SimHei", 10)

    images = image_source.GameImageSource()
    images.load()
    land.Lands, land.Land_group = land.create_lands(images, font, samil_font)
    hero.reset()

    game.control.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
