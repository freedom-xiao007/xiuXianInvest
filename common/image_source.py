import pygame

from common import five_element


class GameImageSource(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.game_images_of_file_element = {}

    def load(self):
        metal = pygame.image.load(r".\img\metal.png").convert_alpha()
        wood = pygame.image.load(r".\img\wood.png").convert_alpha()
        water = pygame.image.load(r".\img\water.png").convert_alpha()
        fire = pygame.image.load(r".\img\fire.png").convert_alpha()
        earth = pygame.image.load(r".\img\earth.png").convert_alpha()
        self.game_images_of_file_element = {
            five_element.FiveElementType.METAL: metal,
            five_element.FiveElementType.WOOD: wood,
            five_element.FiveElementType.WATER: water,
            five_element.FiveElementType.FIRE: fire,
            five_element.FiveElementType.EARTH: earth,
        }

    def get_five_element_image(self, type: five_element.FiveElementType):
        self.load()
        return self.game_images_of_file_element[type]

    def get_all_alpha_img(self):
        return pygame.image.load(r".\img\alpha.png").convert_alpha()