import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input

from typing import List
import itertools
from math import gcd
from functools import reduce

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".split(
    "\n"
)

sample_input_b = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split(
    "\n"
)

sample_input_c = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split(
    "\n"
)


NODES = {}


def parse_input(input):
    instructions = input[0]
    for node in input[2:]:
        NODES[node.split(" = ")[0]] = {
            "L": node.split(", ")[0].split("(")[1],
            "R": node.split(", ")[1].split(")")[0],
        }
    return instructions


def follow_instructions(instructions, current="AAA", target: List = ["ZZZ"]):
    instruction = itertools.cycle(instructions)
    count = 0
    while current not in target:
        count += 1
        current = NODES[current].get(next(instruction))
    return count


def follow_ghost_instructions(instructions, list_of_ghosts, list_of_targets):
    return [
        follow_instructions(instructions, current=ghost, target=list_of_targets)
        for ghost in list_of_ghosts
    ]


def lcm(a, b):
    # on python 3.8
    return (a * b) // gcd(a, b)


input_day = get_input("2023__8")
instructions = parse_input(input_day)
# part_1
total = follow_instructions(instructions=instructions)
print(total)

# part_2
list_of_ghosts = [ghost for ghost in NODES.keys() if ghost[-1] == "A"]
list_of_targets = [ghost for ghost in NODES.keys() if ghost[-1] == "Z"]
landings = follow_ghost_instructions(instructions, list_of_ghosts, list_of_targets)
# print(landings)
print(reduce(lcm, landings))
