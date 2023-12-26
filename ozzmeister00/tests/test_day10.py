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

        expectedConnections = [utils.math.Grid2D.East, utils.math.Grid2D.North]
        startCoords = network.findCoords('S')

        self.assertEquals(1, len(startCoords))

        self.assertTrue([all([i in network[startCoords[0]].connectors for i in expectedConnections])])

    def test_traversal(self):
        network = solutions.day10.PipeNetwork(self.testData)
        distances = [0,1,1,-1]

        self.assertEqual(distances, [i.distanceFromStart for i in network])

    def test_mainLoop(self):
        testData = '''S-7\n|.|\nL-J'''.splitlines()
        mainLoopPoints = [utils.math.Int2((0,0)),
                          utils.math.Int2((1,0)),
                          utils.math.Int2((2,0)),
                          utils.math.Int2((0,1)),
                          utils.math.Int2((0,2)),
                          utils.math.Int2((1,2)),
                          utils.math.Int2((2,2)),
                          utils.math.Int2((2,1))]
        network = solutions.day10.PipeNetwork(testData)
        self.assertTrue(all([point in mainLoopPoints for point in network.mainLoopPipes]))
        self.assertEqual([utils.math.Int2((1,1))], network.disconnectedPipes)


class TestDay10(TestCase):
    def test_part01(self):
        testData = [('.....\n.S-7.\n.|.|.\n.L-J.\n.....', 4),
                    ('..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...', 8)]

        for test, expected in testData:
            solver = solutions.day10.Solver(rawData=test)
            self.assertEqual(expected, solver.SolvePartOne())

    def test_part02(self):
        testData = [(1, '''S-7\n|.|\nL-J'''),
                    (10, 'FF7FSF7F7F7F7F7F---7\nL|LJ||||||||||||F--J\nFL-7LJLJ||||||LJL-77\nF--JF--7||LJLJ7F7FJ-\nL---JF-JLJ.||-FJLJJ7\n|F|F-JF---7F7-L7L|7|\n|FFJF7L7F-JF7|JL---7\n7-L-JL7||F7|L7F-7F7|\nL.L7LFJ|||||FJL7||LJ\nL7JLJL-JLJLJL--JLJ.L'),
                    (4, '...........\n.S-------7.\n.|F-----7|.\n.||.....||.\n.||.....||.\n.|L-7.F-J|.\n.|..|.|..|.\n.L--J.L--J.\n...........')]
        try:
            for expected, test in testData:
                solver = solutions.day10.Solver(rawData=test)
                self.assertEqual(expected, solver.SolvePartTwo())
        except NotImplementedError:
            self.skipTest("Not implemented yet")