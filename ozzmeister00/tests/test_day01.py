from unittest import TestCase

import solutions.day01


class TestDay01(TestCase):
    def test_part01(self):
        expected = 142
        testData = '''1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet'''
        solver = solutions.day01.Solver(rawData=testData)

        self.assertEqual(expected, solver.SolvePartOne())

    def test_part02(self):
        expected = 281
        testData = '''two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen'''
        solver = solutions.day01.Solver(rawData=testData)

        self.assertEqual(expected, solver.SolvePartTwo())
