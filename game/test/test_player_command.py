import unittest
from game import player_commond
from game import hero
from game import card


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.play = player_commond.Player()

    def test_parse_invest(self):
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：t2"), "0萧0 投资了 %s" % hero.hero_names[2])
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：t20"), "0萧0 投资了 %s" % hero.hero_names[20])
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：t125"), "0萧0 投资了 %s" % hero.hero_names[125])
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：t0"), "0萧0 投资了 %s" % hero.hero_names[0])
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：t-1"), None)
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：t200"), "0萧0 指令错误，角色编号不存在")

    def test_parse_card(self):
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.0"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[0].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.1"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[1].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.2"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[2].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.3"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[3].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.4"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[4].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.5"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[5].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.6"), "0萧0 对 %s 使用 %s" % (hero.hero_names[2], card.cards[6].value["name"]))
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.10"), None)
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j2.-1"), None)
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j-1.0.23"), None)
        self.assertEqual(self.play.exe_command("[11953515] 0萧0：j200.0"), "0萧0 指令错误")
