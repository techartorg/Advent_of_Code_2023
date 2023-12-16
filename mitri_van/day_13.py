#! python3.11
"""
--- Day 13: Point of Incidence ---
With your help, the hot springs team locates an appropriate spring which
launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like
gray mountains scattered around. After a while, you make your way to a
nearby cluster of mountains only to discover that the valley between them
is completely full of large mirrors. Most of the mirrors seem to be aligned
in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them
have fallen from the large metal frames keeping them in place. The mirrors
are extremely flat and shiny, and many of the fallen mirrors have lodged
into the ash at strange angles. Because the terrain is all one color, it's
hard to tell where it's safe to walk or where you're about to run into a
mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you
walk (your puzzle input); perhaps by carefully analyzing these patterns,
you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

To find the reflection in each pattern, you need to find a perfect
reflection across either a horizontal line between two rows or across a
vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two
columns; arrows on each of the two columns point at the line between the
columns:

123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789

In this pattern, the line of reflection is the vertical line between
columns 5 and 6. Because the vertical line is not perfectly in the middle
of the pattern, part of the pattern (column 1) has nowhere to reflect onto
and can be ignored; every other column has a reflected column within the
pattern and must match exactly: column 2 matches column 9, column 3 matches
8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row
1 would reflect with a hypothetical row 8, but since that's not in the
pattern, row 1 doesn't need to match anything. The remaining rows match:
row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left
of each vertical line of reflection; to that, also add 100 multiplied by
the number of rows above each horizontal line of reflection. In the above
example, the first pattern's vertical line has 5 columns to its left and
the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What
number do you get after summarizing all of your notes?

Your puzzle answer was 33735.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
You resume walking through the valley of mirrors and - SMACK! - run
directly into one. Hopefully nobody was watching, because that must have
been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one
smudge: exactly one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a
different reflection line to be valid. (The old reflection line won't
necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

The first pattern's smudge is in the top-left corner. If the top-left #
were instead ., it would have a different, horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7

With the smudge in the top-left corner repaired, a new horizontal line of
reflection between rows 3 and 4 now exists. Row 7 has no corresponding
reflected row and can be ignored, but every other row matches exactly: row
1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol
on row 2 from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7

Now, the pattern has a different horizontal line of reflection between rows
1 and 2.

Summarize your notes as before, but instead use the new different
reflection lines. In this example, the first pattern's new horizontal line
has 3 rows above it and the second pattern's new horizontal line has 1 row
above it, summarizing to the value 400.

In each pattern, fix the smudge and find the different line of reflection.
What number do you get after summarizing the new reflection line in each
pattern in your notes?
"""

import difflib
import numpy

TEST_DATA = [ '#.##..##.',
              '..#.##.#.',
              '##......#',
              '##......#',
              '..#.##.#.',
              '..##..##.',
              '#.#.##.#.',
              '',
              '#...##..#',
              '#....#..#',
              '..##..###',
              '#####.##.',
              '#####.##.',
              '..##..###',
              '#....#..#',
            ]

DEBUG = True



def _print(data):
    for datum in data:
        [print(''.join(row)) for row in datum]


def _diff_reflection(a, b):
    diff_idx = -1
    diff_val = None

    diff_ratio = difflib.SequenceMatcher(None, ''.join(a), ''.join(b)).ratio()
    if 0.857 < diff_ratio < 1.0:
        for idx, val in enumerate(difflib.ndiff(a, b)):
            diff_idx = idx
            diff_val = val

    return diff_idx, diff_val


def _check_smudge(mirror_data, mirror_axis):
    smudge_found = False

    a_side = mirror_axis - 1
    b_side = mirror_axis

    # Scan the reflection until a mismatch is found
    while not smudge_found:
        if a_side < 0 or b_side > len(mirror_data) - 1:
            return smudge_found

        if ''.join(mirror_data[a_side]) != ''.join(mirror_data[b_side]):
            # Check the mismatch to see if it's a smudge
            diff_idx, diff_val = _diff_reflection(mirror_data[a_side], mirror_data[b_side])
            if diff_idx != -1:
                smudge_found = True
                # Fix the smudge
                mirror_data[a_side] = [x for x in mirror_data[b_side]]

        a_side -= 1
        b_side += 1

    return smudge_found


def _find_smudge(mirror):
    working_mirror = mirror.copy()
    # Scan the miror for the reflection point
    for idx in range(0, len(working_mirror) - 1):
        if ''.join(mirror[idx]) == ''.join(working_mirror[idx + 1]):
            result = _check_smudge(working_mirror, idx + 1)

            if result:
                valid_reflection = _check_reflection(working_mirror, idx + 1)
                if valid_reflection:
                    mirror[idx] = [x for x in mirror[idx + 1]]
                    return idx + 1
    return -1


