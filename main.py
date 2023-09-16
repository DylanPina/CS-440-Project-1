from ship import Ship
from bots import BotOne
from game import Game


if __name__ == "__main__":
    bot = BotOne()
    ship = Ship(50, bot)
    game = Game(ship)
    game.play(100, 0.25)
