import utils
from .bot import Bot
from typing import List
from config import Cell
from collections import deque


class BotTwo(Bot):
    """
    At every time step, the bot re-plans the shortest path to the button, avoiding the current fire cells, 
    and then executes the next step in that plan.
    """

    def __init__(self) -> None:
        super().__init__()
        self.parent = {}

    def move(self) -> None:
        if self.is_path_on_fire():
            print("[INFO]: Recalculating shortest path")
            new_shortest_path = self.get_shortest_path()
            if new_shortest_path == [-1, -1]:
                print("[FAILURE]: No path to button")
                utils.print_layout(self.ship_layout, title="--Final State--")
                utils.print_layout(self.get_traversal(), title="--Traversal--")
                exit(1)
            elif new_shortest_path != self.shortest_path:
                print(
                    f"[INFO]: New shortest path found -> {new_shortest_path}")
                self.shortest_path = new_shortest_path
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

        shortest_path = []
        visited = set(self.location)
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
                self.parent[(row, col)] = (r, c)
                visited.add((row, col))
                # print(f"({row}, {col}): {self.ship_layout[row][col]}")

        if not shortest_path:
            return [-1, -1]

        while shortest_path[-1] != self.location:
            r, c = self.parent[shortest_path[-1]]
            shortest_path.append((r, c))

        return shortest_path

    def is_path_on_fire(self) -> bool:
        remaining_path = self.shortest_path[len(self.traversed) - 1:]
        for r, c in remaining_path:
            if self.ship_layout[r][c] == Cell.FIRE:
                print(
                    f"[INFO]: Cell ({r}, {c}) on current shortest path is in on fire!")
                return True
        return False
