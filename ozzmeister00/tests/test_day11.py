import itertools
from unittest import TestCase, SkipTest

import solutions.day11
import utils.math


TEST_DATA = '...#......\n.......#..\n#.........\n..........\n......#...\n.#........\n.........#\n..........\n.......#..\n#...#.....'


class TestStarMap(TestCase):
    def setUp(self):
        self.starMap = solutions.day11.StarMap(TEST_DATA)

    def test_expansion(self):
        """
        Make sure that the StarMap properly expands when instantiated from the test data
        """
        self.assertEqual(13, self.starMap.width)
        self.assertEqual(12, self.starMap.height)

    def test_galaxyID(self):
        """
        Make sure that the StarMap properly assigns the expected ID numbers to each of the
        galaxies in the test data
        """
        coord = utils.math.Int2(4, 0)
        self.assertEqual(coord, self.starMap.galaxies[0])

    def test_distance(self):
        """
        Make sure that we're getting the expected distances between pairs of galaxys based
        on their galaxy IDs
        """
        pairs = [((0, 6), 15),
                 ((2, 5), 17),
                 ((7, 8), 5),
                 ((4, 8), 9)]

        for indexes, distance in pairs:
            start, end = indexes
            self.assertEqual(distance, self.starMap.getDistanceBetweenGalaxies(start, end))




class TestDay11(TestCase):
    def test_combinations(self):
        solver = solutions.day11.Solver(rawData=TEST_DATA)
        combinations = list(itertools.combinations(solver.processed.galaxies, 2))
        self.assertEqual(36, len(combinations))


    def test_part01(self):
        solver = solutions.day11.Solver(rawData=TEST_DATA)
        self.assertEqual(374, solver.SolvePartOne())

    def test_part02(self):
        self.skipTest("Not Implemented")
