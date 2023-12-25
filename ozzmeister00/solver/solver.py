"""
Stores our problem-solver class
"""

import os

from utils import constants


class ProblemSolver(object):
    """
    Common class for solving both test and actual data for a given day.

    To test your algorithms, instantiate this class with the rawData kwarg
    otherwise, it will attempt to load real input from the dayXX.txt text file stored in
    the inputData folder
    """
    def __init__(self, day, rawData=None):
        """
        Loads the input or raw data for the given day

        :param int day: which day we're meant to solve
        :param str rawData: the raw data read from text or manually entered for test cases
        """
        self.day = day

        # pull in raw data, and if none is provided, pull the data from the input file
        self.rawData = rawData
        if not self.rawData:
            self.rawData = self.loadDataFromFile(self.makeDayFilePath())

        # process the input from the day through rawData
        self.processed = self.ProcessInput()

        # init these for later access
        self.partOneResult = None
        self.partTwoResult = None

    def makeDayFileName(self):
        """

        :return str:
        """
        return f'day{str(self.day).zfill(2)}'

    def makeDayFilePath(self):
        """

        :param bool isTest:
        :return str: the full file path to the input data for the day
        """
        fileName = self.makeDayFileName() + '.txt'
        return os.path.join(constants.getInputsFolder(), fileName)

    @staticmethod
    def loadDataFromFile(filePath):
        """

        :param str filePath: full path to the file containing the data
        :return str: raw data from the file
        """
        rawData = ''
        # load in the file's data
        if os.path.exists(filePath):
            with open(filePath, 'r') as fh:
                rawData = fh.read()
        else:
            raise FileNotFoundError("Couldn't find the input file {}".format(filePath))

        return rawData

    def ProcessInput(self):
        """
        To be implemented by each day's class to process data into a helpful format
        for later handling

        :returns: Processed Input
        """
        raise NotImplementedError()

    def SolvePartOne(self):
        """
        Method to be implemented to solve for part one

        :returns: The solution for part one
        """
        raise NotImplementedError()

    def SolvePartTwo(self):
        """
        Method to be implemented to solve for part two

        :returns: The solution for part two
        """
        raise NotImplementedError()

    def Run(self):
        """
        Solve both parts 1 and 2 with the input data, and print it out
        """
        self.processed = self.ProcessInput()
        try:
            self.partOneResult = self.SolvePartOne()
            print('Part 1 Result: ', self.partOneResult)
            self.partTwoResult = self.SolvePartTwo()
            print('Part 2 Result: ', self.partTwoResult)
        except NotImplementedError:
            print("Solving not complete due to some parts not being implemented properly")
