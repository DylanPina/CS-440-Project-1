from ship import Ship
from bot import Bot


class Game:
    def __init__(self, ship: Ship, bot: Bot):
        self.ship = ship
        self.bot = bot

    def play(self, time: int, q: int) -> bool:
        for i in range(time):
            self.ship.spread_fire(q)
        self.ship.print_ship("output/ship_layout.csv")
        return True
