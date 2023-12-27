import os
import sys

sys.path.append(os.path.dirname(__file__))

import utils.math


polygonTestA = utils.math.Line2D(utils.math.Int2(2, 2),
                                    utils.math.Int2(6, 2))
polygonTestB = utils.math.Line2D(utils.math.Int2(5, 5),
                                    utils.math.Int2(5, 0))

grid = utils.math.Grid2D(7, data='.'*(7*7))

print(polygonTestA.start)

def draw(line, grid, char):
    if line.start.x == line.end.x:
        print(f"same column, {line.start.x}")
        step = 1 if line.start.y < line.end.y else -1
        for y in range(line.start.y, line.end.y, step):
            print(line.start.x, y)
            grid[utils.math.Int2(line.start.x, y)] = char
    elif line.start.y == line.end.y:
        print("Same row")
        for x in range(line.start.x, line.end.x + 1):
            print(x, line.start.y)
            grid[utils.math.Int2(x, line.start.y)] = char
        

    return grid

grid = draw(polygonTestA, grid, 'A')
grid = draw(polygonTestB, grid, 'B')

print(grid)

print(polygonTestA.intersects(polygonTestB))
print(polygonTestB.intersects(polygonTestA))