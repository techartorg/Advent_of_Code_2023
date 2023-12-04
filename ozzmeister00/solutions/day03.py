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

class PartNumber(int):
    """
    Convenience class for creating and storing a part number and
    the grid coordinates associated with it
    """
    def __init__(number, coords):
        """

        :param str number: the string representation of the number
        :param list[utils.math.Int2] coords: the coordinates occupied by the part number
        """
        super(PartNumber, self).__init__(number)
        self.coords = coords


class Solver(ProblemSolver):
    def __init__(self):
        super(ProblemSolver, self).__init__(3)

        self.testDataAnswersPartOne = [4361]

    def ProcessInput(data=None):
        """
        :param str data: the engine schematic

        :return utils.math.Grid2D processed: turn the input data into a Grid2D
        """
        if not data:
            data = self.rawData

        width = data.splintlines()[0]

        return utils.math.Grid2D(width, data.replace('\n', ''))

    def getPartNumbersFromRow(self, y, row):
        """
        Given a list of single-character strings, parse out all the numbers
        and return the list of PartNumbers

        :param int y: the current row value'
        :param list[str]: the row

        :return list[PartNumber]:
        """

        

        # put the row back into a single string
        # we'll need this later to get the coordinates for the numbers
        combined = ''.join(row)

        # so we can split it out on periods and look for numbers
        for item in combined.split('.'): 


        partNumbers = []

        return partNumbers
        

    def SolvePartOne(data=None):
        """
        Finds all the part numbers in the input schematic (numbers adjacent to symbols that are not .)
        and returns the sum of those part numbers
        
        :param utils.math.Grid2D data: the engine schematic

        :return int: the sum of all the part numbers in the schematic
        """
        if not data:
            data = self.processed

        result = 0 

        # finding all the numbers and then locating symbols on their periphery
        # is likely going to be easier than finding all the symbols and 
        # trying to resolve the adjacent numbers.

        # step one, find all the numbers and their coordinates by scanning
        # through each line in the grid. As long as the next character is a number, 
        # then we're still in the same number.
        
        partNumbers = []




        return result


if __name__ == '__main__':
    solver = Solver()
    solver.Run()