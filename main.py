from ship import Ship
from bot import Bot
from game import Game


if __name__ == "__main__":
    ship = Ship(50)
    bot = Bot
    game = Game(ship, bot)
    game.play(50, 0.25)
