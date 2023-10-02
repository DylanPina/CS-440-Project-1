from game import Game
from ship import Ship
from bots import BotOne, BotTwo, BotThree, BotFour
from config import Bots


class GameBuilder():
    def __init__(self):
        self.game = Game()

    def add_bot(self, bot: Bots):
        match bot:
            case Bots.BOT1:
                self.game.set_bot(BotOne())
            case Bots.BOT2:
                self.game.set_bot(BotTwo())
            case Bots.BOT3:
                self.game.set_bot(BotThree())
            case Bots.BOT4:
                self.game.set_bot(BotFour())
        return self

    def add_ship(self, D: int, q: int):
        self.game.set_ship(Ship(D, q))
        return self

    def build(self):
        return self.game
