import sys
import os
from operator import methodcaller
from copy import deepcopy
from collections import defaultdict

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split(
    "\n\n"
)


def parse_input(input):
    # table = str.maketrans(".#", "01")
    # print(input)
    maps = list(map(methodcaller("split", "\n"), input))
    maps_tr = []
    for map_ in maps:
        new_map = list(map(list, map_))
        maps_tr.append(new_map)

    return maps_tr


def is_possible_palindrome(value):
    # start from one side:
    hits = []
    for i in range(len(value)):
        a, b = value[0:i], value[i:]
        max_range = min(len(a), len(b))
        a, b = a[-max_range:], b[0:max_range:]
        if a and a == b[::-1]:
            hits.append(i)
    return hits


def convert_map(maps):
    convert_maps = []
    # print(len(maps), len(maps[0][0]))
    for mn, map_ in enumerate(maps):
        number_of_columns = len(map_[0])
        temp_map = [[] for i in range(number_of_columns)]
        for j, row in enumerate(map_):
            for i, element in enumerate(row):
                temp_map[i].append(element)
        convert_maps.append(temp_map)
    return convert_maps


def get_values(maps):
    res = list(map(is_possible_palindrome, maps))
    return res


def generate_combinations(map_item):
    combs = []
    for i in range(len(map_item)):
        for j in range(len(map_item[0])):
            temp = deepcopy(map_item)
            temp[i][j] = "#" if map_item[i][j] == "." else "."
            combs.append(temp[:])
    return combs


def check_map(map_item):
    v_r = get_values([map_item])
    v_c = get_values(convert_map([map_item]))
    tests = generate_combinations(map_item)
    vals_r = []
    for t in tests:
        vals_r.extend(is_possible_palindrome(t))
    convert_maps = convert_map(tests)
    vals_c = []
    for c in convert_maps:
        vals_c.extend(is_possible_palindrome(c))
    # condense
    vals_r = set(vals_r)
    vals_c = set(vals_c)
    t_r = []
    for row in v_r:
        t_r.extend(row)
    v_r = set(t_r)
    t_c = []
    for row in v_c:
        t_c.extend(row)
    v_c = set(t_c)

    return (vals_r.difference(v_r), vals_c.difference(v_c), v_r, v_c)


input_day = get_input("2023__13", sep="\n")
input_day = "\n".join(input_day)
input_day = input_day.split("\n\n")
input_to_use = input_day
maps_ = parse_input(input_to_use)

outputs_r1 = []
outputs_c1 = []
outputs_r2 = []
outputs_c2 = []

for map_ in maps_:
    r2, c2, r1, c1 = check_map(map_)
    outputs_r2.extend(list(r2))
    outputs_c2.extend(list(c2))
    outputs_r1.extend(list(r1))
    outputs_c1.extend(list(c1))


print("part 1: ", 100 * sum(outputs_r1) + sum(outputs_c1))
print("part 2: ", 100 * sum(outputs_r2) + sum(outputs_c2))
