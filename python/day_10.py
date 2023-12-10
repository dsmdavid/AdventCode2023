import sys
import os
import numpy as np


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """.....
.S-7.
.|.|.
.L-J.
.....""".split(
    "\n"
)

sample_input_b = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".split(
    "\n"
)

sample_input_c = (
    """Y.........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
X.........""".replace(
        "O", "."
    )
    .replace("I", ".")
    .split("\n")
)


CONNECTIONS = {
    "|": ((0, 1), (0, -1)),
    "-": ((-1, 0), (1, 0)),
    "L": ((0, 1), (1, 0)),
    "J": ((0, 1), (-1, 0)),
    "7": ((-1, 0), (0, -1)),
    "F": ((1, 0), (0, -1)),
    ".": ((0, 0)),
}

REVERSE_CONNECTION = {v: k for k, v in CONNECTIONS.items()}

EXTENDER = {
    "|": (".", "|", ".", (1,)),
    "-": ("-", ".", ".", (0,)),
    "L": ("-", "|", ".", (0, 1)),
    "J": (".", "|", ".", (1,)),
    "7": (".", ".", ".", ()),
    "F": ("-", ".", ".", (0,)),
    ".": (".", ".", ".", ()),
}


COORDS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

GRID = {}
PATH = {}
SIZE = []

# Sets used to hold the trapped/not_trapped points inside the grid
trapped = set()
not_trapped = set()


def parse_input(input):
    # GRID looks like:
    #  -1,1   0,1  1,1
    #  -1,0   0,0  1,0
    #  -1,-1, 0,-1 1,-1
    SIZE.append((len(input[0]), len(input)))
    starting_s = None
    for row, line in enumerate(input[::-1]):
        for column, element in enumerate(line):
            if element == "S":
                starting_s = (column, row)
            elif element not in CONNECTIONS.keys():
                GRID[(column, row)] = (0, 0)
            else:
                GRID[(column, row)] = CONNECTIONS[element]
    return starting_s


def follow_path_single_input(position, step):
    options = GRID[position]
    next_positions = [
        (position[0] + delta[0], position[1] + delta[1]) for delta in options
    ]
    next_positions = list(filter(lambda x: x not in PATH.keys(), next_positions))
    if not next_positions:
        # no valid option
        # either we have finished or something went wrong
        return None

    next_position = next_positions.pop()
    PATH[next_position] = step
    # print('next_position: ', next_position)

    return next_position


def extend_grid(transforming_grid, path_item, step=0.5):
    """
    Transform the grid to allow not_trapped to escape the loop:
    Go from             to
    F-7                 ......
    |.|                 F---7.
    L-J                 |...|.
                        |...|.
                        |...|.
                        L---J.
    """
    grid = {}
    for k, v in transforming_grid.items():
        next_vals = (
            (k[0] + step, k[1]),
            (k[0], k[1] + step),
            (k[0] + step, k[1] + step),
            (k[0], k[1]),
        )
        if k not in path_item:
            extension = (".", ".", ".", ())
        else:
            extension = EXTENDER[REVERSE_CONNECTION[v]]
        for nv, ex in zip(next_vals, extension):
            grid[nv] = CONNECTIONS.get(ex, (0, 0))
        for n in extension[3]:
            path_item[next_vals[n]] = -1
        grid[k] = v
    return grid, path_item


def is_trapped(point, path_item, grid_item, step=1):
    # start from a given point. Grow through neihbours
    # until either we reached the outside of the grid (and we then scaped)
    # or until we can no longer grow without crossing the path of the pipes.
    new_coords = [(v[0] * step, v[1] * step) for v in COORDS.values()]
    if point in path_item or point in trapped:
        return True
    elif point in not_trapped:
        return False
    current = [point]
    last_round = current[:]
    iteration = 0
    while True:
        iteration += 1
        adjacent = list(
            set(
                list(
                    filter(
                        lambda x: x not in current,
                        list(
                            filter(
                                lambda x: x not in path_item,
                                [
                                    (p[0] + c[0], p[1] + c[1])
                                    for p in last_round
                                    for c in new_coords
                                ],
                            )
                        ),
                    )
                )
            )
        )
        if len(adjacent) == 0:
            trapped.update(current)
            return True
        for item in adjacent:
            if grid_item.get(item, "not_in_grid") == "not_in_grid":
                # we reached infinity! aka, we're out of the loop
                not_trapped.update(current)
                not_trapped.update(adjacent)
                return False
        last_round = adjacent[:]
        current.extend(adjacent)


