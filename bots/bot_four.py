from .bot import Bot
from typing import List
from config import Cell, Bots
from collections import deque


class BotFour(Bot):
    """
    The bot plans the shortest path to the button using bi-directional A* search, avoiding the current fire cells, and then executes the next step in that plan.
    If fire spreads on the upcoming path during a traversal, the bot will re-attempt to find another shortest path.
    """

    def __init__(self) -> None:
        super().__init__()
        self.variant = Bots.BOT4

    def move(self) -> None:
        if self.is_on_fire() or self.path_not_found:
            return self.location

        if self.is_path_on_fire():
            print("[INFO]: Recalculating shortest path")
            new_shortest_path = self.get_shortest_path()
            if new_shortest_path == [-1, -1]:
                self.path_not_found = True
                return
            elif new_shortest_path != self.shortest_path:
                print(
                    f"[INFO]: New shortest path found -> {new_shortest_path}")
                self.shortest_path = new_shortest_path

        r, c = self.shortest_path.pop(0)
        self.location = (r, c)
        self.traversed.append((r, c))
        return (r, c)

    def setup(self) -> None:
        self.shortest_path = self.get_shortest_path()
        if self.shortest_path == [-1, -1]:
            self.path_not_found = True
        else:
            print(f"[INFO]: Shortest path -> {self.shortest_path}")

    def get_shortest_path(self) -> List[int]:
        """Returns the shortest path from the current location to the button"""

        lr, lc = self.location
        visited = set()
        queue = deque([(lr, lc)])
        paths = []

        while queue:
            r, c = queue.popleft()
            if self.ship_layout[r][c] == Cell.BTN:
                paths.append(self.construct_path((r, c)))
                continue

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
                queue.append((row, col))
                self.parent[(row, col)] = (r, c)
                visited.add((row, col))

        if not paths:
            return [-1, -1]

        print(f"All {len(paths)} paths: {paths}")
        return paths[0]

    def is_path_on_fire(self) -> bool:
        """Returns True if the current path is blocked by fire, False otherwise"""

        remaining_path = self.shortest_path[len(self.traversed) - 1:]
        for r, c in remaining_path:
            if self.ship_layout[r][c] == Cell.FIRE:
                print(
                    f"[INFO]: Cell ({r}, {c}) on current shortest path is in on fire!")
                return True
        return False

    def construct_path(self, cell: List[int]) -> List[int]:
        shortest_path = [cell]
        while shortest_path[-1] != self.location:
            r, c = self.parent[shortest_path[-1]]
            shortest_path.append((r, c))
        shortest_path.reverse()
        return shortest_path
