from enum import Enum
from typing import List


class Cell(Enum):
    CLOSED = 0
    OPEN = 1
    FIRE = 2
    BTN = 3
    BOT = 4

    def __str__(self):
        return '%s' % self.value


class GameResult():
    def __init__(self, outcome: bool, ship_dimensions: List[int], q: int, run_time_ms: int):
        self.outcome = outcome
        self.ship_dimensions = ship_dimensions
        self.q = q
        self.run_time_ms = run_time_ms

    def __str__(self):
        return f"\nOutcome: {'Success' if self.outcome else 'Failure'}\
                \nShip Dimensions: {self.ship_dimensions}\
                \nFire Spread Probability: {self.q}\
                \nRun Time {self.run_time_ms}ms\n"


class Bots(Enum):
    BOT1 = 1
    BOT2 = 2
    BOT3 = 3
    BOT4 = 4

    def __str__(self):
        return f"Bot {self.value}"


SHIP_LAYOUT_OUTPUT = "output/ship_layout.csv"
