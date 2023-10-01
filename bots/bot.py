from abc import ABC, abstractmethod
from typing import List
from config import Cell


class Bot(ABC):
    """Abstract base class for bots"""

    def __init__(self):
        self.ship_layout = None
        self.location = None
        self.btn_location = None
        self.visited = set()
        self.parent = {}
        self.shortest_path = []
        self.traversed = []
        self.path_not_found = False

    def set_ship_layout(self, ship_layout: List[List[Cell]]) -> None:
        self.ship_layout = ship_layout

    def set_btn_location(self, btn_location: List[int]) -> None:
        self.btn_location = btn_location

    def reached_button(self) -> bool:
        """Returns True if the bot is on the button cell"""

        r, c = self.location
        return self.ship_layout[r][c] == Cell.BTN

    def is_on_fire(self) -> bool:
        """Returns True if the bot is on a burning cell"""

        r, c = self.location
        if self.ship_layout[r][c] == Cell.FIRE:
            print("[FAILURE]: Fire has spread to bot's location!")
            return True
        return False

    def get_traversal(self) -> List[List[int]]:
        """Returns a matrix representing the traversal"""

        print(f"[INFO]: Traversal -> {self.traversed}")
        if not self.traversed:
            return []

        matrix = [[Cell.CLOSED] * len(self.ship_layout)
                  for _ in range(len(self.ship_layout))]
        for i, (r, c) in enumerate(self.traversed[:-1]):
            if i == 0:
                matrix[r][c] = Cell.BOT
            else:
                matrix[r][c] = Cell.OPEN
        r, c = self.traversed[-1]
        matrix[r][c] = self.ship_layout[r][c]
        return matrix

    def heuristic(self, location: List[int]):
        """Returns the Manhattan distance from current location to the button"""

        lr, lc = location
        br, bc = self.btn_location
        return abs(lr - br) + abs(lc - bc)

    @abstractmethod
    def setup(self) -> None:
        """Performs any initial setup which the bot needs to do"""

        pass

    @abstractmethod
    def move(self) -> List[int]:
        """Moves the bot to another cell in the ship and returns new position"""

        pass
