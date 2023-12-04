from unittest import TestCase

import utils.string

class Test(TestCase):
    def test_findall(self):
        inString = 'abcdabc'
        subString = 'abc'
        startExpected = [0, 4]
        result = utils.string.findall(subString, inString)

        self.assertEqual(result, startExpected)

        endExpected = [3, 7]
        result = utils.string.findall_end(subString, inString)

        self.assertEqual(result, endExpected)

        result = utils.string.findall_range(subString, inString)
        expected = list(zip(startExpected, endExpected))

        self.assertEqual(result, expected)
