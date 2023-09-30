from .bot import Bot
from typing import Tuple, List
from config import Cell
from heapq import heappush, heappop
import utils


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
        self.traversed.append((r, c))
        return (r, c)

    def setup(self) -> None:
        self.shortest_path = self.get_shortest_path()
        if self.shortest_path == [-1, -1]:
            print("[FAILURE]: No path to button")
            utils.print_layout(self.ship_layout, title="--Final State--")
            utils.print_layout(self.get_traversal(), title="--Traversal--")
            exit(1)
        else:
            print(f"[INFO]: Shortest path -> {self.shortest_path[::-1]}")

    def get_shortest_path(self) -> List[int]:
        """Returns the shortest path from the current location to the button"""

        lr, lc = self.location
        shortest_path = []
        visited = set()
        minHeap = [[self.heuristic([lr, lc]), (self.location)]]

        while minHeap:
            _, (r, c) = heappop(minHeap)
            if self.ship_layout[r][c] == Cell.BTN:
                shortest_path.append((r, c))
                break

            for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                row, col = r + dr, c + dc
                if (
                    row not in range(len(self.ship_layout))
                    or col not in range(len(self.ship_layout))
                    or (row, col) in visited
                    or self.ship_layout[row][col] == Cell.FIRE
                    or self.ship_layout[row][col] == Cell.CLOSED
                ):
                    continue

                heappush(minHeap, [self.heuristic([row, col]), (row, col)])
                self.parent[(row, col)] = (r, c)
                visited.add((row, col))

        if not shortest_path:
            return [-1, -1]

        while shortest_path[-1] != self.location:
            r, c = self.parent[shortest_path[-1]]
            shortest_path.append((r, c))

        return shortest_path if shortest_path else [-1, -1]

    def heuristic(self, location: List[int]):
        lr, lc = location
        br, bc = self.btn_location
        return abs(lr - br) + abs(lc - bc)
