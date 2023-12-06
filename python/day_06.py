import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
from math import prod, sqrt
import re
from collections import Counter

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """Time:      7  15   30
Distance:  9  40  200""".split(
    "\n"
)


def parse_input(input):
    return [
        list(map(int, filter(lambda x: x != "", part.split(":")[1].strip().split(" "))))
        for part in input
    ]


def calculate_distance(total_time, time_pushing):
    distance = (total_time - time_pushing) * time_pushing
    return distance


def get_all_distances(total_time):
    counter = Counter()
    for i in range(total_time + 1):
        counter[calculate_distance(total_time, i)] += 1
    return counter


def get_options_greater_than_current(counter, current_record):
    total = 0
    for k, v in counter.items():
        if k > current_record:
            total += v
    return total


def get_parabola(time):
    # distance = (total_time - time_pushing) * time_pushing
    # distance = (time * x - x*x)
    # distance = -x*x + time*x
    coeficients = (-1, time)
    return coeficients


def parabola_intersects_line(parabola, line):
    a = parabola[0]
    b = parabola[1]
    c = -line

    d = b**2 - 4 * a * c
    x1 = x2 = None
    if d < 0:
        pass  # No solution, x1,x2 remain None
    elif d == 0:
        x1 = (-b + sqrt(d)) / 2 * a
    else:
        x1 = (-b + sqrt(d)) / (2 * a)
        x2 = (-b - sqrt(d)) / (2 * a)
    return list(map(int, [x1, x2]))


def part_2(time, distance):
    intersects = parabola_intersects_line(get_parabola(time), distance)
    solution = time - (time - max(intersects) + min(intersects))
    return solution


input_day = get_input("2023__6")
time, distance = parse_input(input_day)

# part_1
options = [
    get_options_greater_than_current(get_all_distances(time[i]), distance[i])
    for i in range(len(time))
]
print("part_1")
print(prod(options))

# part_2
time = int("".join(map(str, time)))
distance = int("".join(map(str, distance)))
print("part_2")

print(part_2(time, distance))
assert calculate_distance(7, 0) == 0
assert calculate_distance(7, 7) == 0
assert calculate_distance(7, 4) == 12
assert get_options_greater_than_current(get_all_distances(7), 9) == 4
assert get_options_greater_than_current(get_all_distances(15), 40) == 8
assert get_options_greater_than_current(get_all_distances(30), 200) == 9

assert part_2(71530, 940200) == 71503
