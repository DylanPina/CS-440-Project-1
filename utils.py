from typing import List, Optional
from config import Cell, SHIP_LAYOUT_OUTPUT


def print_layout(layout: List[List[Cell]], file: Optional[str] = SHIP_LAYOUT_OUTPUT, title: Optional[str] = "") -> None:
    """Prints out the current state of the layout to a specified file"""

    if not layout:
        return

    output_file = None
    try:
        output_file = open(file, "a")

        # print num of column
        output = f"{title}\n" if title else ""
        count = 0
        for c in range(len(layout) + 1):
            if c == 0:
                output += "   "
                continue
            output += f"{count}  "
            count = (count + 1) % 10
        output += "\n"
        count = 0

        for r in range(len(layout)):
            # print num of row
            output += f"{count}  "
            count = (count + 1) % 10

            for c in range(len(layout)):
                output += f"{layout[r][c].value}, "

            output = output.rsplit(", ", 1)[0]
            if r != len(layout) - 1:
                output += "\n"

        output_file.write(f"{output}\n")
        output_file.close()
    except IOError:
        print(f"[ERROR]: Unable to write to output file to '{file}'")
