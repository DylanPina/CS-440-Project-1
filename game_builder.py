from game import Game
from ship import Ship
from bots import BotOne, BotTwo, BotThree, BotFour
from config import Bots
from seed import Seed
from typing import List


class GameBuilder():
    def __init__(self):
        self.game = Game()

    def add_bot(self, bot: Bots, q: int = None):
        match bot:
            case Bots.BOT1:
                self.game.set_bot(BotOne(q))
            case Bots.BOT2:
                self.game.set_bot(BotTwo(q))
            case Bots.BOT3:
                self.game.set_bot(BotThree(q))
            case Bots.BOT4:
                self.game.set_bot(BotFour(q))
        return self

    def add_ship(self, D: int, q: int, seed: Seed = None):
        self.game.set_ship(Ship(D, q, seed))
        return self

    def add_seed(self, seed: Seed = None):
        self.game.add_seed(seed)

    def build(self):
        return self.game
