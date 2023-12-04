import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
from math import prod

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".split(
    "\n"
)

def solver(input):
    total = 0
    total_2 = 0
    CARDS = {i:1 for i in range(1,len(input)+1)}
    card_index = 1
    for line in input:
        card, numbers = line.split(': ')
        valid, mine = map(lambda x: set(x.split()), numbers.split(' | '))
        valid_mine = valid & mine # list(filter(lambda x: x in valid, mine)) 
        if valid_mine:
            total += pow(2, len(valid_mine)-1)
            for k in range(card_index+1, card_index+1+len(valid_mine)):
                CARDS[k] += CARDS[card_index]

        card_index += 1
    print(total)

    # part 2
    total_2 = sum(CARDS.values())
    print(total_2)
   
    return total, total_2


input_day = get_input("2023__4")
solver(input_day)
