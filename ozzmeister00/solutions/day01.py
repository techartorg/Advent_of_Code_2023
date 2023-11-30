"""

"""

from utils.solver import ProblemSolver
import utils.math


class Day01Solver(ProblemSolver):
    def __init__(self):
        super(Day01Solver, self).__init__(1)

        self.testDataAnswersPartOne = []
        #self.testDataAnswersPartTwo = [24000]

    def ProcessInput(self, data=None):
        """

        :param string data:
        :returns: the processed results of the day's challenge
        """
        if not data:
            data = self.rawData

        processed = data

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list data:
        :returns:
        """
        if not data:
            data = self.processed

        return data


if __name__ == '__main__':
    day01 = Day01Solver()
    day01.Run()
