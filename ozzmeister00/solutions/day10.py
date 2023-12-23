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
"""

import solver.runner
import solver.solver
import utils.math


class Pipe(str):
    CONNECITON_MAPPING = {'|': [utils.math.Grid2D.North, utils.math.Grid2D.South],
                          '-': [utils.math.Grid2D.West, utils.math.Grid2D.East],
                          'L': [utils.math.Grid2D.North, utils.math.Grid2D.East],
                          'J': [utils.math.Grid2D.West, utils.math.Grid2D.North],
                          '7': [utils.math.Grid2D.West, utils.math.Grid2D.South],
                          'F': [utils.math.Grid2D.South, utils.math.Grid2D.East],
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

    def updateConnectors(self, character):
        """
        Update the connectors of the pipe to match the input character

        :param str character: the pipe charcter whose connections we want to match
        """
        self.connectors = Pipe.CONNECITON_MAPPING[character]


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

        opposites = self.orthoNeighbors[::-1]

        sConnectors = []

        for i, direction in enumerate(self.orthoNeighbors):
            localNeighbor = utils.math.Int2(sCoord + direction)
            if self.coordsInBounds(localNeighbor):
                print(localNeighbor, '->', self[localNeighbor].connectors)
                if opposites[i] in self[localNeighbor].connectors:
                    sConnectors.append(opposites[i])

        print(sConnectors)
        self[sCoord].connectors = sConnectors

        # update each pipe with all of its neighbors
        for i, pipe in self.enumerateCoords():
            for connector in self[i].connectors:
                localNeighbor = utils.math.Int2(connector + i)
                if self.coordsInBounds(localNeighbor):
                    self[i].connections.append(localNeighbor)

        # once we've done that, zoop through the connections from the start point and update their 
        # distance from the start point
        self.traversePaths(sCoord, 0)
    
    def traversePaths(self, coord, distanceSoFar):
        """
        For each of the connections in this pipe, traverse all the unvisited connections
        from this point
        """
        self[coord].distanceFromStart = distanceSoFar
        for connection in self[coord].connections:
            if self[connection].distanceFromStart < 0:
                self.traversePaths(connection, distanceSoFar + 1)


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
        result = 0

        return result


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
