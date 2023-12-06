import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from utils.log import MyLogger
from utils.tools import get_input
from math import inf

logger = MyLogger(log_file="aoc2023.log", log_path="logs", name=__name__)

sample_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42 
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split(
    "\n"
)
MAPPINGS = []
answers = {}


def parse_input(input):
    seeds = list(map(int, input[0].split(": ")[1].replace("\n", "").split(" ")))
    input = list(filter(lambda x: x != "", input))
    # dummy line, easier than parsing
    input.append(":")
    entry_id = -1
    new_vals = []

    for i in range(1, len(input)):
        if ":" in input[i] or i == len(input):
            # new entry
            if entry_id > -1 and new_vals:
                MAPPINGS.append(new_vals)
            entry_id += 1
            new_vals = []
        elif input[i] == "":
            pass
        else:
            new_vals.append(list(map(int, input[i].split())))
    return seeds


def solver(input):
    final_locations = []
    seeds = parse_input(input)
    for seed in seeds:
        # seeds:
        current_location = seed
        for k in range(len(MAPPINGS)):
            current_location = find_next_position(current_location, MAPPINGS[k])

        final_locations.append(current_location)

    seeds_part_two = [(seeds[i * 2], seeds[i * 2 + 1]) for i in range(len(seeds) // 2)]
    return min(final_locations), seeds_part_two


def find_next_position(current_position, mapping):
    next_position = False
    for element in mapping:
        if (current_position >= element[1]) and (
            current_position < element[1] + element[2]
        ):
            next_position = element[0] + (current_position - element[1])
    if not next_position:
        next_position = current_position
    return next_position


def get_new(option, alternative):
    """Maps initial source to target following rules given
    e.g.
    # (-5, 105, -5, 105) (-5, 49, -5, 49) (-5, 49, -5, 49)
    # (-5, 105, -5, 105) (50, 97, 52, 99) (50, 97, 52, 99)
    # (-5, 105, -5, 105) (98, 99, 50, 51) (98, 99, 50, 51)
    # (-5, 105, -5, 105) (100, 105, 100, 105) (100, 105, 100, 105)
    # (98, 99, 50, 51) (15, 51, 0, 36) (63, 64, 0, 1) --> (98, 99, 35, 36)
    # (0, 14, 39, 53),(11, 52, 0, 41) (0, 13, 28, 41)
    """

    source_min = max(option[0], option[0] - option[2] + alternative[0])
    max_range = min(alternative[1], option[3]) - max(alternative[0], option[2])
    source_max = source_min + max_range
    target_min = max(alternative[2], alternative[2] - alternative[0] + option[2])
    target_max = target_min + max_range
    # mapping of source values to target values
    new_val = (source_min, source_max, target_min, target_max)
    return new_val


input_day = get_input("2023__5")
part_1, seeds_p2 = solver(input_day)
print(part_1)
# get the max range of values possible
abs_min = min([x[0] for x in seeds_p2]) - 1
abs_max = max([x[0] + x[1] - 1 for x in seeds_p2]) + 1
for mapping in MAPPINGS:
    abs_min = min(abs_min, min([x[0] for x in mapping]) - 1)
    abs_max = max(abs_max, max([x[0] + x[1] - 1 for x in mapping]) + 1)

# prepare the mapping of the translation from seed to final locations
NMAP = []

for mapping in MAPPINGS:
    boundaries_source = set((abs_min, abs_max))
    boundaries_target = set((abs_min, abs_max))
    nm = []
    for element in mapping:
        temp = (
            element[1],
            element[1] + element[2] - 1,
            element[0],
            element[0] + element[2] - 1,
        )
        nm.append(temp)
        boundaries_source.update((temp[0], temp[1]))
        boundaries_target.update((temp[2], temp[3]))
    nm = sorted(nm)

    nm.extend(
        [
            (nm[-1][1] + 1, abs_max, nm[-1][1] + 1, abs_max),
            (abs_min, nm[0][0] - 1, abs_min, nm[0][0] - 1),
        ]
    )
    nm = sorted(nm)
    current = (abs_min, abs_max)
    ext = []
    for item in nm:
        if current[0] == item[0] or current[1] == item[1]:
            # all good, update current
            current = (item[1] + 1, abs_max)
        else:
            # there's a gap in the instructions given, add to the extension list
            # when there's not a match, the mapping is 1:1 (e.g. same value in
            # target as in source)
            ext.append(
                (
                    current[0],
                    item[0] - 1,
                    current[0],
                    item[0] - 1,
                )
            )
            current = (item[1] + 1, abs_max)
    nm.extend(ext)
    nm = sorted(nm)

    NMAP.append(sorted(nm))


initial_map = [(abs_min, abs_max, abs_min, abs_max)]
temp = initial_map[:]

for mapping in NMAP:
    transient = []
    for option in temp:
        for alternative in mapping:
            new_val = ()
            if min(alternative[1], option[3]) - max(option[2], alternative[0]) >= 0:
                new_val = get_new(option, alternative)
                transient.append(new_val)
    temp = sorted(transient)[:]

# get the min_val possible given the seeds:
min_val = inf
for seed in seeds_p2:
    # print(seed)
    for comb in temp:
        seeder = (seed[0], seed[0] + seed[1] - 1, seed[0], seed[0] + seed[1] - 1)
        if min(comb[1], seeder[3]) - max(seeder[2], comb[0]) >= 0:
            output = get_new(seeder, comb)
            min_val = min(min_val, output[2])
print(min_val)

assert min_val == 37806486, "Part 2 error"
assert part_1 == 1181555926, "Part 1 error"

assert get_new((-5, 49, -5, 49), (-5, -1, -5, -1)) == (-5, -1, -5, -1)
assert get_new((-5, 49, -5, 49), (0, 14, 39, 53)) == (0, 14, 39, 53)
assert get_new((-5, 49, -5, 49), (15, 51, 0, 36)) == (15, 49, 0, 34)
assert get_new((-5, 105, -5, 105), (100, 105, 100, 105)) == (100, 105, 100, 105)
assert get_new((98, 99, 50, 51), (15, 51, 0, 36)) == (98, 99, 35, 36)
assert get_new((0, 14, 39, 53), (11, 52, 0, 41)) == (0, 13, 28, 41)