def desmudge_mirror(data):
    x_results = []
    y_results = []

    for mirror_num, mirror in enumerate(data):
        result = 0

        # Find reflection on the x-axis
        reflection_x = _find_reflection(mirror.transpose())
        reflection_y = _find_reflection(mirror)

        # Find a different reflection line along X
        mirror = mirror.transpose()
        if reflection_x == -1:
            # Find a reflection line, then look for a smudge
            x_axis = _find_smudge(mirror)
            if x_axis != -1:
                x_results.append(x_axis)

        else:
            # Scan for a new reflection close enough to be desmudged into existence
            for idx in range(0, len(mirror) - 2):
                if ''.join(mirror[idx]) != ''.join(mirror[idx + 1]):
                    # Check the mismatch to see if it's a smudge
                    diff_idx, diff_val = _diff_reflection(mirror[idx], mirror[idx + 1])
                    if diff_idx != -1:
                        mirror[idx] = [x for x in mirror[idx + 1]]
                        x_results.append(idx + 1)
                elif idx + 1 != reflection_x:
                    x_results.append(idx)
        mirror = mirror.transpose()


        # Find a different reflection line along Y
        if reflection_y == -1:
            # Find a reflection line, then look for a smudge
            y_axis = _find_smudge(mirror)
            y_results.append(y_axis)

        else:
            # Scan for a new reflection close enough to be desmudged into existence
            for idx in range(0, len(mirror) - 2):
                if ''.join(mirror[idx]) != ''.join(mirror[idx + 1]):
                    # Check the mismatch to see if it's a smudge
                    diff_idx, diff_val = _diff_reflection(mirror[idx], mirror[idx + 1])
                    if diff_idx != -1:
                        mirror[idx] = [x for x in mirror[idx + 1]]
                        y_results.append(idx + 1)
                elif idx + 1 != reflection_y:
                    y_results.append(idx)

        if DEBUG: print(f'[Mirror {mirror_num:02}] ({reflection_x}, {reflection_y})\n\t\t\t {x_results[-1]}, {y_results[-1]}')
        if DEBUG: [print(f"\t\t{''.join(x)}") for x in mirror]
        if DEBUG: print('\n')

    result = sum(x_results) + (100 * sum(y_results))

    return result


def _check_reflection(mirror_data, mirror_axis):
    is_reflection = True

    a_side = mirror_axis - 1
    b_side = mirror_axis
    while is_reflection:
        if a_side < 0 or b_side > len(mirror_data) - 1:
            return is_reflection

        if ''.join(mirror_data[a_side]) != ''.join(mirror_data[b_side]):
            is_reflection = False

        a_side -= 1
        b_side += 1

    return is_reflection


def _find_reflection(mirror):
    for idx in range(0, len(mirror) - 1):
        if ''.join(mirror[idx]) == ''.join(mirror[idx + 1]):
            result = _check_reflection(mirror, idx + 1)
            if result:
                return idx + 1
    return -1


def find_reflection_values(data):
    result = 0
    x_results = []
    y_results = []

    for idx, mirror in enumerate(data):
        # Find reflection on the x-axis
        x_mirror = mirror.transpose()
        x_axis = _find_reflection(x_mirror)

        if x_axis > 0:
            x_results.append(x_axis)
            if DEBUG: print(f'{idx:02} {x_axis} : {x_axis}')

        # Find reflection on the y-axis
        else:
            y_axis = _find_reflection(mirror)

            if  y_axis > 0:
                y_results.append(y_axis)
                if DEBUG: print(f'{idx:02} {y_axis} : {y_axis * 100}')

        if DEBUG: [print(f"\t\t\t{''.join(x)}") for x in mirror]

    result = sum(x_results) + (100 * sum(y_results))

    return result


def parse_data(raw_data):
    data = []
    mirror = []

    for datum in raw_data:
        if datum != '':
            mirror.append([x for x in datum])
        else:
            data.append(numpy.array(mirror))
            mirror = []

    # Add the last element
    if mirror:
        data.append(numpy.array(mirror))

    return data


def main(raw_data, part_two = False):
    result = 0
    data = parse_data(raw_data)

    if part_two:
        result = desmudge_mirror(data)
    else:
        result = find_reflection_values(data)

    print(f'\nThe numbers of all the summarized notes is {result}')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_13_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.strip() for line in input_file.readlines( )]

    # main(TEST_DATA)
    # main(raw_data)
    # main(TEST_DATA, part_two = True)
    main(raw_data, part_two = True)

# Low
# 25755
# 36227
# 36258