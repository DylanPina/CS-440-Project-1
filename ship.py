from typing import List
from random import randint
from config import Cell
from bots import Bot
import random


class Ship:
    def __init__(self, D: int, bot: Bot) -> None:
        self.D = D
        self.bot = bot
        self.closed_cells = set()
        self.open_cells = set()
        self.burning_cells = set()
        self.layout = self.create_matrix()
        self.open_initial_cell()
        self.open_random_closed_cells_with_one_open_neighbor()
        self.open_random_dead_end_cells()
        self.btn_location = self.place_button()
        self.place_bot()
        self.bot.set_ship_layout(self.layout)

    def create_matrix(self) -> List[List[int]]:
        """Creates an D x D matrix used for the layout of the ship"""

        # Generate D x D board initialized with 0
        layout = [[Cell.CLOSED] * self.D for i in range(self.D)]
        self.closed_cells = [(r, c) for r in range(self.D)
                             for c in range(self.D)]
        return layout

    def open_initial_cell(self) -> None:
        """Choose a square in the interior to 'open' at random, or we use the seed if it was given"""

        random_r, random_c = randint(0, self.D - 1), randint(0, self.D - 1)
        self.open_cell(random_r, random_c)

    def get_cells_with_one_open_neighbor(self, cells: set) -> List[int]:
        """Returns a list of all the cells from a set of given cells which only have one open neighbor"""

        output = []
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for r, c in cells:
            open_neighbors = 0
            for dr, dc in directions:
                row, col = r + dr, c + dc
                if (
                    row in range(self.D)
                    and col in range(self.D)
                    and self.layout[row][col] == Cell.OPEN
                ):
                    open_neighbors += 1

            if open_neighbors == 1:
                output.append((r, c))

        return output

    def open_random_closed_cells_with_one_open_neighbor(self) -> None:
        """
        Iteratively chooses a random blocked cell which has only one open neighbor
        and opens it
        """

        closed_cells_with_single_neighbor = self.get_cells_with_one_open_neighbor(
            self.closed_cells
        )

        while closed_cells_with_single_neighbor:
            # Pick a random blocked cell with a single neighbor
            r, c = closed_cells_with_single_neighbor[
                randint(0, len(closed_cells_with_single_neighbor) - 1)
            ]
            # Open that cell
            self.layout[r][c] = Cell.OPEN
            self.closed_cells.remove((r, c))
            self.open_cells.add((r, c))
            # Get the new blocked cells with single neighbors
            closed_cells_with_single_neighbor = self.get_cells_with_one_open_neighbor(
                self.closed_cells
            )

    def open_random_dead_end_cells(self) -> None:
        """Chooses half of the dead end cells at random and opens those chosen"""

        dead_end_cells = self.get_cells_with_one_open_neighbor(
            self.closed_cells)
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
                    and self.layout[row][col] == Cell.CLOSED
                ):
                    # First time we find a closed cell neighbor we will open it and break
                    self.layout[row][col] = Cell.OPEN
                    self.closed_cells.remove((row, col))
                    self.open_cells.add((row, col))
                    break
                else:
                    random_dir = directions[randint(0, len(directions) - 1)]
            # Get the new dead end cells
            dead_end_cells = self.get_cells_with_one_open_neighbor(
                self.closed_cells)

    def open_cell(self, r: int, c: int) -> None:
        """Sets layout[r][c] on fire if [r][c] are valid cells which can catch fire"""

        self.layout[r][c] = Cell.OPEN
        self.closed_cells.remove((r, c))
        self.open_cells.add((r, c))

    def spread_fire(self, q: int) -> None:
        """Potientially spreads a fire onto neighboring open cells with a probability of 1 - (1 - q)^K"""

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
                    and self.layout[row][col] == Cell.OPEN
                ):
                    cell_catches_fire = random.choices(
                        [True, False], weights=(q, 1 - q), k=1
                    )[0]
                    if cell_catches_fire:
                        self.set_cell_on_fire(row, col)

    def set_cell_on_fire(self, r: int, c: int) -> None:
        """Sets layout[r][c] on fire if [r][c] are valid cells which can catch fire"""

        if r in range(self.D) and c in range(self.D) and self.layout[r][c] == Cell.OPEN:
            self.layout[r][c] = Cell.FIRE
            self.open_cells.remove((r, c))
            self.burning_cells.add((r, c))
        else:
            print(f"[ERROR]: Cannot set cell ({r}, {c}) on fire...")
            exit(1)

    def place_button(self) -> List[int]:
        """Places the button on a random closed cell and returns the location of button"""

        r, c = random.choice(list(self.open_cells))
        self.open_cells.remove((r, c))
        self.layout[r][c] = Cell.BTN
        return [r, c]

    def place_bot(self) -> List[int]:
        """Places the bot on a random open cell and returns location of bot"""

        r, c = random.choice(list(self.open_cells))
        self.open_cells.remove((r, c))
        self.layout[r][c] = Cell.BOT
        self.bot.location = [r, c]
        print([r, c])

    def move_bot(self) -> None:
        """Moves bot to a different cell on the ship based on the bots implementation"""

        self.bot.move()

    def print_layout(self, file: str) -> None:
        """Prints out the current state of the layout to a specified file"""

        output_file = None
        try:
            output_file = open(file, "w")

            layout = ""
            for r in range(self.D):
                for c in range(self.D):
                    layout += f"{self.layout[r][c].value}, "

                layout = layout.rsplit(", ", 1)[0]
                if r != self.D - 1:
                    layout += "\n"

            output_file.write(layout)
            output_file.close()
        except IOError:
            print(f"[ERROR]: Unable to write to output file to '{file}'")
