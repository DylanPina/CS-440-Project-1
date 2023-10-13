import csv
from config import Cell
from typing import List


class Seed:
    def __init__(self, file: str):
        self.layout = self.read_from_file(file)
        self.D = len(self.layout)
        self.closed_cells = set()
        self.open_cells = set()
        self.burning_cells = set()
        self.fire_start_location = None
        self.btn_location = None
        self.bot_location = None
        self.get_cells()

    def read_from_file(self, file: str) -> List[int]:
        layout = []
        reader = csv.reader(open(file))
        for row in reader:
            vals = [i.strip() for i in row]
            enums = []
            for val in vals:
                if val == str(Cell.CLOSED.value):
                    enums.append(Cell.CLOSED)
                elif val == str(Cell.OPEN.value):
                    enums.append(Cell.OPEN)
                elif val == str(Cell.FIRE.value):
                    enums.append(Cell.FIRE)
                elif val == str(Cell.BTN.value):
                    enums.append(Cell.BTN)
                elif val == str(Cell.BOT.value):
                    enums.append(Cell.BOT)
            layout.append(enums)
        return layout

    def get_cells(self) -> None:
        for r in range(self.D):
            for c in range(self.D):
                if self.layout[r][c] == Cell.CLOSED:
                    self.closed_cells.add((r, c))
                elif self.layout[r][c] == Cell.OPEN:
                    self.open_cells.add((r, c))
                elif self.layout[r][c] == Cell.FIRE:
                    self.fire_start_location = (r, c)
                    self.burning_cells.add((r, c))
                elif self.layout[r][c] == Cell.BTN:
                    self.btn_location = (r, c)
                elif self.layout[r][c] == Cell.BOT:
                    self.bot_location = (r, c)
