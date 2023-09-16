from abc import ABC, abstractmethod
from typing import List
from config import Cell


class Bot(ABC):

    def __init__(self):
        self.ship_layout = None
        self.location = None
        self.visited = set()

    def set_ship_layout(self, ship_layout: List[List[Cell]]) -> None:
        self.ship_layout = ship_layout

    @abstractmethod
    def move(self) -> List[int]:
        """Moves the bot to another cell in the ship and returns new position"""

        pass
