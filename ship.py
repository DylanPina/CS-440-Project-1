from typing import List
from random import randint
from config import Cell
import random


class Ship:
    def __init__(self, D: int) -> None:
        self.D = D
        self.blocked_cells = set()
        self.open_cells = set()
        self.burning_cells = set()
        self.ship = self.create_ship()
        self.open_random_blocked_cells_with_one_open_neighbor()
        self.open_random_dead_end_cells()
        self.spread_fire(0.8)
        self.spread_fire(0.8)

    def create_ship(self) -> List[List[int]]:
        # Generate D x D board initialized with 0
        ship = [[Cell.CLOSED] * self.D for i in range(self.D)]
        self.blocked_cells = [(r, c) for r in range(self.D) for c in range(self.D)]

        # Choose a square in the interior to 'open' at random, or we use the seed if it was given
        random_r, random_c = randint(0, self.D - 1), randint(0, self.D - 1)
        ship[random_r][random_c] = Cell.OPEN
        self.blocked_cells.remove((random_r, random_c))
        self.open_cells.add((random_r, random_c))

        return ship

    def get_blocked_cells_with_single_neighbor(self) -> List[List[int]]:
        blocked_cells_with_single_neighbor = []
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for r, c in self.blocked_cells:
            open_neighbors = 0

            for dr, dc in directions:
                row, col = r + dr, c + dc
                if (
                    row in range(self.D)
                    and col in range(self.D)
                    and self.ship[row][col] == Cell.OPEN
                ):
                    open_neighbors += 1

            if open_neighbors == 1:
                blocked_cells_with_single_neighbor.append((r, c))

        return blocked_cells_with_single_neighbor

    def open_random_blocked_cells_with_one_open_neighbor(self) -> None:
        blocked_cells_with_single_neighbor = (
            self.get_blocked_cells_with_single_neighbor()
        )

        while blocked_cells_with_single_neighbor:
            # Pick a random blocked cell with a single neighbor
            r, c = blocked_cells_with_single_neighbor[
                randint(0, len(blocked_cells_with_single_neighbor) - 1)
            ]
            # Open that cell
            self.ship[r][c] = Cell.OPEN
            self.blocked_cells.remove((r, c))
            self.open_cells.add((r, c))
            # Get the new blocked cells with single neighbors
            blocked_cells_with_single_neighbor = (
                self.get_blocked_cells_with_single_neighbor()
            )

    def get_dead_end_cells(self) -> List[List[int]]:
        dead_end_cells = []
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for r, c in self.open_cells:
            open_neighbors = 0

            for dr, dc in directions:
                row, col = r + dr, c + dc
                if (
                    row in range(self.D)
                    and col in range(self.D)
                    and self.ship[row][col] == Cell.OPEN
                ):
                    open_neighbors += 1

            if open_neighbors == 1:
                dead_end_cells.append((r, c))
        return dead_end_cells

    def open_random_dead_end_cells(self) -> None:
        dead_end_cells = self.get_dead_end_cells()
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for _ in range(0, len(dead_end_cells), 2):
            # Pick a random dead end cell
            r, c = dead_end_cells[randint(0, len(dead_end_cells) - 1)]
            # Choose a random direction
            random_dir = directions[randint(0, len(directions) - 1)]
            while True:
                random_r, random_c = random_dir
                # Check to see if this direction is a closed cell
                row, col = r + random_r, c + random_c
                if (
                    row in range(self.D)
                    and col in range(self.D)
                    and self.ship[row][col] == Cell.CLOSED
                ):
                    # First time we find a closed cell neighbor we will open it and break
                    self.ship[row][col] = Cell.OPEN
                    self.blocked_cells.remove((row, col))
                    self.open_cells.add((row, col))
                    break
                else:
                    random_dir = directions[randint(0, len(directions) - 1)]
            # Get the new dead end cells
            dead_end_cells = self.get_dead_end_cells()

    def spread_fire(self, q: int) -> None:
        # Check to see if this is the first flame
        if not self.burning_cells:
            # Choose a random open cell to start the fire
            r, c = random.choice(list(self.open_cells))
            self.set_cell_on_fire(r, c)
            return

        # Fire (potientially) spreads in every neighboring open cell
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for r, c in self.burning_cells.copy():
            for dr, dc in directions:
                row, col = r + dr, c + dc
                if (
                    row in range(self.D)
                    and col in range(self.D)
                    and self.ship[row][col] == Cell.OPEN
                ):
                    cell_catches_fire = random.choices(
                        [True, False], weights=(q, 1 - q), k=1
                    )[0]
                    if cell_catches_fire:
                        self.set_cell_on_fire(row, col)

    def set_cell_on_fire(self, r: int, c: int) -> None:
        if r in range(self.D) and c in range(self.D) and self.ship[r][c] == Cell.OPEN:
            self.ship[r][c] = Cell.FIRE
            self.open_cells.remove((r, c))
            self.burning_cells.add((r, c))
        else:
            print(f"[ERROR]: Cannot set cell ({r}, {c}) on fire...")
            exit(1)

    def print_layout(self) -> List[List[int]]:
        layout = ""
        for r in range(self.D):
            for c in range(self.D):
                layout += f"{self.ship[r][c].value}, "

            layout = layout.rsplit(", ", 1)[0]
            if r != self.D - 1:
                layout += "\n"

        print(layout)
