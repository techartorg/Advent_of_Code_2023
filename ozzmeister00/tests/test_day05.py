from unittest import TestCase

import solutions.day05


class TestDay05(TestCase):
    def test_range(self):
        # make sure that a range can be created through both methods and its creation can fail
        a = solutions.day05.Range("10 5")
        b = solutions.day05.Range(10, 5)

        self.assertRaises(ValueError, solutions.day05.Range)

        # test equivalency
        self.assertEqual(a, b)

        # make sure we error out when we test equivalency with an unsupported type
        self.assertRaises(TypeError, self.assertEqual, a, 'a')

        # test overlap
        overlapRange = solutions.day05.Range(7, 8)
        containsRange = solutions.day05.Range(11,2)
        nonOverlapRange = solutions.day05.Range(15, 5)

        self.assertTrue(b.overlaps(overlapRange))
        self.assertTrue(b.overlaps(containsRange))
        self.assertFalse(b.overlaps(nonOverlapRange))

        # test overlaps safety
        self.assertRaises(TypeError, self.assertEqual, b, 'b')

        # test getOverlaps safety
        self.assertRaises(TypeError, self.assertEqual, b, 'b')

        # test no Tail
        head, overlap, tail = a.getOverlaps(overlapRange)
        expectedHeadOverlap = solutions.day05.Range(7, 3)
        expectedOverlap = solutions.day05.Range(10, 5)
        self.assertIsNone(tail)
        self.assertEqual(expectedHeadOverlap, head)
        self.assertEqual(expectedOverlap, overlap)

        # test No Head
        c = solutions.day05.Range(7, 10)
        d = solutions.day05.Range(4, 6)
        expectedOverlap = solutions.day05.Range(7, 3)
        expectedTailOverlap = solutions.day05.Range(10, 7)
        head, overlap, tail = d.getOverlaps(c)
        self.assertIsNone(head)
        self.assertEqual(expectedOverlap, overlap)
        self.assertEqual(expectedTailOverlap, tail)

        # test Neither Head nor Tail (test range is fully enclosed by the target range)
        e = solutions.day05.Range(0, 15)
        expectedOverlap = solutions.day05.Range(4, 6)
        head, overlap, tail = e.getOverlaps(d)
        self.assertIsNone(head)
        self.assertEqual(expectedOverlap, overlap)
        self.assertIsNone(tail)

    def test_mapping(self):
        # test instantiation from a MappingLine
        mapping = solutions.day05.Mapping("10 5 5")

        # make sure we get the expected values
        self.assertEqual(10, mapping.dest.start)
        self.assertEqual(5, mapping.source.start)
        self.assertEqual(5, mapping.offset)
        self.assertEqual(5, mapping.source.length)

        # test fromDetails
        mappingFromDetails = solutions.day05.Mapping.fromDetails(5, 10, 5)

        # make sure we get the expected values
        self.assertEqual(10, mapping.dest.start)
        self.assertEqual(5, mapping.source.start)
        self.assertEqual(5, mapping.offset)
        self.assertEqual(5, mapping.source.length)

        # test fromRange
        testRange = solutions.day05.Range(5, 5)
        mappingFromRange = solutions.day05.Mapping.fromRange(testRange, 5)
        self.assertEqual(10, mapping.dest.start)
        self.assertEqual(5, mapping.source.start)
        self.assertEqual(5, mapping.offset)
        self.assertEqual(5, mapping.source.length)        

        # test equivalency
        self.assertEqual(mapping, mappingFromDetails)
        self.assertEqual(mapping, mappingFromRange)
        self.assertEqual(mappingFromRange, mappingFromDetails)

        # test single-value destination finding
        lowSource = 3
        midSource = 6
        highSource = 11

        self.assertEqual(3, mapping.findDestination(lowSource))
        self.assertEqual(11, mapping.findDestination(midSource))
        self.assertEqual(11, mapping.findDestination(highSource))

        # test overlap + low (Range, Mapping, None)
        tailMiddleRange = solutions.day05.Range(0, 10)
        
        head, overlap, tail = mapping.mapRangeToDest(tailMiddleRange)
        expectedHeadOverlap = solutions.day05.Range(0, 5)
        expectedOverlap = solutions.day05.Mapping.fromDetails(5, 10, 5)
        self.assertIsNone(tail)
        self.assertEqual(expectedHeadOverlap, head)
        self.assertEqual(expectedOverlap, overlap)

        # test No Head
        middleHeadRange = solutions.day05.Range(5, 10)
        head, overlap, tail = mapping.mapRangeToDest(middleHeadRange)
        expectedTailOverlap = solutions.day05.Range(10, 5)
        expectedOverlap = solutions.day05.Mapping.fromDetails(5, 10, 5)
        self.assertIsNone(head)
        self.assertEqual(expectedOverlap, overlap)
        self.assertEqual(expectedTailOverlap, tail)

        # test Neither Head nor Tail (test range is fully enclosed by the target range)
        middleRange = solutions.day05.Range(6, 2)
        head, overlap, tail = mapping.mapRangeToDest(middleRange)
        expectedOverlap = solutions.day05.Mapping.fromDetails(6, 11, 2)
        self.assertIsNone(head)
        self.assertEqual(expectedOverlap, overlap)
        self.assertIsNone(tail)

        # test no overlaps
        noOverlapRange = solutions.day05.Range(0, 2)
        self.assertTrue(mapping.doesRangeOverlapSource(noOverlapRange))

    def test_mappings(self):
        # make sure we can create a Mappings
        lines = ['10 5 5',
                 '20 15 5']

        mappings = solutions.day05.Mappings(lines)
        
        # make sure we can find a destination value in a Mappings
        self.assertEqual(10, mappings.findDestination(5))

        # make sure we can find a destination value not in the Mappings
        self.assertEqual(2, mappings.findDestination(2))

        # make sure we can create the correct destination Ranges
        # based on a source Range that overlaps two Mappings
        sourceRange = solutions.day05.Range(0, 20)
        expectedRanges = [solutions.day05.Mapping.fromDetails(0, 0, 5),
                          solutions.day05.Mapping.fromDetails(5, 10, 5),
                          solutions.day05.Mapping.fromDetails(10, 10, 5),
                          solutions.day05.Mapping.fromDetails(15, 20, 5)]

        results = mappings.mapSourceOverlaps([sourceRange])
        test = all([i in expectedRanges for i in results]) and len(results) == len(expectedRanges)
        self.assertTrue(test)

        # test actual data Seed to Soil
        sourceRanges = [solutions.day05.Range(79, 14),
                        solutions.day05.Range(55, 13)]
        mappingLines = ['50 98 2', '52 50 48']
        testDataMappings = solutions.day05.Mappings(mappingLines)
        results = testDataMappings.mapSourceOverlaps(sourceRanges)
        expectedResults = [solutions.day05.Mapping.fromDetails(79, 81, 14),
                           solutions.day05.Mapping.fromDetails(55, 57, 13)]
        
        test = all([i in expectedResults for i in results]) and len(results) == len(expectedResults)
        self.assertTrue(test)

        mappingLines = ['0 15 37', '37 52 2', '39 0 15']
        testDataMappings = solutions.day05.Mappings(mappingLines)
        results = testDataMappings.mapSourceOverlaps([r.dest for r in results])
