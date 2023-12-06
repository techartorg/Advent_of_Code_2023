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

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life,
you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately,
the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands
 the engineer, holding a phone in one hand and waving with the other. You're going so slowly
  that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any
 * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of
  multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer
 can figure out which gear needs to be replaced.

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
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so
its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490.
(The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of
 the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
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
        self.testDataAnswersPartTwo = [467835]

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

        # iterate through the row, parsing out numbers by hand
        for i, v in enumerate(row):
            if v.isnumeric():
                if startIndex == -1:
                    startIndex = i 
                currentNumber += v

                # if we're at the end of the row, then make a number
                if i >= (len(row) - 1):
                    # generate the coordinates of the number
                    coords = [utils.math.Int2((x, y)) for x in range(startIndex, i+1)]

                    # and add a new PartNumber to the list
                    partNumbers.append(PartNumber(currentNumber, coords))

            # if it's not a number, but we'd been making a number
            # then we know the number we're constructing is over
            elif startIndex > -1:
                # generate the coordinates of the number
                coords = [utils.math.Int2((x, y)) for x in range(startIndex, i)]

                # and add a new PartNumber to the list
                partNumbers.append(PartNumber(currentNumber, coords))

                # then reset our search variables
                startIndex = -1
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
                        result += part
                        i = len(part.coords)
                        j = 9
                    j += 1

                i += 1

        return result

    def SolvePartTwo(self, data=None):
        """
        Finds all the gears in the schematic and return the sum of
        the gear ratios

        Gears = any * symbol adjacent to exactly two parts

        :param utils.math.Grid2D data: the engine schematic

        :return int: the sum of all the gear ratios
        """
        if not data:
            data = self.processed

        result = 0

        # step one, find all the numbers and their coordinates by scanning
        # through each line in the grid.
        partNumbers = []
        for y, row in data.enumerateRows():
            partNumbers += self.getPartNumbersFromRow(y, row)

        # then build a map from 1D coordinates to a part number for efficient searching later
        partMap = {}
        for part in partNumbers:
            for c in part.coords:
                partMap[data.coordsToIndex(c)] = part

        # next, get the locations of all the * in the grid
        gearSymbols = data.findIndexes('*')

        # and loop over all the neighbors of those symbols
        for gear in gearSymbols:
            neighborParts = []

            # and then loop through all the neighbors of those symbols
            for coord, value in data.enumerateNeighborsBox(data.indexToCoords(gear), 1):
                # if we find that a neighbor is contained in the part map,
                # add it to our candidate list of neighbor parts

                if value.isnumeric():
                    index = data.coordsToIndex(coord)
                    # make sure we don't grab the same part twice!
                    if index in partMap:
                        alreadyGrabbed = False
                        for neighborPart in neighborParts:
                            if partMap[neighborPart] == partMap[index]:
                                alreadyGrabbed = True

                        if not alreadyGrabbed:
                            neighborParts.append(index)

            # if we ended up finding exactly two neighbors, we know we're dealing with a gear
            if len(neighborParts) == 2:
                # so add the product of those two part numbers
                result += utils.math.product([partMap[i] for i in neighborParts])
            else:
                partNos = '\n\t'.join([str(partMap[i]) for i in neighborParts])
                print(f'Symbol at {data.indexToCoords(gear)} does not have two adjacent part numbers:\n\t{partNos}')

        return result


if __name__ == '__main__':
    solver = Solver()
    solver.Run()
