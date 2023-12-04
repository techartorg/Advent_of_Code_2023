"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take 
you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, 
I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while 
before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can
 figure out which one. If you can add up all the part numbers in the engine schematic, it 
 should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. 
There are lots of numbers and symbols you don't really understand, but apparently any number 
adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. 
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
In this schematic, two numbers are not part numbers because they are not adjacent to a 
symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and 
so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger.
What is the sum of all of the part numbers in the engine schematic?
"""


import sys

from utils.solver import ProblemSolver

import utils.constants
import utils.math 
import utils.string


class PartNumber(int):
    """
    Convenience class for creating and storing a part number and
    the grid coordinates associated with it
    """
    def __new__(cls, number, coords):
        return super(PartNumber, cls).__new__(cls, number)

    def __init__(self, number, coords):
        super(PartNumber, self).__init__()
        self.coords = coords

    def __repr__(self):
        return f'PartNumber({super(PartNumber, self).__repr__()}, {self.coords})'


class Solver(ProblemSolver):
    def __init__(self):
        super(Solver, self).__init__(3)

        self.testDataAnswersPartOne = [4361]

    def ProcessInput(self, data=None):
        """
        :param str data: the engine schematic

        :return utils.math.Grid2D processed: turn the input data into a Grid2D
        """
        if not data:
            data = self.rawData

        width = len(data.splitlines()[0])

        return utils.math.Grid2D(width, data.replace('\n', ''))

    def getPartNumbersFromRow(self, y, row):
        """
        Given a list of single-character strings, parse out all the numbers
        and return the list of PartNumbers

        :param int y: the current row value'
        :param list[str]: the row

        :return list[PartNumber]:
        """
        partNumbers = []

        currentNumber = ''
        startIndex = -1
        endIndex = -1

        # iterate through the row, parsing out numbers by hand
        for i, v in enumerate(row):
            if v.isnumeric():
                if startIndex == -1:
                    startIndex = i 
                currentNumber += v 

            # if it's not a number, but we'd been making a number
            # then we know the number we're constructing is over
            elif startIndex > -1:
                endIndex = i
                # generate the coordinates of the number
                coords = [utils.math.Int2((x, y)) for x in range(startIndex, endIndex)]

                # and add a new PartNumber to the list
                partNumbers.append(PartNumber(currentNumber, coords))

                # then reset our search variables
                startIndex = -1
                endIndex = -1
                currentNumber = ''

        return partNumbers
        

    def SolvePartOne(self, data=None):
        """
        Finds all the part numbers in the input schematic (numbers adjacent to symbols that are not .)
        and returns the sum of those part numbers
        
        :param utils.math.Grid2D data: the engine schematic

        :return int: the sum of all the part numbers in the schematic
        """
        if not data:
            data = self.processed

        result = 0 

        # step one, find all the numbers and their coordinates by scanning
        # through each line in the grid.
        partNumbers = []
        for y, row in data.enumerateRows():
            partNumbers += self.getPartNumbersFromRow(y, row)

        print('\n'.join([str(p) for p in partNumbers[:10]]))

        # then, loop through all the neighbors of the coordinates of the part numbers
        # and if any of those values are symbols, add that part number to the result
        for part in partNumbers:
            i = 0
            while i < len(part.coords):
                j = 0
                neighbors = list(data.enumerateNeighborsBox(part.coords[i], 1))
                while j < len(neighbors):
                    c, v = neighbors[j]
                    if not v.isnumeric() and v != '.':
                        print(f"{part} is adjacent symbol {v} at {c}")
                        result += part
                        i = len(part.coords)
                        j = 9
                    j += 1

                i += 1

        return result


if __name__ == '__main__':
    solver = Solver()
    solver.Run()