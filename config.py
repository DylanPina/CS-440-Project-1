from enum import Enum


class Cell(Enum):
    CLOSED = 0
    OPEN = 1
    FIRE = 2
    BTN = 3
    BOT = 4
    TEST = 9

    def __str__(self):
        return '%s' % self.value


SHIP_LAYOUT_OUTPUT = "output/ship_layout.csv"
