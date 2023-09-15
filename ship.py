from typing import List
from random import randint
from config import Cell


class Ship:
    def __init__(self, D: int) -> None:
        self.D = D
        self.blocked_cells = set()
        self.open_cells = set()
        self.ship = self.create_ship()
        print(self.get_blocked_cells_with_single_neighbor())

    def create_ship(self) -> List[List[int]]:
        # Generate D x D board initialized with 0
        ship = [[Cell.CLOSED] * self.D for i in range(self.D)]
        self.blocked_cells = [(r, c) for r in range(self.D) for c in range(self.D)]

        # Choose a square in the interior to 'open' at random
        random_r, random_c = randint(0, self.D - 1), randint(0, self.D - 1)
        ship[random_r][random_c] = Cell.OPEN
        print(random_r, random_c)
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
                    row in range(self.D) and col in range(self.D)
                    and self.ship[row][col] == Cell.OPEN
                ):
                    open_neighbors += 1
                    self.ship[r][c] = Cell.FIRE

            if open_neighbors == 1:
                blocked_cells_with_single_neighbor.append((r, c))

        return blocked_cells_with_single_neighbor

    def print_layout(self) -> List[List[int]]:
        layout = ""
        for r in range(self.D):
            for c in range(self.D):
                layout += f"{self.ship[r][c].value}, "

            layout = layout.rsplit(", ", 1)[0]
            if r != self.D - 1:
                layout += "\n"

        print(layout)
