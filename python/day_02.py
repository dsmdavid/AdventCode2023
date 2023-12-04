import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
import re

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split(
    "\n"
)

map_available = {"red": 12, "green": 13, "blue": 14}

pattern = re.compile(r"(\d+) (red|green|blue)")


def solver(input, pattern):
    total = 0
    total_2 = 0
    for line in input:
        colours = re.findall(pattern, line)
        factor = 1
        for col in ("red", "green", "blue"):
            factor *= max([int(x[0]) for x in filter(lambda x: x[1] == col, colours)])
        total_2 += factor
        invalid = list(filter(lambda x: int(x[0]) > map_available[x[1]], colours))
        if not invalid:
            total += int(line.split(":")[0].split(" ")[1])
    print(total, total_2)


input_day_2 = get_input("2023__2")
solver(input_day_2, pattern)
