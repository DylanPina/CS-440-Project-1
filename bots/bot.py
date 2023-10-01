from abc import ABC, abstractmethod
from typing import List
from config import Cell


class Bot(ABC):
    """Abstract base class for bots"""

    def __init__(self):
        self.ship_layout = None
        self.starting_location = None
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
        br, bc = btn_location
        self.btn_location = (br, bc)

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
        for (r, c) in self.traversed[:-1]:
            matrix[r][c] = Cell.OPEN
        r, c = self.traversed[-1]
        matrix[r][c] = self.ship_layout[r][c]
        print((r, c), matrix[r][c])
        return matrix

    def heuristic(self, source: List[int], destination: List[int] = None):
        """Returns the Manhattan distance from current location to the button"""

        sr, sc = source
        dr, dc = destination if destination else self.btn_location
        return abs(sr - sc) + abs(dr - dc)

    @abstractmethod
    def setup(self) -> None:
        """Performs any initial setup which the bot needs to do"""

        pass

    @abstractmethod
    def move(self) -> List[int]:
        """Moves the bot to another cell in the ship and returns new position"""

        pass
