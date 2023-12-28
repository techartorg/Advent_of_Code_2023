from unittest import TestCase

import utils.math


class Test(TestCase):
    def test_clamp(self):
        testValues = {(2, 3, 4): 3,
                      (3, 2, 4): 3,
                      (4, 2, 3): 3}

        for test, answer in testValues.items():
            self.assertEqual(utils.math.clamp(test[0], test[1], test[2]),
                             answer, msg="Failed to properly clamp {} to {}".format(test, answer))

    def test_saturate(self):
        testValues = {-1.0: 0.0,
                      0.5: 0.5,
                      1.5: 1.0}

        for test, answer in testValues.items():
            self.assertEqual(utils.math.saturate(test), answer,
                             msg="Failed to saturate {} to expected {}".format(test, answer))


class TestTwoD(TestCase):
    def setUp(self):
        self.testValues = 'AB'
        self.otherValues = 'CD'
        self.testObj = utils.math.TwoD(*self.testValues)
        self.otherObj = utils.math.TwoD(*self.otherValues)

        self.floatValues = [1.5, 2.5]
        self.otherFloatValues = [.5, 1.5]
        self.testFloatObj = utils.math.Float2(*self.floatValues)
        self.otherFloatObj = utils.math.Float2(*self.otherFloatValues)

    def test_values(self):
        self.assertEqual(self.testObj.x, self.testValues[0],
                         msg="For some reason {} does not equal A".format(self.testObj.x))
        self.assertEqual(self.testObj.y, self.testValues[1],
                         msg="For some reason {} does not equal B".format(self.testObj.y))

    def test_eq(self):
        self.assertEqual(self.testObj, self.testObj,
                         msg="For some reason {} does not equal itself".format(self.testObj))

        self.assertNotEqual(self.testObj, self.otherObj,
                            msg="For some reason {} equals {}".format(self.testObj, self.otherObj))

    def test_hash(self):
        a = utils.math.Int2(0, 0)
        b = utils.math.Int2(0, 0)
        c = utils.math.Int2(0, 1)
        twoDList = [a, b, c]
        try:
            setList = list(set(twoDList))
        except Exception as e:
            self.fail(msg=f"Failed to create a set using class TwoD\n{e}")

    def test_add(self):
        singleAdd = self.testObj + 'A'
        self.assertEqual(singleAdd.x, 'AA',
                         msg="For some reason {} does not equal AA".format(singleAdd.x))
        self.assertEqual(singleAdd.y, 'BA',
                         msg="For some reason {} does not equal BA".format(singleAdd.y))

        sameEquivalent = utils.math.TwoD('AC', 'BD')
        sameClassAdd = self.testObj + self.otherObj
        self.assertEqual(sameEquivalent, sameClassAdd,
                         msg="For some reason {} does not equal AC,BD".format(sameClassAdd))

        sameClass = self.testFloatObj + self.otherFloatObj
        expected = utils.math.Float2(self.floatValues[0] + self.otherFloatValues[0],
                                     self.floatValues[1] + self.otherFloatValues[1])
        self.assertEqual(sameClass, expected,
                         msg="For some reason {} does not equal {}".format(sameClass, expected))

        oneD = self.otherFloatObj + .5
        oneDExpected = utils.math.Float2(1.0, 2.0)
        self.assertEqual(oneD, oneDExpected,
                         msg="For some reason {} does not equal {}".format(oneD, oneDExpected))

    def test_mul(self):
        sameClass = self.testFloatObj * self.otherFloatObj
        expected = utils.math.Float2(self.floatValues[0] * self.otherFloatValues[0],
                                      self.floatValues[1] * self.otherFloatValues[1])
        self.assertEqual(sameClass, expected,
                         msg="For some reason {} does not equal {}".format(sameClass, expected))

        oneD = self.otherFloatObj * 2.0
        oneDExpected = utils.math.Float2(1.0, 3.0)
        self.assertEqual(oneD, oneDExpected,
                         msg="For some reason {} does not equal {}".format(oneD, oneDExpected))

    def test_div(self):
        sameClassDivided = self.testFloatObj / self.otherFloatObj
        expected = utils.math.Float2(self.floatValues[0] / self.otherFloatValues[0],
                                      self.floatValues[1] / self.otherFloatValues[1])
        self.assertEqual(sameClassDivided, expected,
                         msg="For some reason {} does not equal {}".format(sameClassDivided, expected))

        oneD = self.otherFloatObj / 2.0
        oneDExpected = utils.math.Float2(.25, .75)
        self.assertEqual(oneD, oneDExpected,
                         msg="For some reason {} does not equal {}".format(oneD, oneDExpected))

    def test_sub(self):
        sameClass = self.testFloatObj - self.otherFloatObj
        expected = utils.math.Float2(self.floatValues[0] - self.otherFloatValues[0],
                                      self.floatValues[1] - self.otherFloatValues[1])
        self.assertEqual(sameClass, expected,
                         msg="For some reason {} does not equal {}".format(sameClass, expected))

        oneD = self.otherFloatObj - .5
        oneDExpected = utils.math.Float2(0.0, 1.0)
        self.assertEqual(oneD, oneDExpected,
                         msg="For some reason {} does not equal {}".format(oneD, oneDExpected))

    def test_length(self):
        a = utils.math.Float2(0.0, 1.0)
        self.assertEqual(a.length(), 1.0)

    def test_distance(self):
        a = utils.math.Float2(1.0, 1.0)
        b = utils.math.Float2(1.0, 2.0)
        self.assertEqual(a.distance(b), 1.0)

    def test_normalize(self):
        a = utils.math.Float2(1.0, 2.0).normalize()
        expected = [0.4472135954999579, 0.8944271909999159]
        self.assertEqual(a[0], expected[0])
        self.assertEqual(a[1], expected[1])

    def test_direction(self):
        a = utils.math.Float2(1.0, 0.0)
        b = utils.math.Float2(0.0, 0.0)
        aToB = utils.math.Float2(-1.0, 0.0)
        bToA = utils.math.Float2(1.0, 0.0)

        self.assertEqual(a.direction(b), aToB)
        self.assertEqual(b.direction(a), bToA)

        a = utils.math.Int2(0, 0)
        b = utils.math.Int2(1, 1)
        c = utils.math.Int2(-1, -1)

        self.assertEqual(a.direction(b), b)
        self.assertEqual(b.direction(a), c)


