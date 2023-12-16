#! python3.11
"""
--- Day 11: Cosmic Expansion ---
You continue following signs for "Hot Springs" and eventually come across
an observatory. The Elf within turns out to be a researcher studying cosmic
expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only
visiting for this research project. However, he confirms that the hot
springs are the next-closest area likely to have people; he'll even take
you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a
single giant image (your puzzle input). The image includes empty space (.)
and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the
shortest path between every pair of galaxies. However, there's a catch: the
universe expanded in the time it took the light from those galaxies to
reach the observatory.

Due to something involving gravitational effects, only some space expands.
In fact, the result is that any rows or columns that contain no galaxies
should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic
expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair
of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order
within the pair doesn't matter. For each pair, find any shortest path
between the two galaxies using only steps that move up, down, left, or
right exactly one . or # at a time. (The shortest path between two galaxies
is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from
galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto
galaxy 9 itself). Here are some other example shortest path lengths:

  - Between galaxy 1 and galaxy 7: 15
  - Between galaxy 3 and galaxy 6: 17
  - Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path
between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between
every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 9974721.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The galaxies are much older (and thus much farther apart) than the
researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column
one million times larger. That is, each empty row should be replaced with
1000000 empty rows, and each empty column should be replaced with 1000000
empty columns.

(In the example above, if each empty row or column were merely 10 times
larger, the sum of the shortest paths between every pair of galaxies would
be 1030. If each empty row or column were merely 100 times larger, the sum
of the shortest paths between every pair of galaxies would be 8410.
However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to
these new rules, then find the length of the shortest path between every
pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 702770569197.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

import copy
import itertools
import numpy

from collections import deque

TEST_DATA = [ '...#......',
              '.......#..',
              '#.........',
              '..........',
              '......#...',
              '.#........',
              '.........#',
              '..........',
              '.......#..',
              '#...#.....',
            ]



def _draw_map(data):
    for i in data:
        print(''.join(i))


def calculate_galaxy_dist(galaxy_1, galaxy_2):
    distance = 0

    # Zip the x and y coords
    coords = [x for x in zip(galaxy_1, galaxy_2)]

    # sort them
    x_positions = [int(x) for x in reversed(sorted(coords[0]))]
    x_dist = x_positions[0] - x_positions[1]

    y_positions = [int(y) for y in reversed(sorted(coords[1]))]
    y_dist = y_positions[0] - y_positions[1]

    # Add the totals
    distance = x_dist + y_dist

    return distance


def expand_galaxy_data(data, expansion_rate):
    galaxy_number = 1
    galaxy_data = numpy.array(copy.deepcopy(data))
    galaxy_dict = {}
    galaxy_pairs = []
    empty_rows = []
    empty_cols = []

    # Expand rows
    for row_idx in range(0, len(galaxy_data) - 1):
        row = galaxy_data[row_idx]
        if '#' not in row:
            empty_rows.append(row_idx)

    # Expand columns
    for col_idx in range(len(galaxy_data[0]) - 1, 0, -1):
        # Build Column data
        col_data = [row[col_idx] for row in galaxy_data]

        # Check for emptiness
        if '#' not in col_data:
            empty_cols.append(col_idx)
            # for row in galaxy_data:
                # row.insert(col_idx, '.')

    # Number the galaxies
    for row_idx in range(0, len(galaxy_data)):
        y_coord = row_idx
        for col_idx in range(0, len(galaxy_data[row_idx])):
            x_coord = col_idx
            if galaxy_data[row_idx][col_idx] == '#':
                galaxy_data[row_idx][col_idx] = str(galaxy_number)
                expansion_x = len([x for x in empty_cols if x <= col_idx])
                expansion_y = len([x for x in empty_rows if x <= row_idx])

                if expansion_x:
                    x_coord = col_idx + expansion_rate * expansion_x

                if expansion_y:
                    y_coord = row_idx + expansion_rate * expansion_y

                galaxy_dict[str(galaxy_number)] = (x_coord, y_coord)
                galaxy_number += 1

    # Galaxy pairs
    galaxy_pairs = itertools.combinations(galaxy_dict.keys(), 2)

    return galaxy_data, galaxy_dict, galaxy_pairs


def parse_data(raw_data):
    # Parse raw_data into a usable form
    data = [deque([x for x in row]) for row in raw_data]

    return data


def main(raw_data, part_two = False):
    expansion_rate = 1
    results = []

    data = parse_data(raw_data)
    if part_two:
        n = 1000000
        expansion_rate = n - 1

    galaxy_data, galaxy_dict, galaxy_pairs = expand_galaxy_data(data, expansion_rate)

    for galaxy_pair in galaxy_pairs:
        result = calculate_galaxy_dist(galaxy_dict[galaxy_pair[0]], galaxy_dict[galaxy_pair[1]])
        results.append(result)

    print(f'\nThe sum of the lengths is {sum(results)}')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_11_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = deque([line for line in input_file.readlines( )])

    # main(TEST_DATA)
    # main(raw_data)
    # main(TEST_DATA, part_two = True)
    main(raw_data, part_two = True)