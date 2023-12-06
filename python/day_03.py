import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
from math import prod

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split(
    "\n"
)

GRID = {}
NUMBERS = {}
SYMBOLS = {}


def solver(input):
    # part 1
    create_grids(input)
    adjacent_coords = []
    for k, v in SYMBOLS.items():
        adjacent_coords.extend(v["adjacent"])
    valid_numbers_names = list(
        set(
            [
                GRID.get(coords)
                for coords in adjacent_coords
                if GRID.get(coords) is not None
            ]
        )
    )
    total = sum(
        [
            NUMBERS.get(number_name, {}).get("value", 0)
            for number_name in valid_numbers_names
        ]
    )
    print(total)

    # part 2
    total_2 = 0
    asterisk = [sym for k, sym in SYMBOLS.items() if sym["value"] == "*"]
    for item in asterisk:
        valid_numbers_names = list(
            set(
                [
                    GRID.get(coords)
                    for coords in item["adjacent"]
                    if GRID.get(coords) is not None
                ]
            )
        )
        if len(valid_numbers_names) == 2:
            total_2 += prod(
                [
                    NUMBERS.get(number_name, {}).get("value")
                    for number_name in valid_numbers_names
                ]
            )

    print(total_2)
    return total


def add_item_to_group(item, group):
    if group == "numbers":
        add_number(item)
    elif group == "symbols":
        add_symbol(item)
    else:
        raise Exception(
            f"**\n\t\t{group} is not implemented as a valid group to add items to"
        )


def add_symbol(symbol_item):
    adjacent = []
    for ki in range(-1, 2):
        for kj in range(-1, 2):
            adjacent.append((ki + symbol_item[0][0], kj + symbol_item[0][1]))
    SYMBOLS[symbol_item[0]] = {
        "coord": symbol_item[0],
        "value": symbol_item[1],
        "adjacent": adjacent[:],
    }


def add_number(number_item):
    NUMBERS[number_item[0]] = {
        "start": number_item[1],
        "end": number_item[2],
        "value": int(number_item[3]),
        "coords": number_item[4],
    }
    for coord in number_item[4]:
        GRID[coord] = number_item[0]


def create_grids(input):
    for r in range(0, len(input)):
        number_of_numbers = 0
        is_current_number = False
        current_number_name = current_number_start = current_number_end = None
        current_number_value = ""
        current_number_coords = []
        for c in range(0, len(input[r])):
            # check all elements, if it's a digit: either continue the previous number
            # or start a new one. If it's not a digit:
            # finish the previous number if it was open, add the symbol if there's one.
            element = input[r][c]
            if element.isdigit():
                if not is_current_number:
                    is_current_number = True
                    current_number_start = (r, c)
                    current_number_name = f"{str(r)}-{number_of_numbers}"
                    number_of_numbers += 1
                current_number_value += element
                current_number_coords.append((r, c))
                if c == len(input[r]) - 1:
                    add_item_to_group(
                        item=(
                            current_number_name,
                            current_number_start,
                            len(input[r]) - 1,
                            current_number_value,
                            current_number_coords,
                        ),
                        group="numbers",
                    )
            else:
                if is_current_number:
                    is_current_number = False
                    current_number_end = (r, c - 1)
                    add_item_to_group(
                        item=(
                            current_number_name,
                            current_number_start,
                            current_number_end,
                            current_number_value,
                            current_number_coords,
                        ),
                        group="numbers",
                    )
                    # reset
                    current_number_name = (
                        current_number_start
                    ) = current_number_end = None
                    current_number_value = ""
                    current_number_coords = []

                if element != ".":
                    symbol_value = element
                    coord = (r, c)
                    add_item_to_group(item=(coord, symbol_value), group="symbols")


input_day = get_input("2023__3")
solver(input_day)
