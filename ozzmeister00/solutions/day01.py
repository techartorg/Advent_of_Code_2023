"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you
 a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty
stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second
 puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you
("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the
sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a
trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been
amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are
having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific
calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining
 the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""

import sys

import solver.runner
import solver.solver

import utils.constants


class Solver(solver.solver.ProblemSolver):
    def __init__(self, rawData=None):
        super(Solver, self).__init__(1, rawData=rawData)

    def ProcessInput(self):
        """
        Processes the stored raw data into self.processed

        :returns list[str]: The list of calibration lines
        """
        processed = self.rawData.splitlines(keepends=False)

        return processed

    def SolvePartOne(self):
        """
        Parse out numbers from the calibration lines, get the first and last numbers as a single number
        then return the sum of those numbers

        :returns int: the sum of the calibration values
        """
        numbers = []

        for line in self.processed:
            local = []
            for i in line:
                if i.isnumeric():
                    local.append(i)

            assert len(local) > 0, f"{line} apparently doesn't contain any numbers."

            numbers.append(int(local[0] + local[-1]))

        return sum(numbers)

    def SolvePartTwo(self):
        """
        :param list[str] data:

        Parse out numbers from the calibration lines, but this time look for spelled-out numbers instead
        of numeric values

        then return the sum of those numbers

        :returns int: the sum of the calibration values
        """
        numbers = []

        for line in self.processed:
            # build a dict mapping numbers to a list of the indexes at which the numbers are found
            localIndexes = {k: [] for k in range(10)}

            # first, find the spelled out digits in the line, and store their indexes in the dict
            for i, num in enumerate(utils.constants.DIGITS):
                # since we want the first and last numbers, and the same digit could appear in the line more than once
                # do a left find and a right find
                left = line.find(num)
                right = line.rfind(num)

                # if the value is found
                if left > -1:
                    localIndexes[i].append(left)
                    # and if the left and right find returned different results, also add the right find to the list
                    if left != right:
                        localIndexes[i].append(right)

            # then, ALSO find the numerals in the string, and store those indexes in the dict as well
            for i, value in enumerate(line):
                if value.isnumeric():
                    localIndexes[int(value)].append(i)

            # now that we've located all the spelled out and numerals in the line
            # find the lowest-found digit and the highest-found digit
            firstIndex = sys.maxsize
            firstValue = -1
            lastIndex = -1
            lastValue = -1

            for number, indexes in localIndexes.items():
                if indexes:
                    leftIndex = min(indexes)
                    rightIndex = max(indexes)
                    if leftIndex < firstIndex:
                        firstIndex = leftIndex
                        firstValue = number

                    if rightIndex > lastIndex:
                        lastIndex = rightIndex
                        lastValue = number

            assert firstValue > -1, f"Failed to get a good first value for {line}"
            assert lastValue > -1, f"Failed to get a good last value for {line}"

            # then combine those two numbers into a single string to create a two-digit number and convert it to an int
            lineNumber = int(str(firstValue) + str(lastValue))

            numbers.append(lineNumber)

        return sum(numbers)


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
