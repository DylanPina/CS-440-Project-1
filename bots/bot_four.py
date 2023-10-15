from .bot import Bot
from typing import List
from config import Cell, Bots
from collections import deque
from heapq import heappush, heappop


class BotFour(Bot):
    """
    The bot plans the shortest path to the button using the safest path away from the fire, avoiding the simulated probabilities captured, during
    the fire simulation run and then executes the next step in that plan.
    If fire spreads on the upcoming path during a traversal, the bot will re-attempt to find another shortest path.
    """

    def __init__(self, q: int = None) -> None:
        super().__init__(q)
        self.variant = Bots.BOT4

    def move(self) -> None:
        if self.is_on_fire() or self.path_not_found:
            return self.location

        if self.is_path_on_fire():
            print("[INFO]: Recalculating shortest path")
            new_shortest_path = self.get_path()
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
        self.shortest_path = self.get_path()
        if self.shortest_path == [-1, -1]:
            self.path_not_found = True
        else:
            print(f"[INFO]: Shortest path -> {self.shortest_path}")

    def get_path(self) -> List[int]:
        lr, lc = self.location
        fire_spread_prediction = self.simulate_fire(len(self.ship_layout) * 2)
        shortest_path = []
        visited = set()
        minHeap = [(self.get_safety_rating(
            lr, lc, 0, fire_spread_prediction), self.location, 0)]

        while minHeap:
            _, (r, c), t = heappop(minHeap)
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

                heappush(minHeap, [self.get_safety_rating(
                    lr, lc, 0, fire_spread_prediction), (row, col), t + 1])
                self.parent[(row, col)] = (r, c)
                visited.add((row, col))

        if not shortest_path:
            return [-1, -1]

        while shortest_path[-1] != self.location:
            r, c = self.parent[shortest_path[-1]]
            shortest_path.append((r, c))
        shortest_path.reverse()

        return shortest_path[1:]

    def is_path_on_fire(self) -> bool:
        """Returns True if the current path is blocked by fire, False otherwise"""

        remaining_path = self.shortest_path[len(self.traversed) - 1:]
        for r, c in remaining_path:
            if self.ship_layout[r][c] == Cell.FIRE:
                print(
                    f"[INFO]: Cell ({r}, {c}) on current shortest path is in on fire!")
                return True
        return False

    def simulate_fire(self, max_t: int) -> dict:
        visited = set([self.fire_start_location])
        queue = deque(
            [(self.fire_start_location[0], self.fire_start_location[1], 0)])
        # (r, c) -> (probability, distance)
        fire_spread_prediction = {self.fire_start_location: (1, 0)}

        while queue:
            r, c, t = queue.popleft()
            if t == max_t:
                break

            for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                row, col = r + dr, c + dc
                if (
                    row in range(len(self.ship_layout))
                    and col in range(len(self.ship_layout))
                    and (row, col) not in visited
                    and self.ship_layout[row][col] != Cell.FIRE
                    and self.ship_layout[row][col] != Cell.CLOSED
                ):
                    queue.append((row, col, t + 1))
                    fire_spread_prediction[(row, col)] =\
                        (float(pow(self.q, t + 1)), t + 1)
                    visited.add((row, col))

        return fire_spread_prediction

    def get_safety_rating(self, r: int, c: int, t: int, fire_spread_prediction: dict) -> float:
        if (r, c) in fire_spread_prediction:
            pf, tf = fire_spread_prediction[(r, c)]
            if t >= tf:
                return pf
        return 0
