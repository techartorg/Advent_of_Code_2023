"""--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to
 the floating metal island. This island is surprisingly cold and there 
definitely aren't any thermals to glide on, so you leave your hang glider 
behind.

You wander around for a while, but you don't find any people or animals. 
However, you do occasionally find signposts labeled "Hot Springs" pointing in a 
seemingly consistent direction; maybe you can find someone at the hot springs 
and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As 
you stop to admire some metal grass, you notice something metallic scurry away 
in your peripheral vision and jump into a big pipe! It didn't look like any 
animal you've ever seen; if you want a better look, you'll need to get ahead of 
it.

Scanning the area, you discover that the entire field you're standing on is 
densely packed with pipes; it was hard to tell at first because they're the same
 metallic silver color as the "ground". You make a quick sketch of all of the 
surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your
 sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that
 contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would 
instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell 
because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This
 sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: 
they're the ones connected to S, pipes those pipes connect to, pipes those pipes
 connect to, and so on. Every pipe in the main loop connects to its two 
neighbors (including S, which will have exactly two pipes connecting to it, and 
which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also 
shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop
 that is farthest from the starting position. Because the animal is in the pipe,
 it doesn't make sense to measure this by direct distance. Instead, you need to 
find the tile that would take the longest number of steps along the loop to 
reach from the starting point - regardless of which way around the loop the 
animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like
 this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it 
take to get from the starting position to the point farthest from the starting 
position?

--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. 
Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, 
you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest 
and southeast (marked I below). The middle . tiles (marked O below) are not in 
the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles
 to count as outside the loop - squeezing between pipes is also allowed! Here, I
 is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop 
(I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the 
loop. Here's another example with many bits of junk pipe lying around that 
aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area 
within the loop. How many tiles are enclosed by the loop?
"""

import solver.runner
import solver.solver
import utils.math


class Pipe(str):
    CONNECITON_MAPPING = {'|': [utils.math.Grid2D.North, utils.math.Grid2D.South],
                          '-': [utils.math.Grid2D.West, utils.math.Grid2D.East],
                           # the north/souths are flipped for the corners because Grid2D puts. 0,0 in the top left, and "North" is actually down
                          'L': [utils.math.Grid2D.South, utils.math.Grid2D.East],
                          'J': [utils.math.Grid2D.West, utils.math.Grid2D.South],
                          '7': [utils.math.Grid2D.West, utils.math.Grid2D.North],
                          'F': [utils.math.Grid2D.North, utils.math.Grid2D.East],
                          '.': (),
                          'S': ()}

    def __new__(cls, character):
        """
        :param str character: which character represents this pipe
        """
        if not character in Pipe.CONNECITON_MAPPING:
            raise ValueError(f"Character {character} is not a valid pipe ID")

        return super().__new__(cls, character)

    def __init__(self, character):
        self.connectors = []  # in which directions this pipe connects
        self.updateConnectors(character)
        self.connections = []  # indexes of the points in the grid to which this pipe connects
        self.distanceFromStart = -1 # init this since we'll need it later and we dont' want to make a whole separate Grid2D for it
        self.isInsideLoop = False
        self.hasBeenVisited = False

    def updateConnectors(self, character):
        """
        Update the connectors of the pipe to match the input character

        :param str character: the pipe charcter whose connections we want to 
match
        """
        self.connectors = Pipe.CONNECITON_MAPPING[character]

    @property
    def isMainLoop(self):
        return self.distanceFromStart > -1


