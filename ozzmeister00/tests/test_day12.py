from unittest import TestCase, SkipTest

import solutions.day12

class TestDay12(TestCase):
    def test_part01(self):
        testData = '''???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1'''
        expected = 21
        solver = solutions.day12.Solver(rawData=testData)
        self.assertEqual(expected, solver.SolvePartOne())()

    def test_part02(self):
        self.skipTest("Not Implemented")