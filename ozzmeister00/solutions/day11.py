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

--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher 
initially estimated.

Now, instead of the expansion you did before, make each empty row or column one 
million times larger. That is, each empty row should be replaced with 1000000 
empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, 
the sum of the shortest paths between every pair of galaxies would be 1030. If 
each empty row or column were merely 100 times larger, the sum of the shortest 
paths between every pair of galaxies would be 8410. However, your universe will 
need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new
 rules, then find the length of the shortest path between every pair of 
galaxies. What is the sum of these lengths?
"""

import itertools

import solver.runner
import solver.solver
import utils.math


class StarMap(utils.math.Grid2D):
    BLANK = '.'
    EXPANDED = '~'
    EXPANSION_THRESHOLD = 99

    def __init__(self, inData: str, expansion: int = 2):
        # initialize the Grid2D
        lines = inData.splitlines()
        width = len(lines[0])

        self.expansion = expansion

        super(StarMap, self).__init__(width, data=''.join(lines))

        # then loop through and find all the rows and columns that contain no galaxies and expand them
        self.expandColumns()
        self.expandRows()

        # then go a head and store off the coordinates of all the galaxies
        self.galaxies = self.findCoords('#')

    def expandRows(self):
        """
        Based on the expansion value of the star map, either manually expand the rows
        or mark the rows with a different character so we can hit-test expansion instead
        """

        y = 0
        while y < self.height:
            if all([i == StarMap.BLANK or i == StarMap.EXPANDED for i in self.getRow(y)]):
                if self.expansion < StarMap.EXPANSION_THRESHOLD:
                    for i in range(1, self.expansion):
                        self.insertRow(y, '.' * self.width)
                        y += 1
                else:
                    for x in range(self.width):
                        self[utils.math.Int2(x, y)] = StarMap.EXPANDED
            y += 1

    def expandColumns(self):
        """
        Based on the expansion value of the star map, either manually expand the columns
        or mark the columns with a different character so we can hit-test expansion instead
        """
        x = 0
        while x < self.width:
            if all([i == StarMap.BLANK or i == StarMap.EXPANDED for i in self.getColumn(x)]):
                if self.expansion < StarMap.EXPANSION_THRESHOLD:
                    for i in range(1, self.expansion):
                        self.insertColumn(x, '.' * self.height)
                        x += 1
                else:
                    for y in range(self.height):
                        self[utils.math.Int2(x, y)] = StarMap.EXPANDED
            x += 1

    def getDistanceBetweenGalaxies(self, a: int, b: int) -> int:
        """

        :param a: the index of the galaxy to start from
        :param b: the index of the galaxy to end at
        :return: the orthogonal distance between the two galaxies
        """
        length = utils.math.Line2D(self.galaxies[a], self.galaxies[b]).length

        # if we're below the expansion threshold, then we know we can just return the length
        if self.expansion < StarMap.EXPANSION_THRESHOLD:
            return length
        # however if we're above it, we need to add the expansion value for each expanded cell
        # along the path from A to B
        else:
            aCoord = self.galaxies[a]
            bCoord = self.galaxies[b]

            # get coords from the rows and columns we pass through to reach the target
            # ignoring the first point, because we know that will be the starting galaxy
            horizontal = self[aCoord:utils.math.Int2(bCoord.x, aCoord.y)][1:]
            vertical = self[aCoord:utils.math.Int2(aCoord.x, bCoord.y)][1:]

            path = horizontal + vertical
            distances = [self.expansion if i == StarMap.EXPANDED else 1 for i in path]
            return sum(distances)


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
        Process all the combinations of galaxies, and return the sum of the distances
        between all those combinations
        :return int: the result
        """
        result = 0
        combinations = itertools.combinations(range(len(self.processed.galaxies)), 2)
        for a, b in combinations:
            result += self.processed.getDistanceBetweenGalaxies(a, b)

        return result

    def SolvePartTwo(self, expansion: int = 1000000):
        """
        :param expansion: How much expansion to use when processing the star map
        :return int: the sum of the distances between all the pairs of galaxies
        """
        result = 0

        expandedStarMap = StarMap(self.rawData, expansion=expansion)

        combinations = itertools.combinations(range(len(expandedStarMap.galaxies)), 2)
        for a, b in combinations:
            result += expandedStarMap.getDistanceBetweenGalaxies(a, b)

        return result


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
