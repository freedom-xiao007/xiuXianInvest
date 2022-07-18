import re
from game import hero
from game import card

class Player:
    def __init__(self):
        self.invest_reg = re.compile('.*? (?P<name>.*?)：(?P<type>t)(?P<hero_no>\d+)$')
        self.card_hero_reg = re.compile('.*? (?P<name>.*?)：(?P<type>j)(?P<hero_no>\d+)\.(?P<card_no>[0123456])$')
        self.command_queue = []
        self.log_cache = []

    def exe_command(self, command):
        res = self.invest(command)
        if res is not None:
            return res

        res = self.hero_card(command)
        if res is not None:
            return res

    def invest(self, command):
        match = self.invest_reg.match(command)
        if match is None:
            return None

        res = match.groupdict()
        name = res["name"]
        hero_no = int(res["hero_no"])
        if hero_no < 0 or hero_no >= len(hero.hero_names):
            return "%s 指令错误，角色编号不存在" % res["name"]
        has, invest_hero = hero.has_invest(name)
        if has:
            return invest_hero
        hero.add_hero_rel_player(hero_no, name)
        log = "%s 投资了 %s" % (res["name"], hero.hero_names[hero_no])
        if len(self.log_cache) >= 15:
            self.log_cache.pop()
            self.log_cache.append(log)
        else:
            self.log_cache.append(log)
        return log

    def hero_card(self, command):
        match = self.card_hero_reg.match(command)
        if match is None:
            return None
        res = match.groupdict()
        print(res)
        name = res["name"]
        hero_no = int(res["hero_no"])
        card_no = int(res["card_no"])
        if hero_no < 0 or hero_no >= len(hero.hero_names):
            return "%s 指令错误" % name
        log = "%s 对 %s 使用 %s" % (name, hero.hero_names[hero_no], card.cards[card_no].value["name"])
        if len(self.log_cache) >= 15:
            self.log_cache.pop()
            self.log_cache.append(log)
        else:
            self.log_cache.append(log)
        return log

    def get_log_cache(self):
        return self.log_cache


player_instance = Player()