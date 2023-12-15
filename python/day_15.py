import sys
import os
from collections import defaultdict, OrderedDict

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from utils.log import MyLogger
from utils.tools import get_input

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

BOXES = {i: OrderedDict() for i in range(0, 256)}


def parse_input(input):
    # table = str.maketrans(".#", "01")
    # print(input)
    input_list = input.split(",")
    return input_list


def hash(string):
    val = 0
    for c in string:
        val += ord(c)
        val = (17 * val) % 256
    return val


def process_instruction(instruction):
    if "=" in instruction:
        instruction = instruction.split("=")
        instruction_type = "add"
        BOXES[hash(instruction[0])][instruction[0]] = int(instruction[1])

    elif "-" in instruction:
        instruction = instruction.split("-")
        instruction_type = "subtract"
        try:
            BOXES[hash(instruction[0])].pop(instruction[0])
        except:
            # the lens was not in the box
            # print(f'The box {hash(instruction[0])} did not have {ins}')
            pass

    else:
        print("instruction type not expected")


def calculate_focusing(ordered_item):
    # print(ordered_item)
    v = 0
    for i in range(len(ordered_item)):
        v += (i + 1) * ordered_item[i]
    return v


input_day = get_input("2023__15", sep="\n")[0]
input_to_use = input_day

input_list = parse_input(input_to_use)

print("part 1: ", sum(map(hash, input_list)))
# print("part 2: ", 100 * sum(outputs_r2) + sum(outputs_c2))

fill_boxes = list(map(process_instruction, input_list))

total = 0
for k, v in BOXES.items():
    total += (k + 1) * calculate_focusing(list(v.values()))
print("part 2: ", total)
print(
    sum(
        map(
            lambda k, v: (k + 1) * calculate_focusing(list(v.values())),
            BOXES.keys(),
            BOXES.values(),
        )
    )
)
