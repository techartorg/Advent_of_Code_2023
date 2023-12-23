from unittest import TestCase

import solutions.day10


class TestDay10(TestCase):
    def test_part01(self):
        expected = 142
        testData = '''-L|F7\n7S-7|\nL|7||\n-L-J|\nL|-JF'''
        solver = solutions.day10.Solver(rawData=testData)

        self.assertEqual(expected, solver.SolvePartOne())

    def test_part02(self):
        try:
            expected = None
            testData = ''
            solver = solutions.day10.Solver(rawData=testData)

            self.assertEqual(expected, solver.SolvePartTwo())
        except NotImplementedError:
            self.skipTest("Part Two Not Yet Implemented")