class TestBoundingBox2D(TestCase):
    def setUp(self):
        minValue = utils.math.Int2(1, 1)
        maxValue = utils.math.Int2(4, 4)
        self.bbox = utils.math.BoundingBox2D(minValue, maxValue)

    def test_class(self):
        self.assertEqual(3, self.bbox.width)
        self.assertEqual(3, self.bbox.height)
        self.assertEqual(utils.math.Int2(1, 4), self.bbox.topLeft)
        self.assertEqual(utils.math.Int2(4, 1), self.bbox.bottomRight)

    def test_contains(self):
        inside = utils.math.Int2(2, 2)
        outside = utils.math.Int2(0, 0)

        self.assertTrue(self.bbox.pointInside(inside))
        self.assertFalse(self.bbox.pointInside(outside))

    def test_overlap(self):
        doesOverlap = utils.math.BoundingBox2D(utils.math.Int2(0, 0),
                                               utils.math.Int2(2, 2))
        doesNotOverlap = utils.math.BoundingBox2D(utils.math.Int2(5, 5), 
                                                  utils.math.Int2(7, 7))
        
        self.assertTrue(self.bbox.overlaps(doesOverlap))
        self.assertFalse(self.bbox.overlaps(doesNotOverlap))
        self.assertRaises(ValueError, self.bbox.overlaps, 'Foo')

    def test_fromPoints(self):
        points = [utils.math.Int2(1, 1),
                  utils.math.Int2(4, 4),
                  utils.math.Int2(2, 1),
                  utils.math.Int2(1, 2)]

        self.assertEqual(self.bbox, utils.math.BoundingBox2D.fromPoints(points))


class TestLine2D(TestCase):
    def test_length(self):
        start = utils.math.Int2(1, 1)
        end = utils.math.Int2(3, 3)
        line = utils.math.Line2D(start, end)
        self.assertEqual(4, line.length)

    def test_direction(self):
        start = utils.math.Int2(1, 1)
        end = utils.math.Int2(3, 3)
        line = utils.math.Line2D(start, end)
        self.assertEqual(utils.math.Int2(1, 1), line.direction)

    def test_intersection(self):
        targetLine = utils.math.Line2D(utils.math.Int2(0, 0),
                                          utils.math.Int2(1, 10))

        intersecting = utils.math.Line2D(utils.math.Int2(0, 5),
                                            utils.math.Int2(5, 5))

        nonIntersecting = utils.math.Line2D(utils.math.Int2(5, 5),
                                               utils.math.Int2(10, 5))

        self.assertTrue(targetLine.intersects(intersecting))
        self.assertFalse(targetLine.intersects(nonIntersecting))

        polygonTestA = utils.math.Line2D(utils.math.Int2(2, 2),
                                         utils.math.Int2(6, 2))
        polygonTestB = utils.math.Line2D(utils.math.Int2(5, 5),
                                         utils.math.Int2(5, 0))

        self.assertTrue(polygonTestA.intersects(polygonTestB))


