"""
--- Day 11: Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an 
observatory. The Elf within turns out to be a researcher studying cosmic 
expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for
 this research project. However, he confirms that the hot springs are the next-
closest area likely to have people; he'll even take you straight there once he's
 done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single
 giant image (your puzzle input). The image includes empty space (.) and 
galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest 
path between every pair of galaxies. However, there's a catch: the universe 
expanded in the time it took the light from those galaxies to reach the 
observatory.

Due to something involving gravitational effects, only some space expands. In 
fact, the result is that any rows or columns that contain no galaxies should all
 actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion 
therefore looks like this:

....#........   ....#........
.........#...   .........#...
#............   #............
.............   .............
.............   .............
........#....   ........#....
.#...........   .#...........
............#   ............#
.............   .............
.............   .............
.........#...   .........#...
#....#.......   #....#.......

Equipped with this expanded universe, the shortest path between every pair of 
galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within
 the pair doesn't matter. For each pair, find any shortest path between the two 
galaxies using only steps that move up, down, left, or right exactly one . or # 
at a time. (The shortest path between two galaxies is allowed to pass through 
another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from 
galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 
itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path 
between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every 
pair of galaxies. What is the sum of these lengths?


"""
import itertools

import solver.runner
import solver.solver
import utils.math


class StarMap(utils.math.Grid2D):
    def __init__(self, inData: str):
        # initialize the Grid2D
        lines = inData.splitlines()
        width = len(lines[0])

        super(StarMap, self).__init__(width, data=''.join(lines))

        # then loop through and find all the rows and columns that contain no galaxies and expand them
        x = 0
        while x < self.width:
            if all([i == '.' for i in self.getColumn(x)]):
                self.insertColumn(x, '.' * self.height)
                # after inserting, make sure we skip ahead so we don't
                # end up in an infinite loop
                x += 1
            x += 1

        y = 0
        while y < self.height:
            if all([i == '.' for i in self.getRow(y)]):
                self.insertRow(y, '.' * self.width)
                y += 1
            y += 1

        # then go a head and store off the coordinates of all the galaxies
        self.galaxies = self.findCoords('#')

    def getDistanceBetweenGalaxies(self, a: int, b: int) -> int:
        """

        :param a: the index of the galaxy to start from
        :param b: the index of the galaxy to end at
        :return: the orthogonal distance between the two galaxies
        """
        length = utils.math.Line2D(self.galaxies[a], self.galaxies[b]).length
        return length


class Solver(solver.solver.ProblemSolver):
    def __init__(self, rawData=None):
        super(Solver, self).__init__(11, rawData=rawData)
        self.processed: StarMap

    def ProcessInput(self) -> StarMap:
        """
        :returns: a star map based on the input data
        """
        return StarMap(self.rawData)

    def SolvePartOne(self) -> int:
        """

        :return int: the result
        """
        result = 0
        combinations = itertools.combinations(range(len(self.processed.galaxies)), 2)
        for a, b in combinations:
            result += self.processed.getDistanceBetweenGalaxies(a, b)

        return result


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
