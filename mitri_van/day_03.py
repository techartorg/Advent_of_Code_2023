#! python3.11
"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the
gondola lift will take you up to the water source, but this is as far as he
can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem:
they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of
surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the
engine, but nobody can figure out which one. If you can add up all the part
numbers in the engine schematic, it should be easy to work out which part
is missing.

The engine schematic (your puzzle input) consists of a visual
representation of the engine. There are lots of numbers and symbols you
don't really understand, but apparently any number adjacent to a symbol,
even diagonally, is a "part number" and should be included in your sum.
(Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not
adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of
all of the part numbers in the engine schematic?

Your puzzle answer was 514969.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the
engine springs to life, you jump in the closest gondola, finally ready to
ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still
wrong? Fortunately, the gondola has a phone labeled "help", so you pick it
up and the engineer answers.

Before you can explain the situation, she suggests that you look out the
window. There stands the engineer, holding a phone in one hand and waving
with the other. You're going so slowly that you haven't even left the
station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is
wrong. A gear is any * symbol that is adjacent to exactly two part numbers.
Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all
up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it
has part numbers 467 and 35, so its gear ratio is 16345. The second gear is
in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not
a gear because it is only adjacent to one part number.) Adding up all of
the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

Your puzzle answer was 78915902.

Both parts of this puzzle are complete! They provide two gold stars: **

"""
import numpy

test_data = [ '467..114..',
              '...*......',
              '..35..633.',
              '......#...',
              '617*......',
              '.....+.58.',
              '..592.....',
              '......755.',
              '...$.*....',
              '.664.598..',
             ]


DEBUG = False

class Part():

    def __init__(self, part_number, gear_pos):
        self.part_number = part_number
        self.gear = gear_pos

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.part_number}, [{self.gear[0]}, {self.gear[1]}])>"


def is_valid_symbol(character, gear_only=False):
    if gear_only:
        if not character.isdigit() and character == '*':
            return True

    else:
        if not character.isdigit() and character != '.':
            return True

    return False



def check_validity(row, col, data):
    is_valid = []

    for cur_row in range(row - 1, row + 2):
        if len(data) - 1 >= cur_row >= 0:
            for cur_col in range(col - 1, col + 2):
                if len(data[0]) - 1 >= cur_col >= 0:
                    if DEBUG: print(f'\t{cur_row}, {cur_col} : {data[cur_row][cur_col]}')
                    is_valid.append(is_valid_symbol(data[cur_row][cur_col]))
                else:
                    if DEBUG: print(f'--- {cur_row}, {cur_col}')
    if any(is_valid):
        if DEBUG: print(f'**********\tValid number!')
    else:
        if DEBUG: print('**********')

    return any(is_valid)


def find_current_gear(row, col, data):
    is_valid = []
    found_gear = []

    # Check by rows
    for cur_row in range(row - 1, row + 2):
        if len(data) - 1 >= cur_row >= 0: # Check bounds
            # Check by column
            for cur_col in range(col - 1, col + 2):
                if len(data[0]) - 1 >= cur_col >= 0: # Check bounds
                    if DEBUG: print(f'\t{cur_row}, {cur_col} : {data[cur_row][cur_col]}')
                    result = is_valid_symbol(data[cur_row][cur_col], gear_only=True)
                    is_valid.append(result)
                    if result:
                        found_gear = [cur_row, cur_col]
                else:
                    if DEBUG: print(f'--- {cur_row}, {cur_col}')
    if any(is_valid):
        if DEBUG: print(f'**********\tValid gear at {found_gear}')
    else:
        if DEBUG: print('**********')

    return any(is_valid), found_gear

def parse_data(data):
    is_valid = []
    part_numbers = []

    # Scan line
    for row, datum in enumerate(data):
        found_number = ''
        number_found = False

        for col, character in enumerate(datum):
            if DEBUG: print(f'[{row}, {col}]')
            if character.isdigit():
                number_found = True
                found_number += character
                is_valid.append(check_validity(row, col, data))

            else:
                # Check validity
                if number_found:
                    if any(is_valid):
                        part_numbers.append(int(found_number))
                    # Reset temp variables
                    number_found = False
                    is_valid = []
                    found_number = ''

            if col == len(datum) - 1:
                # Check validity
                if number_found:
                    if any(is_valid):
                        part_numbers.append(int(found_number))
                    # Reset temp variables
                    number_found = False
                    is_valid = []
                    found_number = ''

    return part_numbers


def parse_data_p2(data):

    is_valid = []
    part_numbers = []
    gear_ratios = []
    parts = []

    # Scan line
    for row, datum in enumerate(data):
        current_gear = ''
        found_number = ''
        number_found = False

        for col, character in enumerate(datum):
            if DEBUG: print(f'[{row}, {col}]')
            if character.isdigit():
                number_found = True
                found_number += character
                # is_valid.append(check_validity(row, col, data))
                result, new_gear = find_current_gear(row, col, data)
                is_valid.append(result)
                if result:
                    current_gear = new_gear

            else:
                # Check validity
                if number_found:
                    if any(is_valid):
                        part_numbers.append(int(found_number))
                        parts.append(Part(int(found_number), current_gear))

                    # Reset temp variables
                    number_found = False
                    is_valid = []
                    found_number = ''
                    current_gear = ''

            if col == len(datum) - 1:
                # Check validity
                if number_found:
                    if any(is_valid):
                        part_numbers.append(int(found_number))
                        parts.append(Part(int(found_number), current_gear))

                    # Reset temp variables
                    number_found = False
                    is_valid = []
                    found_number = ''
                    current_gear = ''

    gears = {tuple(x.gear) for x in parts}
    parts_by_gear = [[x for x in parts if tuple(x.gear)==gear] for gear in gears]

    for part_group in parts_by_gear:
        if len(part_group) > 1:
            gear_group = [x.part_number for x in part_group]
            gear_ratios.append(numpy.prod(gear_group))

    return gear_ratios


def main(data, part_two = False):
    part_numbers = []

    if not part_two:
        part_numbers = parse_data(data)
        print(f'\nThe sum of all part numbers: {part_numbers}\n\tis {sum(part_numbers)}\n')

    else:
        part_numbers = parse_data_p2(data)
        print(f'\nThe sum of all the gear ratios: {part_numbers}\n\tis {sum(part_numbers)}\n')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_03_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.rstrip() for line in input_file.readlines( )]

    # main(test_data)
    # main(raw_data)
    # main(test_data, part_two=True)
    main(raw_data, part_two=True)