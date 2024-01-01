from unittest import TestCase, SkipTest

import solutions.day12


class TestSpringDataEntry(TestCase):
    def test_class(self):
        validData = '#.#.### 1,1,3'
        validEntry = solutions.day12.SpringDataEntry(validData)
        self.assertTrue(validEntry.isValidConfiguration(validData.split(' ')[0]))

        buildConfigurationsTestData = '??# 1,1'
        buildConfigurationsTest = solutions.day12.SpringDataEntry(buildConfigurationsTestData)
        configurations = buildConfigurationsTest.buildAllConfigurations()
        self.assertEqual(4, len(configurations))

        self.assertEqual(1, len(buildConfigurationsTest.getValidConfigurations()))

        tenConfigurationsData = '?###???????? 3,2,1'
        tenConfigurations = solutions.day12.SpringDataEntry(tenConfigurationsData)
        self.assertEqual(10, len(tenConfigurations.getValidConfigurations()))


class TestDay12(TestCase):
    def test_part01(self):
        testData = '''???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1'''
        expected = 21
        solver = solutions.day12.Solver(rawData=testData)
        self.assertEqual(expected, solver.SolvePartOne())

    def test_part02(self):
        self.skipTest("Not Implemented")