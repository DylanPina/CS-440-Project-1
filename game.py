from ship import Ship
from config import SHIP_LAYOUT_OUTPUT


class Game:
    def __init__(self, ship: Ship):
        self.ship = ship

    def play(self, time: int, q: int) -> bool:
        for i in range(time):
            self.ship.spread_fire(q)
            self.ship.move_bot()

        self.ship.print_layout(SHIP_LAYOUT_OUTPUT)
        return True
