from abc import ABC, abstractmethod
from typing import List
from config import Cell


class Bot(ABC):
    """Abstract base class for bots"""

    def __init__(self):
        self.ship_layout = None
        self.location = None
        self.visited = set()

    def set_ship_layout(self, ship_layout: List[List[Cell]]) -> None:
        self.ship_layout = ship_layout

    def reached_button(self) -> bool:
        """Returns True if the bot is on the button cell"""

        r, c = self.location
        return self.ship_layout[r][c] == Cell.BTN

    def is_on_fire(self) -> bool:
        """Returns True if the bot is on a burning cell"""

        r, c = self.location
        return self.ship_layout[r][c] == Cell.FIRE

    @abstractmethod
    def setup(self) -> None:
        """Performs any initial setup which the bot needs to do"""

        pass

    @abstractmethod
    def move(self) -> List[int]:
        """Moves the bot to another cell in the ship and returns new position"""

        pass
