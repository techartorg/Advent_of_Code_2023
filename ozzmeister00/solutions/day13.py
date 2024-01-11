"""
--- Day 13: Point of Incidence ---

With your help, the hot springs team locates an appropriate spring which 
launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray 
mountains scattered around. After a while, you make your way to a nearby cluster
 of mountains only to discover that the valley between them is completely full 
of large mirrors. Most of the mirrors seem to be aligned in a consistent way; 
perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have 
fallen from the large metal frames keeping them in place. The mirrors are 
extremely flat and shiny, and many of the fallen mirrors have lodged into the 
ash at strange angles. Because the terrain is all one color, it's hard to tell 
where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk 
(your puzzle input); perhaps by carefully analyzing these patterns, you can 
figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection 
across either a horizontal line between two rows or across a vertical line 
between two columns.

In the first pattern, the reflection is across a vertical line between two 
columns; arrows on each of the two columns point at the line between the 
columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
In this pattern, the line of reflection is the vertical line between columns 5 
and 6. Because the vertical line is not perfectly in the middle of the pattern, 
part of the pattern (column 1) has nowhere to reflect onto and can be ignored; 
every other column has a reflected column within the pattern and must match 
exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 
matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 
would reflect with a hypothetical row 8, but since that's not in the pattern, 
row 1 doesn't need to match anything. The remaining rows match: row 2 matches 
row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of 
each vertical line of reflection; to that, also add 100 multiplied by the number
 of rows above each horizontal line of reflection. In the above example, the 
first pattern's vertical line has 5 columns to its left and the second pattern's
 horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number 
do you get after summarizing all of your notes?
"""
import solver.runner
import solver.solver
import utils.math


class ReflectionOrientation(object):
    HORIZONTAL = 0
    VERTICAL = 1



class Reflection(object):
    def __init__(self, index: int, orientation: int):
        self.index = index
        self.orientation = orientation

    def __eq__(self, other) -> bool:
        if isinstance(other, Reflection):
            return self.index == other.index and self.orientation == other.orientation
        
        return super(Reflection, self).__eq__(other)

    def __repr__(self) -> str:
        return f"Reflection({self.index}, {self.orientation})"



class TerrainMap(utils.math.Grid2D):
    def __init__(self, inData: str):
        lines = inData.splitlines()
        width = len(lines[0])
        super(TerrainMap, self).__init__(width, data=inData.replace('\n',''))

    def findReflection(self) -> Reflection:
        """
        Find the index of the reflection (where two rows or columns are equal)
        and return a Reflection object with the index and orientation
        of the reflection in this terrain map
        """
        def searchForReflection(lines: list[str]) -> int:
            """
            Handles looping through an input set of lines
            regardless of orientation and returns the
            index of reflection, if any
            """
            i = 0
            indexOfReflection = -1
            # first find the spot where one line and the next are 
            # equal to each other
            while i < len(lines) -1 and indexOfReflection < 0:
                if lines[i] == lines[i+1]:
                    indexOfReflection = i
                
                i += 1

            # then, if one was found, we next need to search outward from 
            # that point to ensure the lines on either side are ALSO 
            # equivalent to each other
            if indexOfReflection > 0:
                # start with the lines on either side of the reflection
                i = indexOfReflection - 1
                j = indexOfReflection + 2

                validReflection = True
                while i > -1 and validReflection and j < len(lines):
                    low = lines[i]
                    high = lines[j]

                    print(low)
                    print(high)

                    # if the lines aren't equal, bail out
                    if low != high:
                        print("fail")
                        validReflection = False
                    
                    i -= 1 
                    j += 1
                
                if validReflection:
                    return indexOfReflection

            return -1

        # first search for a horizontal reflection
        index = searchForReflection([row for i, row in self.enumerateRows()])
        
        # if we found one, return it
        if index > -1:
            return Reflection(index + 1, ReflectionOrientation.HORIZONTAL)

        # otherwise, look for a vertical reflection
        index = searchForReflection([column for i, column in self.enumerateColumns()])

        # if we DIDN'T find one, something went wrong
        if index < 0:
            raise Exception(f"Couldn't find reflection in map:\n {str(self)}")

        return Reflection(index + 1, ReflectionOrientation.VERTICAL)


class Solver(solver.solver.ProblemSolver):
    def __init__(self, rawData=None):
        super(Solver, self).__init__(13, rawData=rawData)

    def ProcessInput(self) -> list[TerrainMap]:
        """
        :returns: a list of TerrainMaps for the input raw data
        """
        maps = []

        # run through all the lines in the input data
        currentMap = ''
        for line in self.rawData.splitlines():
            # if the line contains data, add it to the current map
            if line.strip():
                currentMap += line + '\n'
            # if we hit a blank line, create a new TerrainMap with 
            # all the data we currently have, and reset the currentMap
            else:
                maps.append(TerrainMap(currentMap))
                currentMap = ''

        # when we're done, if there's any data remaining, treat that as
        # another map to parse
        if currentMap:
            maps.append(TerrainMap(currentMap))

        return maps

    def SolvePartOne(self) -> int:
        """
        Loop through all the terrain maps we've generated
         and find the point of reflection.

         If the reflection is vertical, sum the indexes
         If the reflection is horizontal, multiply the index by 100 

         and sum those reflection values

        :return int: the result
        """
        result = 0

        reflections = [i.findReflection() for i in self.processed]

        for r in reflections:
            if r.orientation == ReflectionOrientation.VERTICAL:
                result += r.index
            elif r.orientation == ReflectionOrientation.HORIZONTAL:
                result += (r.index * 100)
            else:
                raise ValueError(f"Invalid orientation {r.orientation} for reflection {r}")

        return result


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
