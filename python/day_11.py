import sys
import os
from collections import defaultdict
import itertools

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".split(
    "\n"
)


def parse_input(input):
    nodes = {}
    empty_rows = []
    empty_cols = []
    empty_cols_temp = defaultdict(list)

    for i, row in enumerate(input):
        if all(pos == "." for pos in row):
            # empty row
            empty_rows.append(i)
        for k, pos in enumerate(row):
            # create the columns
            empty_cols_temp[k].append(pos)
            if pos != ".":
                # galaxy found
                nodes[(i, k)] = {}

    for i, col in empty_cols_temp.items():
        if all(pos == "." for pos in col):
            # empty col
            empty_cols.append(i)

    return nodes, empty_rows, empty_cols


def get_distance(node1, node2, empty_rows=[], empty_cols=[], step=2) -> int:
    r_max = max(node1[0], node2[0])
    r_min = min(node1[0], node2[0])
    if r_max <= r_min:
        r = 0
    else:
        r = (r_max - r_min) + (
            (step - 1)
            * len(list(filter(lambda x: x < r_max and x > r_min, empty_rows)))
        )
    c_max = max(node1[1], node2[1])
    c_min = min(node1[1], node2[1])
    if c_max <= c_min:
        c = 0
    else:
        c = (c_max - c_min) + (
            (step - 1)
            * len(list(filter(lambda x: x < c_max and x > c_min, empty_cols)))
        )

    return r + c


input_day = get_input("2023__11")
input_to_use = input_day
nodes, empty_rows, empty_cols = parse_input(input_to_use)
node_list = sorted(nodes.keys())

total = 0
for i in range(len(node_list)):
    for k in range(i + 1, len(node_list)):
        total += get_distance(
            node_list[i], node_list[k], empty_rows=empty_rows, empty_cols=empty_cols
        )
print("part_1")
print(total)

total_ans = 0
for i in range(len(node_list)):
    for k in range(i + 1, len(node_list)):

        total_ans += get_distance(
            node_list[i],
            node_list[k],
            empty_rows=empty_rows,
            empty_cols=empty_cols,
            step=1000000,
        )
print("part_2")
print(total_ans)
