"""
Common maths functions and datatypes for solving Advent of Code problems
"""
from __future__ import annotations


import math
import functools
import operator
from typing import Any, Iterable


def add(a, b=None):
    """
    Adds two numbers together, if a second number is not supplied, the number will be added to itself
    :param a:
    :param b:
    :return:
    """
    if not b:
        b = a
    return a + b


def mul(a, b=None):
    """
    Multiplies two numbers together, if a second number is not supplied, the number will be added to itself
    :param a:
    :param b:
    :return:
    """
    if not b:
        b = a
    return a * b


def saturate(value):
    """
    Saturates a value, so it is only ever between 0 and 1

    :param float value: the value to saturate

    :return float: the value, but clamped between 0 and 1
    """
    return clamp(value, 0.0, 1.0)


def clamp(value, minValue, maxValue):
    """
    Returns a value that is no less than the min value, and no more than the max value

    :param float value: the value to clamp
    :param float minValue: the minimum value to return
    :param float maxValue: the maximum value to return

    :return float: the clamped value
    """
    return max(minValue, min(value, maxValue))


def product(iterable):
    """
    Returns the product of an iterable of numbers
    :param list iterable: eg [1, 2, 3, 4, 5]
    :return float: the product of all items in the iterable multiplied together
    """
    return functools.reduce(operator.mul, iterable, 1)


