from unittest import TestCase

import solutions.day10
import utils.math


class TestPipe(TestCase):
    VALID_CHARACTERS = '-L|F7NSJ.'

    def test(self):
        self.assertRaises(ValueError, solutions.day10.Pipe, 'A')
        pipe = solutions.day10.Pipe('-')

        expectedConnectors = [utils.math.Grid2D.West, utils.math.Grid2D.East]
        self.assertTrue(all([i in pipe.connectors for i in expectedConnectors]))


class TestPipeNetwork(TestCase):
    testData = 'S-\n|.'.splitlines()
    def test_SConnectors(self):
        network = solutions.day10.PipeNetwork(self.testData)

        expectedConnections = [utils.math.Grid2D.East, utils.math.Grid2D.South]
        startCoords = network.findCoords('S')

        self.assertEquals(1, len(startCoords))

        self.assertTrue([all([i in network[startCoords[0]].connectors for i in expectedConnections])])

    def test_traversal(self):
        network = solutions.day10.PipeNetwork(self.testData)
        distances = [0,1,1,-1]

        self.assertEqual(distances, [i.distanceFromStart for i in network])


class TestDay10(TestCase):
    def test_part01(self):
        self.skipTest("not ready")
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
