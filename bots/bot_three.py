import utils
from .bot import Bot
from typing import List
from config import Cell
from heapq import heappop, heappush


class BotThree(Bot):
    """
    At every time step, the bot re-plans the shortest path to the button, avoiding the current fire cells and any cells adjacent to current fire cells, 
    if possible, then executes the next step in that plan. If there is no such path, it plans the shortest path based only on current fire cells, 
    then executes the next step in that plan
    """

    def __init__(self) -> None:
        super().__init__()

    def move(self) -> List[int]:
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
        else:
            r, c = self.shortest_path.pop()
            self.location = (r, c)
            self.traversed.append((r, c))

        return (r, c)

    def setup(self) -> None:
        self.shortest_path = self.get_shortest_path()
        if self.shortest_path == [-1, -1]:
            self.path_not_found = True
        else:
            print(f"[INFO]: Shortest path -> {self.shortest_path[::-1]}")

    def get_shortest_path(self, avoid_adjacent_fire_cells: bool = True) -> List[int]:
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

                if avoid_adjacent_fire_cells:
                    for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                        row_2, col_2 = row + dr, col + dc
                        if (
                            row_2 in range(len(self.ship_layout))
                            and col_2 in range(len(self.ship_layout))
                            and self.ship_layout[row_2][col_2] == Cell.FIRE
                        ):
                            continue

                        heappush(
                            minHeap, [self.heuristic([row, col]), (row, col)])
                        self.parent[(row, col)] = (r, c)
                        visited.add((row, col))
                else:
                    heappush(minHeap, [self.heuristic([row, col]), (row, col)])
                    self.parent[(row, col)] = (r, c)
                    visited.add((row, col))

        if not shortest_path:
            if avoid_adjacent_fire_cells:
                print(
                    "[INFO]: No path to button avoiding adjacent fire cells. Attempting with adjancent fire cells...")
                return self.get_shortest_path(False)
            else:
                return [-1, -1]

        while shortest_path[-1] != self.location:
            r, c = self.parent[shortest_path[-1]]
            shortest_path.append((r, c))

        return shortest_path

    def is_path_on_fire(self) -> bool:
        """Returns True if the current path is blocked by fire, False otherwise"""

        remaining_path = self.shortest_path[len(self.traversed) - 1:]
        for r, c in remaining_path:
            if self.ship_layout[r][c] == Cell.FIRE:
                print(
                    f"[INFO]: Cell ({r}, {c}) on current shortest path is in on fire!")
                return True
        return False
