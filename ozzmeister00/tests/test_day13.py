from unittest import TestCase, SkipTest

import solutions.day13


TEST_MAP_A = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.'''


TEST_MAP_B = '''#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

TEST_MAP_C = '''##.###...#.##
##.###...#.##
###.#####..##
##....#.##.##
#....#.#.####
.#....###....
#....#...####
.##.##.####..
..#.##.###.#.'''

TEST_DATA = TEST_MAP_A + '\n\n' + TEST_MAP_B


class TestTerrainMap(TestCase):
    def test_vertical_reflection(self):
        testMapA = solutions.day13.TerrainMap(TEST_MAP_A)
        expected = solutions.day13.Reflection(5, solutions.day13.ReflectionOrientation.VERTICAL)
        self.assertEqual(expected, testMapA.findReflection())

    def test_horizontal_reflection(self):
        testMapB = solutions.day13.TerrainMap(TEST_MAP_B)
        expected = solutions.day13.Reflection(4, solutions.day13.ReflectionOrientation.HORIZONTAL)
        self.assertEqual(expected, testMapB.findReflection())

    def test_early_reflection(self):
        testMap = solutions.day13.TerrainMap(TEST_MAP_C)
        expected = solutions.day13.Reflection(1, solutions.day13.ReflectionOrientation.HORIZONTAL)
        self.assertEqual(expected, testMap.findReflection())


class TestDay13(TestCase):
    def test_part01(self):
        try:
            expected = 405
            solver = solutions.day13.Solver(rawData=TEST_DATA)
            self.assertEqual(expected, solver.SolvePartOne())
        except NotImplementedError:
            self.skipTest("Not Implemented")

    def test_part02(self):
        try:
            expected = -1
            solver = solutions.day13.Solver(rawData=TEST_DATA)
            self.assertEqual(expected, solver.SolvePartTwo())
        except NotImplementedError:
            self.skipTest("Not Implemented")
