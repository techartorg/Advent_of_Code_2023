from unittest import TestCase, SkipTest

import solutions.day11
import utils.math

TEST_DATA = '...#......\n.......#..\n#.........\n..........\n......#...\n.#........\n.........#\n..........\n.......#..\n#...#.....'

raise SkipTest("Day11")

class TestStarMap(TestCase):
    def setUp(self):
        self.starMap = solutions.day11.StarMap(TEST_DATA)

    def test_expansion(self):
        """
        Make sure that the StarMap properly expands when instantiated from the test data
        """
        self.assertEqual(13, self.v.width)
        self.assertEqual(12, self.starMap.height)

    def test_galaxyID(self):
        """
        Make sure that the StarMap properly assigns the expected ID numbers to each of the
        galaxies in the test data
        """
        coord = utils.math.Int2(4, 0)
        self.assertEqual(coord, self.starMap.galaxies[1])

    def test_distance(self):
        """
        Make sure that we're getting the expected distances between pairs of galaxys based
        on their galaxy IDs
        """
        pairs = [((1, 7), 15),
                 ((3, 6), 17),
                 ((8, 9), 5),
                 ((5, 9), 9)]

        for start, end, distance in pairs:
            self.assertEqual(distance, self.galaxy.getDistance(start, end))


class TestDay11(TestCase):
    def test_part01(self):
        solver = solutions.day11.Solver(rawData=TEST_DATA)
        self.assertEqual(374, solver.SolvePartOne())

    def test_part02(self):
        self.skipTest("Not Implemented")
