from .bot import Bot
from typing import List
from config import Cell
from heapq import heappop, heappush


class BotFour(Bot):
    """
    At every time step, the bot re-plans the shortest path to the button, avoiding the current fire cells, 
    and then executes the next step in that plan.
    """

    def __init__(self) -> None:
        super().__init__()

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
        br, bc = self.btn_location
        forward_shortest_path, backwards_shortest_path, shortest_path = [], [], []
        forward_parent = {(lr, lc): (lr, lc)}
        backwards_parent = {(br, bc): (br, bc)}
        forward_heap = [[self.heuristic([lr, lc]), (self.location)]]
        backwards_heap = [
            [self.heuristic([br, bc], [lr, lc]), (self.btn_location)]]
        forward_visited, backwards_visited = set(), set()

        while forward_heap and backwards_heap:
            # Explore forward
            _, (r, c) = heappop(forward_heap)
            # Check for intersection between forward and backward explorations
            if (r, c) in backwards_visited:
                forward_shortest_path.append((r, c))
                backwards_shortest_path.append((r, c))
                break
            forward_visited.add((r, c))
            # Explore forward frontier
            for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                row, col = r + dr, c + dc
                if (
                    row not in range(len(self.ship_layout))
                    or col not in range(len(self.ship_layout))
                    or (row, col) in forward_visited
                    or self.ship_layout[row][col] == Cell.FIRE
                    or self.ship_layout[row][col] == Cell.CLOSED
                ):
                    continue

                heappush(forward_heap, [
                         self.heuristic([row, col]), (row, col)])
                forward_parent[(row, col)] = (r, c)

            # Explore backwards
            _, (r, c) = heappop(backwards_heap)
            # Check for intersection between forward and backward explorations
            if (r, c) in forward_visited:
                backwards_shortest_path.append((r, c))
                forward_shortest_path.append((r, c))
                break
            backwards_visited.add((r, c))
            # Explore backwards frontier
            for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                row, col = r + dr, c + dc
                if (
                    row not in range(len(self.ship_layout))
                    or col not in range(len(self.ship_layout))
                    or (row, col) in backwards_visited
                    or self.ship_layout[row][col] == Cell.FIRE
                    or self.ship_layout[row][col] == Cell.CLOSED
                ):
                    continue

                heappush(backwards_heap, [
                         self.heuristic([row, col], self.location), (row, col)])
                backwards_parent[(row, col)] = (r, c)

        if not forward_shortest_path and not backwards_shortest_path:
            return [-1, -1]

        while forward_shortest_path and forward_shortest_path[-1] != self.location:
            r, c = forward_parent[forward_shortest_path[-1]]
            forward_shortest_path.append((r, c))

        while backwards_shortest_path and backwards_shortest_path[-1] != self.btn_location:
            r, c = backwards_parent[backwards_shortest_path[-1]]
            backwards_shortest_path.append((r, c))

        # Combine the two shortest paths
        forward_shortest_path.reverse()
        backwards_shortest_path = backwards_shortest_path[1::]
        shortest_path = forward_shortest_path[1::] + backwards_shortest_path[1::]
        
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
