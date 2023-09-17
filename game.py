from ship import Ship
from config import SHIP_LAYOUT_OUTPUT
from bots import Bot
import utils


class Game:
    def __init__(self, ship: Ship, bot: Bot):
        self.ship = ship
        self.bot = bot
        self.ship.start_fire()
        self.ship.add_bot(bot)

    def play(self, time: int, q: int) -> bool:
        open(SHIP_LAYOUT_OUTPUT, "w").close()

        for _ in range(time):
            self.ship.spread_fire(q)
            self.bot.move()

            if self.bot.reached_button():
                print("[SUCCESS]: Bot has reached button!")
                break
            if self.bot.is_on_fire():
                print("[FAILURE]: Bot is on fire!")
                break

        # Printing out the final state of the board
        utils.print_layout(self.ship.layout, title="--Final State--")
        utils.print_layout(self.bot.get_traversal(), title="--Traversal--")
