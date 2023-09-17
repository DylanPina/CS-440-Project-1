from ship import Ship
from config import SHIP_LAYOUT_OUTPUT
from bots import Bot


class Game:
    def __init__(self, ship: Ship, bot: Bot):
        self.ship = ship
        self.bot = bot

    def play(self, time: int, q: int) -> bool:
        for _ in range(time):
            self.ship.spread_fire(q)
            self.ship.move_bot(self.bot)

            if self.bot.reached_button():
                print("[SUCCESS]: Bot has reached button!")
                break
            if self.bot.is_on_fire():
                print("[FAILURE]: Bot is on fire!")
                break

        # Printing out the final state of the board
        self.ship.print_layout(SHIP_LAYOUT_OUTPUT)
