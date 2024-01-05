import time
from unittest import TestCase, SkipTest

import solutions.day12


class TestSpringDataEntry(TestCase):
    def test_class(self):
        validData = '#.#.### 1,1,3'
        validEntry = solutions.day12.SpringDataEntry(validData)
        self.assertTrue(validEntry.isValidConfiguration(validData.split(' ')[0]))

        buildConfigurationsTestData = '??# 1,1'
        buildConfigurationsTest = solutions.day12.SpringDataEntry(buildConfigurationsTestData)
        configurations = buildConfigurationsTest.buildConfigurationsSmarter()
        self.assertEqual(4, len(configurations))

        shorterTestData = '.??..??...?##. 1,1,3'
        shorterTests = solutions.day12.SpringDataEntry(shorterTestData)
        configurations = shorterTestData.buildConfigurationsSmarter()
        self.assertEqual(4, len([i for i in configurations if shorterTests.isValidConf]))
        

        self.assertEqual(1, len(buildConfigurationsTest.getValidConfigurations()))

    def test_ten(self):
        self.skipTest(" Not yet")
        tenConfigurationsData = '?###???????? 3,2,1'
        tenConfigurations = solutions.day12.SpringDataEntry(tenConfigurationsData)
        self.assertEqual(10, len(tenConfigurations.getValidConfigurations()))

    def test_unfolding(self):
        initialTestData = '.# 1'
        initialTest = solutions.day12.SpringDataEntry(initialTestData, unfold=True)
        self.assertEqual(5, len(initialTest.inactiveSprings))
        self.assertEqual(14, len(initialTest.data))


class TestDay12(TestCase):
    TEST_DATA = '''???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1'''
    def test_part01(self):
        expected = 21
        solver = solutions.day12.Solver(rawData=TestDay12.TEST_DATA)
        self.assertEqual(expected, solver.SolvePartOne())

    def test_part02(self):
        try:
            expected = 525152
            solver = solutions.day12.Solver(rawData=TestDay12.TEST_DATA)
            self.assertEqual(expected, solver.SolvePartTwo())
        except NotImplementedError:
            self.skipTest("Not Implemented")