import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".split(
    "\n"
)

# tuple : expected_value
EXPECTED = {}
PREVIOUS = {}


def parse_input(input):
    records = [tuple(map(int, line.split())) for line in input]
    return records


def get_previous(line):
    if PREVIOUS.get(line, None) is None:
        # never processed
        up = line[1:] + (0,)

        line_below = tuple(a - b for a, b in zip(up, line))[0:-1]
        if any(line_below):
            # at least one non-zero value
            # we need to continue
            return line[0] - get_previous(line_below)
        else:
            # we found it
            PREVIOUS[line] = line[0]
            return line[0]
    else:
        return PREVIOUS.get(line, None)


def get_next(line):
    if EXPECTED.get(line, None) is None:
        # never processed
        up = line[1:] + (0,)

        line_below = tuple(a - b for a, b in zip(up, line))[0:-1]
        if any(line_below):
            # at least one non-zero value
            # we need to continue
            return line[-1] + get_next(line_below)
        else:
            # we found it
            EXPECTED[line] = line[-1]
            return line[-1]
    else:
        return EXPECTED.get(line, None)


input_day = get_input("2023__9")
records = parse_input(input_day)

# part_1
print(sum(get_next(record) for record in records))
# part_2
print(sum(get_previous(record) for record in records))
