import sys
import os
from typing import List

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
from math import prod, sqrt
import re
from collections import Counter

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".split(
    "\n"
)

TYPES = ("High", "Two", "Double", "Three", "Full", "Four", "Five")

rank = "23456789TJQKA"
RANK = tuple(r for r in rank)
rank_2 = "J23456789TQKA"
RANK_2 = tuple(r for r in rank_2)


def generate_combinations(starting_string: str, replaced: str) -> List:
    replacing = [letter for letter in starting_string if letter != "J"]
    if not replacing:
        # if we have 5 J, winning combination shoud be 5*A
        replacing = "A"
    combinations = []
    final = []
    combinations.append(starting_string)
    while combinations:
        combination = combinations.pop()
        if "J" not in combination:
            final.append(combination)
        # combination is a string like 'AKJFD'
        for i in range(len(combination)):
            if combination[i] == replaced:
                for k in replacing:
                    combinations.append(combination[0:i] + k + combination[i + 1 :])
    return list(set(final))


class HAND:
    def __init__(self, cards: str, bid: int) -> None:
        self.str = cards
        self.bid = bid
        # self.check_is_valid() # all hands seem valid
        self.type = self.get_type(self.str)
        self.type_value = TYPES.index(self.type)
        self.ranks = self.get_ranks(RANK)

    # def check_is_valid(self):
    #     assert len(self.str) == 5
    #     for i in self.str:
    #         assert i in rank

    def __str__(self):
        return self.str

    def __repr__(self) -> str:
        return self.str

    def get_type(self, str_val):
        ct = Counter(str_val)
        most_common = ct.most_common()[0][1]
        if most_common == 5:
            type_ = "Five"
        elif most_common == 4:
            type_ = "Four"
        elif most_common == 3 and ct.most_common()[1][1] == 2:
            type_ = "Full"
        elif most_common == 3:
            type_ = "Three"
        elif most_common == 2 and ct.most_common()[1][1] == 2:
            type_ = "Double"
        elif most_common == 2:
            type_ = "Two"
        elif most_common == 1:
            type_ = "High"
        else:
            print(self.str)
            raise

        return type_

    def get_ranks(self, rank_checker):
        return tuple(rank_checker.index(i) for i in self.str)

    def __lt__(self, other):
        return (self.type_value, self.ranks) < (other.type_value, other.ranks)

    def __eq__(self, other):
        return self.str == str(other)

    def get_types_part_2(self):
        new_hands = [HAND(val, 0) for val in generate_combinations(self.str, "J")]
        s = sorted(new_hands)
        best = s[-1]
        self._original_type = self.type
        self._original_type_value = self.type_value
        self.type = best.type
        self.type_value = best.type_value
        self.ranks = self.get_ranks(RANK_2)


def parse_input(input):
    return [HAND(cards=line.split()[0], bid=int(line.split()[1])) for line in input]


def calculate_winnings(list_of_hands):
    for i in range(len(list_of_hands)):
        list_of_hands[i].position = i + 1
    total = sum([card.position * card.bid for card in list_of_hands])
    return total


input_day = get_input("2023__7")
hands = parse_input(input_day)

# part_1
print(calculate_winnings(sorted(hands)))

for hand in hands:
    hand.get_types_part_2()
# part_2
print(calculate_winnings(sorted(hands)))


assert generate_combinations("JJJJJ", "J") == ["AAAAA"]
assert generate_combinations("JJJJA", "J") == ["AAAAA"]
