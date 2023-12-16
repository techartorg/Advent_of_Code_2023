#! python3.11
"""
--- Day 14: Parabolic Reflector Dish ---
You reach the place where all of the mirrors were pointing: a massive
parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves
are roughly in the shape of a parabolic reflector dish, each individual
mirror seems to be pointing in slightly the wrong direction. If the dish is
meant to focus light, all it's doing right now is sending it in a vague
direction.

This system must be what provides the energy for the lava! If you focus the
reflector dish, maybe you can go where it's pointing and use the light to
fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected
via an elaborate system of ropes and pulleys to a large metal platform
below the dish. The platform is covered in large rocks of various shapes.
Depending on their position, the weight of the rocks deforms the platform,
and the shape of the platform controls which ropes move and ultimately the
focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even
has a control panel on the side that lets you tilt it in one of four
directions! The rounded rocks (O) will roll when the platform is tilted,
while the cube-shaped rocks (#) will stay in place. You note the positions
of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as
they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are
damaged; to ensure the platform doesn't collapse, you should calculate the
total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the
number of rows from the rock to the south edge of the platform, including
the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.)
So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks.
In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what
is the total load on the north support beams?

Your puzzle answer was 110274.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the
beam. To do that, you'll need to move the rocks to the edges of the
platform. Fortunately, a button on the side of the control panel labeled
"spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll
north, then west, then south, then east. After each tilt, the rounded rocks
roll as far as they can before the platform tilts in the next direction.
After one cycle, the platform will have finished rolling the rounded rocks
in those four directions in that order.

Here's what happens in the example above after each of the first few
cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

This process should work if you leave it running long enough, but you're
still worried about the north support beams. To make sure they'll survive
for a while, you need to calculate the total load on the north support
beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north
support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load
on the north support beams?

Your puzzle answer was 90982.

Both parts of this puzzle are complete! They provide two gold stars: **

"""

import numpy

from collections import deque

TEST_DATA = [ 'O....#....',
              'O.OO#....#',
              '.....##...',
              'OO.#O....O',
              '.O.....O#.',
              'O.#..O.#.#',
              '..O..#O..O',
              '.......O..',
              '#....###..',
              '#OO..#....',
            ]

OPEN_GROUND = '.'
ROCK_ROUND = 'O'
ROCK_FLAT = '#'


class Rock():

    def __init__(self, pos_x, pos_y, is_round=True):
        self.x = pos_x
        self.y = pos_y
        self.is_round = is_round

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.x},{self.y})>"

    def __str__(self):
        if self.is_round:
            return ROCK_ROUND

        return '#'

    def __eq__(self, other):
        if isinstance(other, Rock):
            return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        if isinstance(other, Rock):
            return (self.x, self.y) > (other.x, other.y)

    def __lt__(self, other):
        if isinstance(other, Rock):
            return (self.x, self.y) < (other.x, other.y)


def _print(data):
    if isinstance(data, list):
        for datum in data:
            print(''.join(map(str,datum)))
    else:
        print(f"\t{''.join(map(str,data))}")


def _sort_rocks(row):
    result = []

    for idx, obj in enumerate(row):
        if isinstance(obj, Rock):
            obj.x = idx
            result.append(obj)

    return result


def calculate_load(data):
    load = []
    results = []
    working_data = numpy.transpose(data)

    for row_idx, row in enumerate(working_data):
        results = []
        for col_idx, position_data in enumerate(row):
            if isinstance(position_data, Rock) and position_data.is_round:
                load_value = len(row) - col_idx
                results.append(load_value)
        load.extend(results)

    return load