class TwoD(list):
    """
    A TwoD object to make it easier to access and multiply 2-length lists of numbers
    """
    defaultClass = None

    def __init__(self, *args):
        """
        :param iterable inV: two-length iterable of class defaultClass
        :param defaultClass: which datatype class to use to instantiate the array
        """
        # set up a default input value to instatiate a float 2 to 0,0 automatically
        # because we can't put a [0,0] in the kwargs otherwise it'll be the same
        # for every instance and that's no bueno
        if not args:
            args = [self.defaultClass(), self.defaultClass()]

        # convert our inputData to a list of the correct class, if one is defined, and the input values
        # aren't already of the correct type
        elif self.defaultClass:
            if not isinstance(args[0], self.defaultClass):
                args = [self.defaultClass(v) for v in args]

        super(TwoD, self).__init__(args)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)
        else:
            return self.__class__(self.x + other, self.y + other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x - other.x, self.y - other.y)
        else:
            return self.__class__(self.x - other, self.y - other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x * other.x, self.y * other.y)
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__(self.x * other, self.y * other)

    def __imul__(self, other):
        return self.__mul__(other)

    def _div(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x / other.x, self.y / other.y)
        if isinstance(other, int) or isinstance(other, float):
            return self.__class__(self.x / other, self.y / other)

    def __truediv__(self, other):
        return self._div(other)

    def __itruediv__(self, other):
        return self._div(other)

    def __divmod__(self, other):
        return self._div(other)

    def __idiv__(self, other):
        return self._div(other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.x == other.x and self.y == other.y:
                return True

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def x(self):
        """
        Access the first, X value of the list
        :return float:
        """
        return self[0]

    @x.setter
    def x(self, v):
        self[0] = v

    @property
    def y(self):
        """
        The second, Y value of the list
        :return float:
        """
        return self[1]

    @y.setter
    def y(self, v):
        self[1] = v


class Number2(TwoD):
    """
    Wrapper around numerical two-d classes with common methods shared between them
    """

    def distance(self, other):
        """
        :param Number2 other: the other point to which we want the distance

        :return float: the distance from this point to the input point
        """
        if not issubclass(other.__class__, Number2):
            raise ValueError(
                "{} is not a subclass of Number2 and its distance cannot be computed".format(other.__class__))

        return math.sqrt(((other.x - self.x) ** 2) + ((other.y - self.y) ** 2))

    def direction(self, other):
        """

        :param Number2 other: the other point to which we want to determine the direction

        :return Number2: the direction from this point to the other point
        """
        return (other - self).normalize()

    def normalize(self):
        """
        :return Number2: this number, normalized to its length
        """
        return self / self.length()

    def length(self):
        """
        :return float: the distance from 0,0 to this point
        """
        return self.__class__().distance(self)


class Float2(Number2):
    """
    Float-specific alias for TwoD
    """
    defaultClass = float

    def __init__(self, *args):
        super(Float2, self).__init__(*args)


class Int2(Number2):
    """
    Alias for TwoD
    """
    defaultClass = int

    def __init__(self, *args):
        super(Int2, self).__init__(*args)

    def __truediv__(self, other):
        # if an int2 is divided by a float, return the ceil of that division
        if isinstance(other, float):
            x = self.x / other
            y = self.y / other

            x = math.ceil(x) if x > 0 else math.floor(x)
            y = math.ceil(y) if y > 0 else math.floor(y)

            return Int2(x, y)

        return super(Int2, self).__truediv__(other)

    def direction(self, other: Number2):
        """
        Convert the float direction to an integer
        """
        return Int2(*[int(i) for i in super(Int2, self).direction(other)])

    # overload the setters so that they always convert to int
    @TwoD.x.setter
    def x(self, value):
        self[0] = int(value)

    @TwoD.y.setter
    def y(self, value):
        self[1] = int(value)


def dot(a, b):
    """
    :param list a: list of numbers
    :param list b: list of numbers equal in length to the first list
    :return float: dot product of n-length lists of numbers
    """
    if len(a) != len(b):
        raise ValueError("Input lists must be of equal length (got {} and {})".format(len(a), len(b)))

    return sum([x * y for x, y in zip(a, b)])


def getBarycentric(p, a, b, c):
    """
    Get the barycentric coordinates of cartesin point a in
    reference frame abc

    :param Float2 p: test point
    :param Float2 a: point A
    :param Float2 b: point B
    :param Float2 c: point C

    :return list: the UVW coordinate of cartesian point P in reference frame created by points ABC
    """
    v0 = b - a  # Vector BA
    v1 = c - a  # Vector CA
    v2 = p - a  # Vector PA
    d00 = dot(v0, v0)  # dot BA . BA
    d01 = dot(v0, v1)  # dot BA . CA
    d11 = dot(v1, v1)  # dot CA . CA
    d20 = dot(v2, v0)  # dot PA . BA
    d21 = dot(v2, v1)  # dot PA . CA

    denom = (d00 * d11) - (d01 * d01)

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return u, v, w


class BoundingBox2D(object):
    def __init__(self, minPoint, maxPoint):
        super(BoundingBox2D, self).__init__()

        self.min = self.bottomLeft = minPoint
        self.max = self.topRight = maxPoint
        self.width = self.max.x - self.min.x
        self.height = self.max.y - self.min.y
        self.bottomRight = Int2(self.max.x, self.min.y)
        self.topLeft = Int2(self.min.x, self.max.y)

    @staticmethod
    def fromPoints(inPoints):
        """
        Given an input list of points, create a bounding box that encompasses 
        all of those points
        """
        xPoints = [point.x for point in inPoints]
        xMin = min(xPoints)
        xMax = max(xPoints)

        yPoints = [point.y for point in inPoints]
        yMin = min(yPoints)
        yMax = max(yPoints)

        minValue = Int2(xMin, yMin)
        maxValue = Int2(xMax, yMax)
        return BoundingBox2D(minValue, maxValue)

    def pointInside(self, point: Number2) -> bool:
        """
        :param point: the point to test
        :return: if the input point is inside this bounding box
        """
        return self.min.x <= point.x < self.max.x and self.min.y <= point.y < self.max.y

    def overlaps(self, other):
        """
        :param BoundingBox2D other: the other bounding box to check
        :return bool: if the input bounding box overlaps with this one at all
        """
        if not issubclass(type(other), BoundingBox2D):
            raise ValueError(f"BoundingBox2D can only test overlaps with BoundingBox2D, not type {type(other)}")

        if self == other:
            return True

        if (self.min.x <= other.min.x < self.max.x or self.min.x <= other.max.x < self.max.x) and \
                (self.min.y <= other.min.y < self.max.y or self.min.y <= other.max.y < self.max.y):
            return True

        return False

    def __eq__(self, other):
        """
        :param BoundingBox2D other:
        :return bool:
        """
        return self.min == other.min and \
               self.max == other.max


class Line2D(object):
    """
    Represents an integer line
    """

    def __init__(self, start: Number2, end: Number2):
        self.start = start
        self.end = end

    @property
    def length(self) -> int:
        return abs((self.end.x - self.start.x)) + abs((self.end.y - self.start.y))

    @property
    def direction(self) -> Number2:
        return self.start.direction(self.end)

    def intersects(self, other) -> bool:
        """
        Test if an input line intersects with this line 

        via: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

        :param other: the other line to test against
        """

        def onSegment(p, q, r) -> bool:
            if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and \
                    (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
                return True
            return False

        o1 = Polygon2D([self.start, self.end, other.start]).orientation()
        o2 = Polygon2D([self.start, self.end, other.end]).orientation()
        o3 = Polygon2D([other.start, other.end, self.start]).orientation()
        o4 = Polygon2D([other.start, other.end, self.end]).orientation()

        if o1 != o2 and o3 != o4:
            return True

        if o1 == Polygon2D.Orientation.Collinear and onSegment(self.start, self.end, other.start):
            return True
        if o2 == Polygon2D.Orientation.Collinear and onSegment(self.start, other.end, other.start):
            return True
        if o3 == Polygon2D.Orientation.Collinear and onSegment(self.end, self.start, other.end):
            return True
        if o4 == Polygon2D.Orientation.Collinear and onSegment(self.end, other.start, other.end):
            return True

        return False

    def __repr__(self):
        return f"Line2D({self.start}, {self.end})"


class Polygon2D(list):
    class Orientation:
        Collinear = 0
        Clockwise = 1
        CounterClockwise = 2

    """
    Represents an arbitrary polygon
    """

    def __init__(self, args: list[Number2]):
        """
        Given an input list of ordered points, make a polygon
        """
        super(Polygon2D, self).__init__(args)
        self.edges = []
        self._rebuildEdges()

    def _rebuildEdges(self):
        """
        Rebuild the edges of the polygon when new vertexes are added or inserted
        """
        self.edges = []
        for i, coord in enumerate(self):
            index = (i + 1) % len(self)
            self.edges.append(Line2D(coord, self[index]))

    def orientation(self) -> int:
        """
        Using the first three points of this polygon, determine its orientation
        """
        p = self[0]
        q = self[1]
        r = self[2]
        value = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))

        if value > 0:
            return self.Orientation.Clockwise
        elif value < 0:
            return self.Orientation.CounterClockwise
        else:
            return self.Orientation.Collinear

    def getBounds(self) -> BoundingBox2D:
        """
        Get the bounding box of this polygon
        """
        return BoundingBox2D.fromPoints(self)

    def pointInside(self, point: Number2) -> bool:
        """
        Raycast against all the edges of the main loop to see if the given point is inside or outside

        :param point: the point to test
        """
        bounds = self.getBounds()
        if bounds.pointInside(point):
            line = Line2D(point, Number2(bounds.max.x + 1, point.y))
            intersections = 0
            for edge in self.edges:
                if line.intersects(edge):
                    intersections += 1

            return bool(intersections % 2)

        return False

    def append(self, other: Number2):
        """
        Override the list append method to update the edges of the polygon
        """
        super(Polygon2D, self).append(other)
        self._rebuildEdges()

    def insert(self, index: int, other: Number2):
        """
        Override the list insert method to update the edges of the polygon
        """
        super(Polygon2D, self).insert(index, other)
        self._rebuildEdges()


