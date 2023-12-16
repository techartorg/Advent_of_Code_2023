#! python3.11
"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to
take a look. The Elves have even given you a map; on it, they've used stars
to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations,
you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on
each day in the Advent calendar; the second puzzle is unlocked when you
complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful
enough") and where they're even sending you ("the sky") and why your map
looks mostly blank ("you sure ask a lot of questions") and hang on did you
just say the sky ("of course, where do you think snow comes from") when you
realize that the Elves are already loading you into a trebuchet ("please
hold still, we need to strap you in").

As they're making the final adjustments, they discover that their
calibration document (your puzzle input) has been amended by a very young
Elf who was apparently just excited to show off her art skills.
Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each
line originally contained a specific calibration value that the Elves now
need to recover. On each line, the calibration value can be found by
combining the first digit and the last digit (in that order) to form a
single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15,
and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the
calibration values?

Your puzzle answer was 55123.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are
actually spelled out with letters: one, two, three, four, five, six, seven,
eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and
last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
Adding these together produces 281.

What is the sum of all of the calibration values?

Your puzzle answer was 55260.

Both parts of this puzzle are complete! They provide two gold stars: **
"""
import re

test_data_1 = [ '1abc2',
                'pqr3stu8vwx',
              'a1b2c3d4e5f',
              'treb7uchet'
              ]

test_data_2 = [ 'two1nine',
                'eightwothree',
               'abcone2threexyz',
               'xtwone3four',
               '4nineeightseven2',
               'zoneight234',
               '7pqrstsixteen',
               ]

number_mapping = [ ('one', '1'),
                   ('two', '2'),
                   ('three', '3'),
                   ('four', '4'),
                   ('five', '5'),
                   ('six', '6'),
                   ('seven', '7'),
                   ('eight', '8'),
                   ('nine', '9')
                   ]


DEBUG = False

def parse_line(data):
    log = data

    data = re.sub('(oneight)', '18', data)
    data = re.sub('(twone)', '21', data)
    data = re.sub('(threeight)', '38', data)
    data = re.sub('(fiveight)', '58', data)
    data = re.sub('(sevenine)', '79', data)
    data = re.sub('(eightwo)', '82', data)
    data = re.sub('(eighthree)', '83', data)
    data = re.sub('(nineight)', '98', data)

    data = re.sub('(one)', '1', data)
    data = re.sub('(two)', '2', data)
    data = re.sub('(three)', '3', data)
    data = re.sub('(four)', '4', data)
    data = re.sub('(five)', '5', data)
    data = re.sub('(six)', '6', data)
    data = re.sub('(seven)', '7', data)
    data = re.sub('(eight)', '8', data)
    data = re.sub('(nine)', '9', data)

    log = (f'{data} - {log}')
    return data, log


def _calculate_calibration_value(datum):
    result = 0
    digits = [x for x in datum if x.isdigit()]
    if digits:
        result += int(''.join([digits[0], digits[-1]]))

    return result


def get_calibration_values(data, part_two=False):
    calibration_values = []

    for datum in data:
        log = datum
        if part_two: datum, log = parse_line(datum)
        result = _calculate_calibration_value(datum)
        calibration_values.append(result)

        log = f"{result}\t{log}"
        if DEBUG: print(log)
    return calibration_values


def main(raw_data , part_two = False):
    calibration_values = get_calibration_values(raw_data, part_two=part_two)
    print(f'The sum of: {calibration_values}\n\tis {sum(calibration_values)}\n')


if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_01_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.rstrip() for line in input_file.readlines()]

    main(test_data_1)
    main(raw_data)
    print('*****************************************')
    main(test_data_2, part_two=True)
    main(raw_data, part_two=True)
