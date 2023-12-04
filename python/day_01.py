import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
import re

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)


def solver(input):
    pattern = "|".join(maps.keys())

    total = 0
    for line in input:
        # there are _overlapping_ patterns
        matches = re.findall(f"(?=({pattern}))", line)
        try:
            total += int(f"{maps[matches[0]]}{maps[matches[-1]]}")
        except:
            print(line)
    return total


def solve_part_01(mode):
    if mode == "test":
        input = """
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet""".split(
            "\n"
        )
    elif mode == "solve":
        input = input_day_1
    output = solver(input=input)
    print(output)


def solve_part_02(mode):
    if mode == "test":
        input = """
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen""".split(
            "\n"
        )
    elif mode == "solve":
        input = input_day_1
    output = solver(input=input)
    # print(output)
    return output


maps = {str(i): str(i) for i in range(1, 10)}
input_day_1 = get_input("day_01")
solve_part_01("test")
solve_part_01("solve")
# update the map used for pattern finding and outcome
maps = {
    **maps,
    **{
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    },
}
print(f"Part 2 test:\t {solve_part_02('test')}")
print(f"Part 2 solve:\t {solve_part_02('solve')}")
