from ship import Ship
from config import SHIP_LAYOUT_OUTPUT, GameResult
from bots import Bot
import utils
import time


class Game:
    def __init__(self):
        self.ship = None
        self.bot = None

    def set_ship(self, ship: Ship) -> None:
        self.ship = ship

    def set_bot(self, bot: Bot) -> None:
        self.bot = bot

    def play(self, output_traversal: bool = False) -> GameResult:
        if not self.ship:
            print("[ERROR]: Cannot play game without ship!")
            exit(1)
        if not self.bot:
            print("[ERROR]: Cannot play game without bot!")
            exit(1)

        self.ship.start_fire()
        self.ship.add_bot(self.bot)

        if output_traversal:
            open(SHIP_LAYOUT_OUTPUT, "w").close()
            utils.print_layout(self.ship.layout, title="--Initial State--")

        start = time.time()
        outcome = True
        while True:
            self.ship.spread_fire()
            self.bot.move()

            if self.bot.reached_button():
                print("[SUCCESS]: Bot has reached button!")
                outcome = True
                break
            if self.bot.is_on_fire():
                print("[FAILURE]: Bot is on fire!")
                outcome = False
                break
            if self.bot.path_not_found:
                print("[FAILURE]: No path to button")
                outcome = False
                break

        if output_traversal:
            utils.print_layout(self.ship.layout, title="--Final State--")
            utils.print_layout(self.bot.get_traversal(
            ), bot_start_location=self.bot.starting_location, title="--Traversal--")

        return GameResult(
            outcome=outcome,
            bot_variant=self.bot.variant,
            ship_dimensions=self.ship.D,
            q=self.ship.q,
            run_time_ms=(time.time() - start) * 1000
        )
