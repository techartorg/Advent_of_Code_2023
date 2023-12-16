"""
"""


from utils.solver import ProblemSolver


class Solver(ProblemSolver):
    def __init__(self):
        super(Solver, self).__init__(4)

        self.testDataAnswersPartOne = []

    def ProcessInput(self, data=None):
        """

        :param str data: the raw input data

        :returns: 
        """
        if not data:
            data = self.rawData
        
        processed = None

        return processed 

    def SolvePartOne(self, data=None):
        """
        
        :param list[Something] data: 

        :return int: the result
        """
        if not data:
            data = self.processed

        result = 0

        return result