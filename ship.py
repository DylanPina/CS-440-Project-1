import utils
from typing import List
from random import randint
from config import Cell
from bots import Bot
import random


class Ship:
    def __init__(self, D: int) -> None:
        self.D = D
        self.bot = None
        self.closed_cells = set()
        self.open_cells = set()
        self.burning_cells = set()
        self.layout = self.create_matrix()
        self.open_initial_cell()
        self.open_random_closed_cells_with_one_open_neighbor()
        self.open_random_dead_end_cells()
        self.btn_location = self.place_button()

    def create_matrix(self) -> List[List[int]]:
        """Creates an D x D matrix used for the layout of the ship"""

        # Generate D x D board initialized with 0
        layout = [[Cell.CLOSED] * self.D for _ in range(self.D)]
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

        for r, c in cells:
            open_neighbors = 0
            for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
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

    def start_fire(self) -> None:
        """Places the first fire cell on a random open cell"""

        r, c = random.choice(list(self.open_cells))
        self.set_cell_on_fire(r, c)
        print(f"[INFO]: Fire started at ({r}, {c})")

    def spread_fire(self, q: int) -> None:
        """Potientially spreads a fire onto neighboring open cells with a probability of 1 - (1 - q)^K"""

        # Fire (potientially) spreads in every neighboring open cell
        for r, c in self.burning_cells.copy():
            for dr, dc in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
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

    def add_bot(self, bot: Bot) -> None:
        """Injects a bot onto the ship and preforms bot setup"""

        self.bot = bot
        self.place_bot(bot)
        bot.set_ship_layout(self.layout)
        bot.set_btn_location(self.btn_location)
        bot.setup()

    def place_bot(self, bot: Bot) -> List[int]:
        """Places the bot on a random open cell and returns location of bot"""

        r, c = random.choice(list(self.open_cells))
        self.open_cells.remove((r, c))
        self.layout[r][c] = Cell.BOT
        bot.location = (r, c)
        print(f"[INFO]: Bot placed at ({r}, {c})")
