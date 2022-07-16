from common.five_element import FiveElementType
from common import config
from common import five_element
from game import land
from common import xiuxian_state


class Hero:
    def __init__(self, x: int, y: int, five_element: FiveElementType):
        self.x = x
        self.y = y
        self.five_element = five_element
        self.state = 0
        self.exp = 0
        self.level = 1
        self.log = ""
        self.is_top = False

    def update(self):
        if self.is_top:
            return

        self.log = ""

        y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
        i = int((self.x - 50) / config.UNIT_LENGTH)
        j = int((self.y - 75) / config.UNIT_LENGTH)
        land_index = i * y_count + j
        cur_land = land.Lands[land_index]
        add_exp = cur_land.exp
        if self.five_element == cur_land.five_element:
            add_exp = add_exp * 2
        self.exp = self.exp + add_exp
        self.log = "修炼+%d" % add_exp

        if self.state >= len(xiuxian_state.State):
            return

        print(self.state, self.level)
        while self.exp >= xiuxian_state.State[self.state]["exp"]:
            self.exp = self.exp - xiuxian_state.State[self.state]["exp"]
            self.level = self.level + 1

            if self.level >= xiuxian_state.State[self.state]["level"]:
                self.state = self.state + 1
                self.level = 1

            if self.state < len(xiuxian_state.State):
                self.log = "突破：%s%d层" % (xiuxian_state.State[self.state]["name"], self.level)
            else:
                self.is_top = True
                self.state = self.state - 1
                self.level = xiuxian_state.State[self.state]["level"]
                break


def create_heroes():
    x_count = int(config.WIN_WIDTH / config.UNIT_LENGTH)
    y_count = int(config.WIN_HEIGHT / config.UNIT_LENGTH)
    list = []
    for i in range(x_count):
        for j in range(y_count):
            x = i * config.UNIT_LENGTH + 50
            y = j * config.UNIT_LENGTH + 75
            list.append(Hero(x, y, five_element.get_random_five_element()))
    for item in list:
        print((item.x, item.y))
    return list


def update_exp():
    for item in Heroes:
        item.update()


Heroes = create_heroes()