def save_grid(filename, grid, path, trapped, not_trapped, step):
    """Only needed for plotting the results"""
    temp_grid = {}
    for k in grid.keys():
        if k in path:
            temp_grid[k] = 50
        elif k in trapped:
            temp_grid[k] = 100
        elif k in not_trapped:
            temp_grid[k] = 25
        else:
            temp_grid[k] = 0
    reshaped_grid = {
        (int(k[0] / step), int(k[1] / step)): v for k, v in temp_grid.items()
    }
    max_cols = max([pos[0] for pos in reshaped_grid.keys()]) + 1
    max_rows = max([pos[1] for pos in reshaped_grid.keys()]) + 1
    arr = np.zeros((max_rows, max_cols))
    for row in range(max_cols):
        for column in range(max_rows):
            arr[column][row] = reshaped_grid[(row, column)]

    with open(f"{filename}.npy", "wb") as f:
        np.save(f, arr)


input_day = get_input("2023__10")
input_to_use = input_day
starting_s = parse_input(input_day)
print("starting_s: ", starting_s)
PATH[starting_s] = 0
GRID[starting_s] = CONNECTIONS["F"]
GRID[starting_s] = CONNECTIONS["-"]
current = starting_s
count = 0
# part_1
print("part_1")
while current:
    count += 1
    current = follow_path_single_input(current, count)

print(int(len(PATH) / 2))
save_grid("assets/day_10/part_1", GRID, PATH, set(), set(), step=1)
original_grid = {k: v for k, v in GRID.items()}

new_grid = {(k[0] * 10, k[1] * 10): v for k, v in GRID.items()}
new_path = {(k[0] * 10, k[1] * 10): v for k, v in PATH.items()}
new_grid, new_path = extend_grid(new_grid, new_path, 5)
save_grid(
    filename="assets/day_10/extended",
    grid=new_grid,
    path=new_path,
    trapped=set(),
    not_trapped=set(),
    step=5,
)
print("part_2")
trap_test = []
for k in original_grid.keys():
    new_k = (k[0] * 10, k[1] * 10)
    if is_trapped(new_k, new_path, new_grid, step=5):
        trap_test.append(new_k)

print(len(trap_test) - len(PATH))


# from assets.utils import return_heatmap


# import seaborn as sns

# import matplotlib.pylab as plt
save_grid("assets/day_10/day_10_0001", new_grid, new_path, trapped, not_trapped, step=5)
new_trapped = [(k[0] / 10, k[1] / 10) for k in list(trapped)]
new_not_trapped = [(k[0] / 10, k[1] / 10) for k in list(not_trapped)]
save_grid(
    filename="assets/day_10/day_10_0000",
    grid=GRID,
    path=PATH,
    trapped=new_trapped,
    not_trapped=new_not_trapped,
    step=1,
)


# plot results

import seaborn as sns

import matplotlib.pylab as plt

filenames = [
    ("part_1.npy", "after_part_1"),
    ("extended.npy", "extend_grid"),
    ("day_10_0001.npy", "extended_assigned"),
    ("day_10_0000.npy", "original_grid_assigned"),
]

for i, item in enumerate(filenames):
    with open(f"assets/day_10/{item[0]}", "rb") as f:
        arr = np.load(f)
    ax = sns.heatmap(
        arr,
        linewidth=0,
        cmap="magma",
        vmin=0,
        vmax=100,
        xticklabels=False,
        yticklabels=False,
        cbar=False,
    )
    # ax._legend_remove()
    plt.savefig(
        f"assets/day_10/{str(i+1)}_{item[1]}.png",
        transparent=None,
        dpi="figure",
        format=None,
        metadata=None,
        bbox_inches=None,
        pad_inches=0.1,
        facecolor="auto",
        edgecolor="auto",
        backend=None,
    )