def move_rocks(data, part_two = False):
    processed_rocks = []
    working_data = data.transpose()

    for row in working_data:
        sorted_row = _sort_rocks(row)
        rocks = deque(sorted_row)

        for column_idx, column_data in enumerate(row):
            if column_data == OPEN_GROUND and rocks:
                if rocks[0].is_round:
                    new_rock = rocks.popleft()
                    new_rock.x = column_idx

                    row[numpy.where(row == new_rock)] = '.'
                    row[column_idx] = new_rock
                    processed_rocks.append(new_rock)

            elif column_data in rocks:
                processed_rocks.append(column_data)
                del rocks[rocks.index(column_data)]
            else:
                pass # do nothing

    if part_two:
        # West
        processed_rocks = []
        working_data = working_data.transpose()

        for row in working_data:
            sorted_row = _sort_rocks(row)
            rocks = deque(sorted_row)

            for column_idx, column_data in enumerate(row):
                if column_data == OPEN_GROUND and rocks:
                    if rocks[0].is_round:
                        new_rock = rocks.popleft()
                        new_rock.x = column_idx

                        row[numpy.where(row == new_rock)] = '.'
                        row[column_idx] = new_rock
                        processed_rocks.append(new_rock)

                elif column_data in rocks:
                    processed_rocks.append(column_data)
                    del rocks[rocks.index(column_data)]
                else:
                    pass # do nothing

        # South
        processed_rocks = []
        working_data = numpy.flip(working_data).transpose()

        for row in working_data:
            sorted_row = _sort_rocks(row)
            rocks = deque(sorted_row)

            for column_idx, column_data in enumerate(row):
                if column_data == OPEN_GROUND and rocks:
                    if rocks[0].is_round:
                        new_rock = rocks.popleft()
                        new_rock.x = column_idx

                        row[numpy.where(row == new_rock)] = '.'
                        row[column_idx] = new_rock
                        processed_rocks.append(new_rock)

                elif column_data in rocks:
                    processed_rocks.append(column_data)
                    del rocks[rocks.index(column_data)]
                else:
                    pass # do nothing

        # East
        processed_rocks = []
        working_data = working_data.transpose()

        for row in working_data:
            sorted_row = _sort_rocks(row)
            rocks = deque(sorted_row)

            for column_idx, column_data in enumerate(row):
                if column_data == OPEN_GROUND and rocks:
                    if rocks[0].is_round:
                        new_rock = rocks.popleft()
                        new_rock.x = column_idx

                        row[numpy.where(row == new_rock)] = '.'
                        row[column_idx] = new_rock
                        processed_rocks.append(new_rock)

                elif column_data in rocks:
                    processed_rocks.append(column_data)
                    del rocks[rocks.index(column_data)]
                else:
                    pass # do nothing
        working_data = numpy.flip(working_data)
    else:
        working_data = working_data.transpose()

    return working_data


def parse_data(raw_data):
    data = []

    for row_idx, datum in enumerate(raw_data):
        row_data = []
        for col_idx, x in enumerate(datum):
            obj = x
            if obj == ROCK_FLAT:
                obj = Rock(row_idx, col_idx, is_round = False)
            elif obj == ROCK_ROUND:
                obj = Rock(row_idx, col_idx)

            row_data.append(obj)
        data.append(row_data)

    data = numpy.array(data)

    return data


def main(raw_data, part_two = False):
    results = []
    test_results = []

    data = parse_data(raw_data)
    if part_two:
        cycles = 1000000000
        cycle_data = data
        num = 0
        while num in range(0, cycles):
            cycle_data = move_rocks(cycle_data, part_two)
            num += 1
            result = calculate_load(cycle_data)
            test_results.append(sum(result))
        data = cycle_data
    else:
        data = move_rocks(data, part_two)

    results = calculate_load(data)

    print(f'\nThe total load on the north support beams is {sum(results)}')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_14_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line for line in input_file.readlines( )]

    # main(TEST_DATA)
    # main(raw_data)
    # main(TEST_DATA, part_two = True)
    main(raw_data, part_two = True)

# z = deque([91039, 91031, 91003, 90974, 90950, 90923, 90918, 90931, 90946, 90982, 91016, 91038, 91057, 91050])
# z.rotate(1000000000 - 178 % 14)
# z[0]
# 90982