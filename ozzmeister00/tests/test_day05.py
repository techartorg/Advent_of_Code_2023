from unittest import TestCase

import solutions.day05

class Test(TestCase):
    def test_range(self):
        # make sure that a range can be created through both methods and its creation can fail
        a = solutions.day05.Range("10 5")
        b = solutions.day05.Range(10, 5)

        self.assertRaises(ValueError, solutions.day05.Range)

        # test equivalency
        self.assertEquals(a, b)

        # make sure we error out when we test equivalency with an unsupported type
        self.assertRaises(TypeError, self.assertEquals, a, 'a')

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
        self.fail()

    def test_mappings(self):
        self.fail()
    

