from ship import Ship
from bots import BotOne, BotTwo, BotThree, BotFour
from game import Game
import time


if __name__ == "__main__":
    start = time.time()
    ship = Ship(20)
    bot = BotFour()
    game = Game(ship, bot)
    game.play(q=0.5)
    print(f"[INFO]: Execution time ({time.time() - start}ms)")
