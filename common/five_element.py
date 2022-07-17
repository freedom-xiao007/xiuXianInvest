import random
from enum import Enum


ALPHA = 255


class FiveElementType(Enum):
    """
    五行：金木水火土
    集群对应的颜色
    """
    METAL = {"color": (255, 255, 0, ALPHA), "type": "金"}
    WOOD = {"color": (0, 51, 0, ALPHA), "type": "木"}
    WATER = {"color": (0, 51, 204, ALPHA), "type": "水"}
    FIRE = {"color": (204, 0, 0, ALPHA), "type": "火"}
    EARTH = {"color": (102, 51, 0, ALPHA), "type": "土"}


Five_element_types = [
    FiveElementType.METAL,
    FiveElementType.WOOD,
    FiveElementType.WATER,
    FiveElementType.FIRE,
    FiveElementType.EARTH,
]


def get_random_five_element():
    return Five_element_types[random.randint(0, 4)]
