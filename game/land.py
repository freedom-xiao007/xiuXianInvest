import random

import pygame

import common.config
from common.five_element import FiveElementType
from common import five_element
from common import config
from common import color

LAND_LENGTH = 100
INTERVAL = 5


class Land(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, five_element: FiveElementType, index: int, img, big_font, small_font):
        self.x = x + INTERVAL
        self.y = y + INTERVAL
        self.img = img
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.image = pygame.transform.scale(self.img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.length = LAND_LENGTH - INTERVAL
        self.five_element = five_element
        self.index = index
        self.level = 1
        self.exp = random.randint(1, 10) * self.level
        self.big_font = big_font
        self.small_font = small_font
        self.update()

    def update(self):
        self.image.fill((255, 255, 255, 0))
        self.image = pygame.transform.scale(self.img, (100, 100))
        pygame.draw.rect(self.image, (255, 255, 255, 125), (0, 0, 100, 100), 1)

        number = self.big_font.render(str(self.index), True, color.BLACK)
        text_pos = number.get_rect(center=(15, 15))
        self.image.blit(number, text_pos)

        five_element = self.big_font.render(self.five_element.value["type"], True, color.BLACK)
        type_pos = five_element.get_rect(center=(15, 80))
        self.image.blit(five_element, type_pos)

        exp = self.small_font.render("exp:" + str(self.exp), True, color.BLACK)
        exp_pos = five_element.get_rect(center=(60, 20))
        self.image.blit(exp, exp_pos)


def create_lands(images, big_font, small_font):
    x_count = int((common.config.WIN_WIDTH - config.LEFT_WIDTH - config.RIGHT_WIDTH) / LAND_LENGTH)
    y_count = int(common.config.WIN_HEIGHT / LAND_LENGTH)
    nodes = []
    group = pygame.sprite.Group()
    for i in range(x_count):
        for j in range(y_count):
            x = i * LAND_LENGTH + config.LEFT_WIDTH
            y = j * LAND_LENGTH
            element = five_element.get_random_five_element()
            land = Land(x, y, element, i * y_count + j, images.get_five_element_image(element), big_font, small_font)
            nodes.append(land)
            group.add(land)
    return nodes, group


def upgrade():
    for item in Lands:
        item.level = item.level + 1
        item.exp = random.randint(1, 100) * item.level
        item.update()


def reset():
    for item in Lands:
        item.level = 1
        item.exp = random.randint(0, 10)


Lands, Land_group = None, None