class TestPolygon(TestCase):
    TEST_POINTS = [utils.math.Int2(0, 0),
                   utils.math.Int2(0, 5),
                   utils.math.Int2(3, 3),
                   utils.math.Int2(5, 5),
                   utils.math.Int2(5, 0)]
    
    def setUp(self):
        self.polygon = utils.math.Polygon2D(self.TEST_POINTS)

    def test_polygon(self):
        """
        Make sure that when we make a polygon it ends up with the
        correct number of edges
        """
        self.assertEqual(5, len(self.polygon.edges))

    def test_pointInside(self):
        """
        Make sure the raycasting algorithm works
        """
        pointInside = utils.math.Int2(2, 2)
        pointOutsideBBox = utils.math.Int2(6, 6)
        pointOutsideInBBox = utils.math.Int2(3, 4)

        self.assertTrue(self.polygon.pointInside(pointInside))
        self.assertFalse(self.polygon.pointInside(pointOutsideBBox))
        self.assertFalse(self.polygon.pointInside(pointOutsideInBBox))

    def test_2023Day10State(self):
        vertexes = [utils.math.Int2(1, 1), 
                    utils.math.Int2(8, 1),
                    utils.math.Int2(8, 7),
                    utils.math.Int2(5, 7),
                    utils.math.Int2(5, 5),
                    utils.math.Int2(7, 5),
                    utils.math.Int2(7, 2),
                    utils.math.Int2(2, 2),
                    utils.math.Int2(2, 5),
                    utils.math.Int2(4, 5), 
                    utils.math.Int2(4, 7),
                    utils.math.Int2(1, 7)]

        polygon = utils.math.Polygon2D(vertexes)

        points = [utils.math.Float2(2.5, 6.5), utils.math.Int2(3.5, 6.5)]

        for point in points:
            self.assertTrue(polygon.pointInside(point))

        
class TestGrid2D(TestCase):
    def setUp(self):
        self.inGrid = 'ABCD'
        self.testCoords = [(utils.math.Int2(0, 0), 'A'),
                           (utils.math.Int2(1, 0), 'B'),
                           (utils.math.Int2(0, 1), 'C'),
                           (utils.math.Int2(1, 1), 'D')]

    def test_get(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        for key, value in self.testCoords:
            self.assertEqual(testObj[key], value)

    def test_set(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        target = utils.math.Int2(1, 1)
        testObj[target] = 'E'
        self.assertEqual(testObj[target], 'E')

    def test_enumerateRow(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        expectedRow = ['A', 'B']

        outRow = [value for coord, value in testObj.enumerateRow(0)]
        self.assertEqual(expectedRow, outRow)

        expectedRow = ['B', 'A']
        outRow = [value for coord, value in testObj.enumerateRow(0, reverse=True)]
        self.assertEqual(expectedRow, outRow)

    def test_enumerateRows(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        expectedOutput = [['A', 'B'], ['C', 'D']]
        reversedOutput = list(reversed(expectedOutput))

        outRows = [value for row, value in testObj.enumerateRows()]
        self.assertEqual(expectedOutput, outRows)

        reversedRows = [value for row, value in testObj.enumerateRows(reverse=True)]
        self.assertEqual(expectedOutput, outRows)

    def test_enumerateColumn(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        expectedColumn = ['A', 'C']
        outColumn = [value for coord, value in testObj.enumerateColumn(0)]
        self.assertEqual(expectedColumn, outColumn)

        expectedColumn = ['C', 'A']
        outColumn = [value for coord, value in testObj.enumerateColumn(0, reverse=True)]
        self.assertEqual(expectedColumn, outColumn)

    def test_enumerateColumns(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        expectedOutput = [['A', 'C'], ['B', 'D']]
        reversedOutput = list(reversed(expectedOutput))

        outColumns = [value for x, value in testObj.enumerateColumns()]
        self.assertEqual(expectedOutput, outColumns)

        outColumns = [value for x, value in testObj.enumerateColumns(reverse=True)]
        self.assertEqual(reversedOutput, outColumns)

    def test_finders(self):
        data = [1, 2, 3, 1]
        testObj = utils.math.Grid2D(2, data=data)
        indexes = testObj.findIndexes(1)
        expectedIndexes = [0, 3]

        self.assertEqual(indexes, expectedIndexes)

        coords = testObj.findCoords(1)
        expectedCoords = [utils.math.Int2(0, 0), utils.math.Int2(1, 1)]

        self.assertEqual(coords, expectedCoords)

    def test_slice(self):
        testObj = utils.math.Grid2D(2, data=self.inGrid)
        outSlice = testObj[self.testCoords[0][0]:self.testCoords[1][0]]
        expected = ['A', 'B']
        self.assertEqual(outSlice, expected)

    def test_bboxGet(self):
        testGrid = list(range(9))
        testObj = utils.math.Grid2D(3, data=testGrid)

        minValue = utils.math.Int2(0, 0)
        maxValue = utils.math.Int2(2, 2)
        bbox = utils.math.BoundingBox2D(minValue, maxValue)

        expected = [0, 1, 3, 4]

        self.assertEqual(expected, testObj[bbox])

    def test_insertRow(self):
        testGrid = list(range(9))
        testObj = utils.math.Grid2D(3, data=testGrid)

        testObj.insertRow(1, '***')

        expected = '''012***345678'''
        result = ''.join([str(i) for i in testObj])
        self.assertEqual(expected, result)

    def test_insertColumn(self):
        testGrid = list(range(9))
        testObj = utils.math.Grid2D(3, data=testGrid)

        testObj.insertColumn(1, '***')

        expected = '''0*123*456*78'''
        result = ''.join([str(i) for i in testObj])
        self.assertEqual(expected, result)
