from ship import Ship
from bots import BotOne
from game import Game


if __name__ == "__main__":
    ship = Ship(5)
    bot = BotOne()
    ship.add_bot(bot)
    game = Game(ship, bot)
    game.play(10000, 0.25)
