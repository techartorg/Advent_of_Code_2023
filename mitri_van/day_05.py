#! python3.11
"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would
be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that
Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with!
Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand
soon; we only turned off the water a few days... weeks... oh no." His face
sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely
forgot to check why we stopped getting more sand! There's a ferry leaving
soon that is headed over in that direction - it's much faster than your
boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another.
"While you wait for the ferry, maybe you can help us with our food
production problem. The latest Island Island Almanac just arrived and we're
having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be
planted. It also lists what type of soil to use with each kind of seed,
what type of fertilizer to use with each kind of soil, what type of water
to use with each kind of fertilizer, and so on. Every type of seed, soil,
fertilizer and so on is identified with a number, but numbers are reused by
each category - that is, soil 123 and fertilizer 123 aren't necessarily
related to each other.

For example:

    seeds: 79 14 55 13

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
    56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14,
55, and 13.

The rest of the almanac contains a list of maps which describe how to
convert numbers from a source category into numbers in a destination
category. That is, the section that starts with seed-to-soil map: describes
how to convert a seed number (the source) to a soil number (the
destination). This lets the gardener and his team know which soil to use
with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination
number one by one, the maps describe entire ranges of numbers that can be
converted. Each line within a map contains three numbers: the destination
range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of
98, and a range length of 2. This line means that the source range starts
at 98 and contains two values: 98 and 99. The destination range is the same
length, but it starts at 50, so its two values are 50 and 51. With this
information, you know that seed number 98 corresponds to soil number 50 and
that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48
values: 50, 51, ..., 96, 97. This corresponds to a destination range
starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed
number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination
number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers
looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial
seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so
they'd like to know the closest location that needs a seed. Using these
maps, find the lowest location number that corresponds to any of the
initial seeds. To do this, you'll need to convert each seed number through
other categories until you can find its corresponding location number. In
this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78,
    humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42,
    humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82,
    humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34,
    humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial
seed numbers?

Your puzzle answer was 196167384.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-
reading the almanac, it looks like the seeds: line actually describes
ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the
first value is the start of the range and the second value is the length of
the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden.
The first range starts with seed number 79 and contains 14 values: 79, 80,
..., 91, 92. The second range starts with seed number 55 and contains 13
values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a
total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed
number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77,
temperature 45, humidity 46, and location 46. So, the lowest location
number is 46.

Consider all of the initial seed numbers listed in the ranges on the first
line of the almanac. What is the lowest location number that corresponds to
any of the initial seed numbers?

