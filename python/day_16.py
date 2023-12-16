import sys
import os
from operator import methodcaller
from copy import deepcopy
from collections import Counter

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input, print_grid

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

REFLECTION = {
    "N": {
        "|": [(0, -1, "N")],
        "-": [(-1, 0, "W"), (1, 0, "E")],
        "\\": [(-1, 0, "W")],
        "/": [(1, 0, "E")],
        ".": [(0, -1, "N")],
    },
    "E": {
        "|": [(0, -1, "N"), (0, 1, "S")],
        "-": [(1, 0, "E")],
        "\\": [(0, 1, "S")],
        "/": [(0, -1, "N")],
        ".": [(1, 0, "E")],
    },
    "S": {
        "|": [(0, 1, "S")],
        "-": [(-1, 0, "W"), (1, 0, "E")],
        "\\": [(1, 0, "E")],
        "/": [(-1, 0, "W")],
        ".": [(0, 1, "S")],
    },
    "W": {
        "|": [(0, -1, "N"), (0, 1, "S")],
        "-": [(-1, 0, "W")],
        "\\": [(0, -1, "N")],
        "/": [(0, 1, "S")],
        ".": [(-1, 0, "W")],
    },
}

sample_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def parse_input(input):
    temp = []
    ct = Counter()
    for i in input.split("\n"):
        ct[len(i)] += 1
    size = ct.most_common()[0][0]
    # print(size)
    input = input.replace("\n", "")
    while input:
        s = input[0:size]
        temp.append(list(s))
        input = input[size:]
        # print(input)
    # print_grid(temp)
    return temp


def make_grid_dict(grid):
    gdict = {}
    for i, row in enumerate(grid):
        # print(row)s
        for j, col in enumerate(row):
            gdict[(j, i)] = col
    return gdict


def solve_starting_path(starting_beam):
    visited = set()
    beams = [starting_beam]
    while beams:
        # steps += 1
        beam = beams.pop()
        current = grid.get((beam[0], beam[1]), None)
        if current is None:
            continue
        else:
            visited.add(beam)

        next_changes = REFLECTION[beam[2]][current]
        for next_change in next_changes:
            next_beam = (
                beam[0] + next_change[0],
                beam[1] + next_change[1],
                next_change[2],
            )
            if next_beam not in visited:
                beams.append(next_beam)

    energized = set([(x[0], x[1]) for x in visited])
    return len(energized)


input_day = "".join(get_input("2023__16", sep=""))
input_to_use = input_day

processed_input = parse_input(input_to_use)
grid = make_grid_dict(processed_input)

# part_1
print("part 1\t", solve_starting_path((0, 0, "E")))

# part_2

# create starting grids from edges pointing inwards
starting_beams = []
n_rows = len(processed_input)
n_cols = len(processed_input[0])
for i in range(n_rows + 1):
    for k in range(n_cols + 1):
        if i == 0:
            starting_beams.append((k, i, "S"))
        elif i == n_rows:
            starting_beams.append((k, i, "N"))
        if k == 0:
            starting_beams.append((k, i, "E"))
        elif k == n_cols:
            starting_beams.append((k, i, "W"))

max_energized = 0
for starting_beam in starting_beams:
    max_energized = max(max_energized, solve_starting_path(starting_beam))


print("part 2\t", max_energized)