class PipeNetwork(utils.math.Grid2D):
    def __init__(self, rows):
        """
        Create a network of pipes based on an input list of rows of pipes

        :param list[str] rows: all the rows of the pipe network as strings
        """
        width = len(rows[0])
        pipes = [Pipe(i) for i in ''.join(rows)]
        super(PipeNetwork, self).__init__(width, data=pipes)

        # find the S, and figure out what it's connections should be
        startPoints = self.findCoords('S')
        assert len(startPoints) == 1

        sCoord = startPoints[0]
        sConnectors = []
        # loop over all the ortho directions and determine if any of those
        # neighbors connect to the starting pipe
        for i, direction in enumerate(self.orthoNeighbors):
            neighbor = utils.math.Int2(sCoord + direction)
            if self.coordsInBounds(neighbor):
                opposite = direction * -1
                if opposite in self[neighbor].connectors:
                    sConnectors.append(direction)

        assert len(sConnectors) > 0 
        self[sCoord].connectors = sConnectors

        # then, once we've got all the pipes connected
        # update each pipe with all of its neighbors
        # so we don't have to keep adding coordinates to themselves
        for coord, pipe in self.enumerateCoords():
            for connector in self[coord].connectors:
                neighbor = utils.math.Int2(connector + coord)
                if self.coordsInBounds(neighbor):
                    self[coord].connections.append(neighbor)

        assert len(self[sCoord].connections) > 0

        # once we've done that, zoop through the connections from the start point and update their 
        # distance from the start point
        self[sCoord].distanceFromStart = 0

        # then traverse from one direction back around
        self.traversePath(sCoord, self[sCoord].connections[0], 1)
        self.traversePath(sCoord, self[sCoord].connections[1], 1)

    def traversePath(self, prev, next, distanceSoFar):
        """
        For each of the connections in this pipe, traverse all the unvisited connections
        from this point

        :param utils.math.Int2 prev: the place we just were
        :param utils.math.Int2 next: the place where we're going
        """
        # while loop this, because recursion depth has issues if we call this function
        # for each non-visited connection (although this will probably bite me in the butt
        # whenever Eric has a challenge involving intersections)
        while self[next] != 'S':
            # if this point hasn't been visited yet
            if self[next].distanceFromStart < 0:
                self[next].distanceFromStart = distanceSoFar
            # otherwise, pick the minimum of the two distances
            else:
                self[next].distanceFromStart = min(self[next].distanceFromStart, distanceSoFar)

            nextIndex = min(abs(1 - self[next].connections.index(prev)), len(self[next].connections) - 1)

            prev = next
            next = self[prev].connections[nextIndex]

            distanceSoFar += 1

    def distancesAsString(self):
        """
        Return a printable string for the distances of all the points in the grid
        """
        distanceGrid = utils.math.Grid2D(self.width, data=[i.distanceFromStart for i in self])
        return str(distanceGrid)

    @property
    def mainLoopPipes(self):
        """
        Gather up all the pipes that are part of the main loop and return them

        :return list[utils.math.Int2]: coords of all the main loop pipes
        """
        return [coord for coord, pipe in self.enumerateCoords() if pipe.isMainLoop]

    @property
    def disconnectedPipes(self):
        """
        Gather up all the pipes that aren't part of the main loop and return them

        :return list[utils.math.Int2]: coords of all the pipes not on the main loop
        """
        return [coord for coord, pipe in self.enumerateCoords() if not pipe.isMainLoop]


class Solver(solver.solver.ProblemSolver):
    def __init__(self, rawData=None):
        super(Solver, self).__init__(10, rawData=rawData)

    def ProcessInput(self):
        """
        Take the input and turn it into a PipeNetwork
        :returns PipeNetwork:
        """
        return PipeNetwork(list(self.rawData.splitlines()))

    def SolvePartOne(self):
        """
        Given the processed pipe network, determine the furthest point away from the start point
        that anything can be

        :return int: the furthest distance away from the start that any pipe could be
        """
        return max([i.distanceFromStart for i in self.processed])

    def SolvePartTwo(self):
        """
        Given the processed pipe network, determine the number of pipes that
        are fully contained by the pipe network

        :return int: the number of contained tiles
        """
        def floodFill(coordinate, group):
            group.append(coordinate)

            for coord, pipe in self.processed.enumerateNeighborsBox(coordinate, distance=1):
                # bail out on the main loop
                if coord not in group and not pipe.isMainLoop:
                    group = floodFill(coord, group) 

            return group

        # bound our search within the the footprint of the pipe network
        # there's no need to parse tiles outside that
        networkBounds = utils.math.BoundingBox2D.fromPoints(self.processed.mainLoopPipes)

        # find the candidate coordinates within the bounding box, and only
        # consider the pipes that aren't prt of the main loop
        candidates = [coord for coord, pipe in self.processed.enumerateBoundingBox(networkBounds) if not pipe.isMainLoop]

        # break up the candidates into group by floodfilling out from 
        # the first available candidate, winnowing down the candidates 
        # until there aren't any more candidates
        groups = []

        while candidates:
            # floodfill a group from the first coordinate in our list of candidates
            group = []
            group = floodFill(candidates[0], group)

            candidates = [coord for coord in candidates if coord not in group]

            groups.append(group)

        # then, check the groups to find the groups that are connected to the edge
        interiorPoints = []

        for group in groups:
            i = 0
            while i < len(group) and not self.processed.coordOnEdge(group[i]):
                i += 1

            # if we got to the end of that and we didn't bail out early
            # then we know that that group is the interior group
            if i == len(group):
                interiorPoints += group

        assert len(interiorPoints) > 0

        return len(interiorPoints)


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