"""
import copy
from collections import defaultdict, deque

test_data = [ 'seeds: 79 14 55 13',
              '',
              'seed-to-soil map:',
              '50 98 2',
              '52 50 48',
              '',
              'soil-to-fertilizer map:',
              '0 15 37',
              '37 52 2',
              '39 0 15',
              '',
              'fertilizer-to-water map:',
              '49 53 8',
              '0 11 42',
              '42 0 7',
              '57 7 4',
              '',
              'water-to-light map:',
              '88 18 7',
              '18 25 70',
              '',
              'light-to-temperature map:',
              '45 77 23',
              '81 45 19',
              '68 64 13',
              '',
              'temperature-to-humidity map:',
              '0 69 1',
              '1 0 69',
              '',
              'humidity-to-location map:',
              '60 56 37',
              '56 93 4',
            ]

SEED_HEADER = 'seeds'
RESOURCE_MAP = [ SEED_HEADER,
                'seed-to-soil map',
                'soil-to-fertilizer map',
                'fertilizer-to-water map',
                'water-to-light map',
                'light-to-temperature map',
                'temperature-to-humidity map',
                'humidity-to-location map'
               ]


DEBUG = True



class MappingTable():

    def __init__(self, id, data):
        self.id = id
        self.data = {}

        self.initialize_data(data)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} ({self.data})>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id} ({self.data})>"

    def initialize_data(self, data):
        for item in data:
            target, source, map_range = item.split()
            self.data[int(source)] = (int(target), int(map_range))


    def get_target_value(self, seed_value):
        target_value = seed_value
        # if source_value in the range of each data-key value
        for key in reversed(sorted(self.data.keys())):
            range_start_value = self.data[key][0]
            range_size = self.data[key][1]

            if key <= seed_value <= key + range_size - 1:
                target_value = seed_value - key + range_start_value

        return target_value

    def get_target_value_range(self, seed, recurse_depth='\t'):
        overlap_range = 0
        results = []

        target_value = None
        target_range = None

        seed_value = seed[0]
        seed_range = seed[1]

        # Find the key range the supplied seed fits into
        for key in sorted(self.data.keys()):
            range_value_initial = self.data[key][0]
            range_size = self.data[key][1]

            # Supplied value is in this mapping range; use overlapped value if this check bled over from a previous iteration
            if overlap_range or (key <= seed_value <= key + range_size - 1):
                if DEBUG: print(f'{recurse_depth}get_target_value_range: {range_value_initial} {key} {range_size}')
                new_seed_value = seed_value - key + range_value_initial
                if overlap_range:
                    new_seed_value = range_value_initial

                # Supplied value is contained in one of the map ranges
                if seed_value + seed_range <= key + range_size:
                    if overlap_range:
                        results.append((new_seed_value, seed_range - overlap_range))
                        overlap_range = 0
                    else:
                        results.append((new_seed_value, seed_range))

                # Supplied value overlaps multiple map ranges
                # Add the current range and bookmark the overlapped range
                else:
                    overlap_range = key + range_size - 1 - seed_value
                    results.append((new_seed_value, overlap_range))
        if results:
            return results

        return [seed]

    def print_map(self):
        print(f'{self.id}:')
        for num in sorted(self.data.keys()):
            print(f'\t{num}:\t{self.data[num]}')


def _print_map(data, ver=0):
    if ver == 0:
        for category in sorted(data.keys()):
            print(f'{category}:\t{data[category]}')
    elif ver == 1:
        for key in data.keys():
            data[key].print_map()
    else:
        for category in data.keys():
            print(f'{category}:\n\t{data[category]}')


def find_location_by_seed(seed_num, data):
    result = None

    current_location_map = data.popleft()
    location = current_location_map.get_target_value(seed_num)
    if DEBUG: print(f'{current_location_map.id}:\n\t{seed_num} -> {location}')

    if data:
        result = find_location_by_seed(location, data)

    if result:
        return result

    return location


def find_location_by_seed_range(seed, data, recurse_depth = '\t'):
    result = []

    current_location_map = data.popleft()
    locations = current_location_map.get_target_value_range(seed, recurse_depth)
    # if DEBUG: print(f'\t{current_location_map.id}:\n\t\t{seed} -> {locations}')
    if DEBUG: print(f'\n{recurse_depth}{current_location_map.id}:\n{recurse_depth}\t{seed} -> {locations}')
    if data:
        for location in locations:
            x = find_location_by_seed_range(location, copy.deepcopy(data), recurse_depth = recurse_depth + '\t')
            if isinstance(x, list):
                result = result + x
            else:
                result.append(x)

    else:
        if len(locations) != 1:
            for location in locations:
                x = current_location_map.get_target_value_range(location)
                if isinstance(x, list):
                    if len(x) != 1:
                        assert "Wtf"
                    else:
                        result.append((x[0][0], 0))

                else:
                    result.append((x, 0))
        else:
            result.append((locations[0][0],0))

    if result:
        return result

    return locations


def find_seed_location(seeds, resource_mappings):
    results = []
    locations = []

    for seed in seeds:
        if DEBUG: print(f'Seed: {seed}')
        # Part 1
        if not isinstance(seed, tuple):
            locations = find_location_by_seed(seed, copy.deepcopy(resource_mappings))

        # Part 2
        else:
            locations = find_location_by_seed_range(seed, copy.deepcopy(resource_mappings))

        if isinstance(locations, list):
            results = results + locations
        else:
            results.append(locations)

        if DEBUG: print('')
# Figure out what happens when more than 2 locations are returned
    return results


def generate_mapping_data(key, data):
    # asset_map = {}

    # for item in data[key]:
        # target, source, map_range = item.split()
        # for i in range(0,int(map_range)):
            # asset_map[int(source) + i] = int(target) + i

    return asset_map


def parse_data(raw_data):
    data = defaultdict(list)
    mapping_category = SEED_HEADER

    for line in raw_data:
        # Blank line found; prepare for a new mapping category
        if not line:
            mapping_category = None

        # First line or mapping_category found
        elif mapping_category == SEED_HEADER or not mapping_category:
            if mapping_category == SEED_HEADER:
                category_header, mapping_data = line.split(': ')
                data[category_header] = [int(x) for x in mapping_data.split()]
            else:
                mapping_category = line.rstrip(':')

        # Line has to contain mappings, by order of elimination
        else:
            data[mapping_category].append(line)

    return data


def parse_seeds(data):
    seeds = data
    new_seeds = []

    if len(data) % 2 != 0:
        assert 'Data not provided in pairs'

    idx = 0
    while idx < len(data):
        source = data[idx]
        map_range = data[idx + 1]
        new_seeds.append((source, map_range))
        idx += 2
    if new_seeds: seeds = new_seeds

    return seeds


def main(raw_data, part_two = False):
    data = parse_data(raw_data)

    resource_mappings = deque()
    result = []

    # Define seeds
    seeds = data[SEED_HEADER]

    if part_two:
        seeds = parse_seeds(data[SEED_HEADER])

    # Define resource mappings
    for key in RESOURCE_MAP[1:]:
        new_mapping_table = MappingTable(key, data[key])
        resource_mappings.append(new_mapping_table)

    # Find seed location
    result = find_seed_location(seeds, resource_mappings)

    if not part_two:
        print(f'\nThe lowest location number that corresponds to any of the initial seed numbers is {min(result)}')
    else:
        print(f'\nThe lowest location number that corresponds to any of the initial seed numbers is {min([x[0] for x in result])}')


if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_05_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.rstrip() for line in input_file.readlines( )]

    # main(test_data)
    # main(raw_data)
    main(test_data, part_two = True)
    # main(raw_data, part_two = True)