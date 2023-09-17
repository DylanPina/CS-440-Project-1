from .bot import Bot
from typing import Tuple, List
from collections import deque
from config import Cell


class BotOne(Bot):
    """
    This bot plans the shortest path to the button, avoiding the initial fire cell, and then executes that plan. 
    The spread of the fire is ignored by the bot.
    """

    def __init__(self) -> None:
        super().__init__()

    def move(self) -> Tuple[int]:
        r, c = self.shortest_path.pop()
        self.location = (r, c)
        return (r, c)

    def setup(self) -> None:
        self.shortest_path = self.get_shortest_path()
        if self.shortest_path == [-1, -1]:
            print("[FAILURE]: Shortest path cannot be reached")
        else:
            print(f"[INFO]: Shortest path -> {self.shortest_path[::-1]}")

    def get_shortest_path(self) -> List[int]:
        """Returns the shortest path from the current location to the button"""

        shortest_path = []
        parent = {self.location: self.location}
        visited = set()
        queue = deque()
        queue.append(self.location)

        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        while queue:
            r, c = queue.pop()
            if self.ship_layout[r][c] == Cell.BTN:
                shortest_path.append((r, c))
                break

            for dr, dc in directions:
                row, col = r + dr, c + dc
                if (
                    row not in range(len(self.ship_layout))
                    or col not in range(len(self.ship_layout))
                    or (row, col) in visited
                    or self.ship_layout[row][col] == Cell.FIRE
                    or self.ship_layout[row][col] == Cell.CLOSED
                ):
                    continue

                queue.append((row, col))
                parent[(row, col)] = (r, c)
                visited.add((row, col))

        while shortest_path[-1] != self.location:
            r, c = parent[shortest_path[-1]]
            shortest_path.append((r, c))

        return shortest_path if shortest_path else [-1, -1]
