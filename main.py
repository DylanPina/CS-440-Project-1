from ship import Ship
from bots import BotOne, BotTwo, BotThree
from game import Game


if __name__ == "__main__":
    ship = Ship(20)
    bot = BotTwo()
    game = Game(ship, bot)
    game.play(10000, 0.5)
