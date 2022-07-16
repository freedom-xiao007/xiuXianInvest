import random

import common.config
from common.five_element import FiveElementType
from common import five_element

LAND_LENGTH = 100
INTERVAL = 5


class Land:
    def __init__(self, x: int, y: int, five_element: FiveElementType, index: int):
        self.x = x + INTERVAL
        self.y = y + INTERVAL
        self.length = LAND_LENGTH - INTERVAL
        self.five_element = five_element
        self.index = index
        self.exp = random.randint(1, 10)


def create_lands():
    x_count = int(common.config.WIN_WIDTH / LAND_LENGTH)
    y_count = int(common.config.WIN_HEIGHT / LAND_LENGTH)
    nodes = []
    for i in range(x_count):
        for j in range(y_count):
            x = i * LAND_LENGTH
            y = j * LAND_LENGTH
            nodes.append(Land(x, y, five_element.get_random_five_element(), i * y_count + j))
    for item in nodes:
        print((item.index, item.x, item.y, item.length))
    return nodes


Lands = create_lands()