class Grid2D(list):
    North = Up = Int2(0, 1)
    South = Down = Int2(0, -1)
    NorthWest = UpLeft = Int2(-1, 1)
    West = Left = Int2(-1, 0)
    SouthWest = DownLeft = Int2(-1, -1)
    NorthEast = UpRight = Int2(1, 1)
    East = Right = Int2(1, 0)
    SouthEast = DownRight = Int2(1, -1)

    # store these anti-clockwise, so we can potentially do useful stuff with that assumption later
    neighbors = [Right, UpRight, Up, UpLeft, Left, DownLeft, Down, DownRight]
    orthoNeighbors = [Right, Up, Left, Down]
    diagonalNeighbors = [UpRight, UpLeft, DownLeft, DownRight]

    def __init__(self, width, data=None):
        """
        :param int width: how wide is the 2D Grid
        :param iterable data: a 1d iterable with which to instantiate the grid
        """
        super(Grid2D, self).__init__(data)
        self._width = width

    @property
    def width(self):
        """
        Get the width of the Grid2D
        :return int:
        """
        return self._width

    @width.setter
    def width(self, value):
        """
        Changing the width of the Grid2D will necessarily affect its height (since "height" is just a function
        of how many bits of data are in the grid) BUT it won't fill any gaps created by changing the total area
        of the grid. Changing this value should be done with extreme caution

        TODO: find a way to support grid resizing that pads the data out, or removes data based on the change in area
        """
        self._width = value

    @property
    def height(self):
        """
        Get the height of the Grid2D
        Height can't be set, since that's a function of its width and the amount of data that's already in it
        :return int:
        """
        return int(len(self) / self.width)

    def _coordsToIndex(self, coords):
        """
        :param Int2 or int coords: the 2d coordinates to translate to 1d,
                                    will just pass through coords if it's an integer

        :return int: 1d index
        """
        if isinstance(coords, Int2):
            return coords.y * self.width + coords.x

        return coords

    def coordsToIndex(self, coords):
        """
        Exposing the method this way, because I'm not sure why I needed this
        to be internal only
        """
        return self._coordsToIndex(coords)

    def indexToCoords(self, index):
        """
        :param int index: the 1d coordinate in the grid to seek

        :return Int2: the x/y coordinate of the input index
        """
        if isinstance(index, int):
            return Int2(index % self.width, index // self.width)

        return index

    def coordsInBounds(self, coords):
        """
        Returns true if the input coordinates are within the bounds of this grid
        :param Int2 coords: 2d coordinates to check
        :returns bool: if the input coords are in bounds
        """
        # TODO there will come a day when I need to update this so that Grid2D supports non-0 starting coordinates
        # TODO 2023_12_26 maybe I can do that with some kind of stored offset?
        return 0 <= coords.x < self.width and 0 <= coords.y < self.height

    def coordOnEdge(self, coord):
        """
        Return true if the input coordinate is on the edge of the grid

        :param Int2 coord:
        :return bool: if the input coord is on the edge
        """
        return coord.x == 0 or coord.y == 0 or coord.x == self.width - 1 or coord.y == self.height - 1

    def enumerateCoords(self):
        """
        :yield (coords, object): the coord and object for each item in the grid
        """
        for i, obj in enumerate(self):
            yield self.indexToCoords(i), obj

    def enumerateOrthoLocalNeighbors(self, coords):
        """
        Returns a list of tuples of coordinate, value for each valid neighbor
        that is North, South, East, and West of the input coordinate

        :param Int2 coords: the coordinates from which to start
        :yield (coords, object): the next neighbor in the NSEW group around the input coordinate
        """
        for neighbor in Grid2D.orthoNeighbors:
            localNeighbor = coords + neighbor
            if self.coordsInBounds(localNeighbor):
                yield localNeighbor, self[localNeighbor]

    def enumerateNeighborsBox(self, coords, distance):
        """
        Yields all the neighbors in a square pattern that are x distance away from the input coords
        :param Int2 coords: the starting coordinates
        :param int distance: how many points away from the current point to search.
            A distance of 1 will yield up to 8 elements (a box that is 3 x 3)
            A distance of 2 will yield up to 24 elements (a box that is 5 x 5)

        :yields (coords, object): the next neighbor in the box surrounding the input point
        """
        if isinstance(coords, int):
            coords = self.indexToCoords(coords)

        for x in range(coords.x - distance, coords.x + distance + 1):
            for y in range(coords.y - distance, coords.y + distance + 1):
                point = Int2(x, y)
                if self.coordsInBounds(point):
                    yield point, self[point]

    def getRow(self, y: int, reverse: bool = False) -> list[Any]:
        """
        Get all the contents of a given row
        :param y:
        :param reverse: if true, will reverse the results
        :return:
        """
        step = 1 if not reverse else -1
        coords = list(range(self.width))
        return [self[Int2(x, y)] for x in coords[::step]]

    def enumerateRow(self, y, reverse=False):
        """
        Yield the items from left to right in the given row
        :param int y: the row number to extract values from
        :param bool reverse: if True, will instead yield items from right to left
        :return (coords, object): the next item in the input row
        """
        step = 1 if not reverse else -1
        coords = list(range(self.width))
        for x in coords[::step]:
            coord = Int2(x, y)
            yield coord, self[coord]

    def enumerateRows(self, reverse=False):
        """
        Yield all of the rows in the grid as a row number, and a list of items

        :param bool reverse: whether to yield the rows from top to bottom or bottom to top

        :yields int, list[object]:
        """
        step = 1 if not reverse else -1
        for y in list(range(self.height))[::step]:
            yield y, self[Int2(0, y):Int2(self.width - 1, y)]

    def rows(self, reverse=False):
        """
        Yield all the rows in the grid as a list of items

        :yields list[object]:
        """
        raise NotImplementedError("Figure out a way to reuse EnumerateRows")

    def getColumn(self, x: int, reverse: bool = False) -> list[Any]:
        """
        Get all the contents of a given column
        :param x:
        :param reverse: if true, will reverse the results
        :return:
        """
        step = 1 if not reverse else -1
        coords = list(range(self.height))
        return [self[Int2(x, y)] for y in coords[::step]]

    def enumerateColumn(self, x, reverse=False):
        """
        Yield the items from top to bottom in the given column

        :param int x: the column number to extract values from
        :param bool reverse: if True, will instead yield items from bottom to top
        :return (coords, object):the next item in the input column
        """
        step = 1 if not reverse else -1
        coords = list(range(self.height))
        for y in coords[::step]:
            coord = Int2(x, y)
            yield coord, self[coord]

    def enumerateColumns(self, reverse=False):
        """
        Yield all the columns in this grid as lists

        :param bool reverse: if the columns should be yielt from the left to right, or right to left
        '
        :yields (int, list[object]): the current columnn number and a list of items from 0 to 1
        """
        step = 1 if not reverse else -1
        for x in list(range(self.width))[::step]:
            yield x, self[Int2(x, 0):Int2(x, self.height - 1)]

    def columns(self, reverse=False):
        """
        Yield all the columns in the grid as a list of objects

        :param bool reverse: whether to run from left to right or right to left
        """
        raise NotImplementedError("Figure out a way to reuse EnumerateColumns")

    def enumerateBoundingBox(self, bbox):
        """
        Return all the objects within an input bounding box

        :param BoundingBox2D bbox:

        :yields Int2, object: the current coordinate and object at that coordinate
        """
        for y in range(bbox.min.y, bbox.max.y):
            for x in range(bbox.min.x, bbox.max.x):
                point = Int2(x, y)
                yield point, self[point]

    def copy(self):
        """
        Override the built-in copy method so it returns a proper Grid2D

        :returns Grid2D:
        """
        return Grid2D(self.width, data=self)

    def findIndexes(self, inValue):
        """
        Find all the instances of value in the grid and return their 1D coordinates

        :return list[int]: indexes of all the instances of the input value in the grid
        """
        return [index for index, value in enumerate(self) if value == inValue]

    def findCoords(self, value):
        """
        Find all the instances of value in the grid and return their 2D coordinates

        :return list[Int2]: coordinates of all the instances of the input value in the grid
        """
        return [self.indexToCoords(index) for index in self.findIndexes(value)]

    def insertRow(self, y: int, contents: Iterable = None):
        """
        Add a new row to this grid

        :param y: the row you want to insert after
        :param contents: what you want to add to this row
        """
        if not contents:
            contents = [None] * self.width

        for x in range(self.width):
            self.insert(Int2(x, y), contents[x])

    def insertColumn(self, x: int, contents: Iterable = None):
        """

        :param x: the row at which to insert the column
        :param contents: what contents, if any, to insert
        """
        if not contents:
            contents = [None] * self.height

        # when we add to the width, we also need to pad
        # out the array width some junk data which we'll delete later
        self.width += 1

        for i in range(self.height + 1):
            self.append('@')

        # then, now that we've got all the data in its normal coordinates
        # with a little of padding
        for y in range(self.height):
            self.insert(Int2(x, y), contents[y])

        # then, once we're done, we can delete the extra padded data
        del self[self.width * self.height:]

    def insert(self, index: int | Int2, value: Any):
        """
        Override the insert method so we can insert using coordinates
        """
        if isinstance(index, Int2):
            index = self.coordsToIndex(index)

        super(Grid2D, self).insert(index, value)

    def __getitem__(self, coords):
        """
        :param int, Int2 coords: the coordinates of the item to retrieve

        :returns: the item at the input coordinates
        """
        # use slice to get orthogonal lines
        if isinstance(coords, slice):
            if isinstance(coords.start, Int2) and isinstance(coords.stop, Int2):
                step = coords.step if coords.step else 1
                if step < 0:
                    raise ValueError("Grid2D slicing step must be positive")

                # slice in X if the X of start and end points are the same
                if coords.start.x == coords.stop.x:
                    if coords.start.y > coords.stop.y:
                        start = coords.stop.y
                        stop = coords.start.y
                    else:
                        start = coords.start.y
                        stop = coords.stop.y

                    return [self[Int2(coords.start.x, y)] for y in range(start, stop + 1, step)]
                elif coords.start.y == coords.stop.y:
                    if coords.start.x > coords.stop.x:
                        start = coords.stop.x
                        stop = coords.start.x
                    else:
                        start = coords.start.x
                        stop = coords.stop.x

                    return [self[Int2(x, coords.start.y)] for x in range(start, stop + 1, step)]
                else:
                    raise ValueError(
                        "Slicing only supports straight lines. Either Y or X must be the same in start and stop")
            else:
                raise ValueError("Grid2D slicing requires start and stop to be Int2")
        elif isinstance(coords, BoundingBox2D):
            output = []
            for y in range(coords.min.y, coords.max.y):
                for x in range(coords.min.x, coords.max.x):
                    point = Int2(x, y)
                    if self.coordsInBounds(point):
                        output.append(self[point])
                    else:
                        raise ValueError(f"BoundingBox {coords} extends beyond the bounds of this grid")

            return output

        return super(Grid2D, self).__getitem__(self._coordsToIndex(coords))

    def __setitem__(self, coords, value):
        """
        :param Int2 coords: the coordinates of the item to set
        :param value: the value to which to set the coordinates
        """
        super(Grid2D, self).__setitem__(self._coordsToIndex(coords), value)

    def __delitem__(self, coords):
        """
        :param Int2 coords: the coordinates of the item to delete
        """
        super(Grid2D, self).__delitem__(self._coordsToIndex(coords))

    def __str__(self):
        outString = '\n'
        for y in range(self.height):
            for x in range(self.width):
                outString += str(self[Int2(x, y)]) + " "
            outString += '\n'

        return outString
