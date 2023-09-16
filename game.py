from ship import Ship
from bot import Bot
from config import SHIP_LAYOUT_OUTPUT


class Game:
    def __init__(self, ship: Ship, bot: Bot):
        self.ship = ship
        self.bot = bot

    def play(self, time: int, q: int) -> bool:
        for i in range(time):
            self.ship.spread_fire(q)
        self.ship.print_ship(SHIP_LAYOUT_OUTPUT)
        return True
