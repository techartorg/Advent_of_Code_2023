"""
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: 
managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island 
isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't
 make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only 
 turned off the water a few days... weeks... oh no." His face sinks into a 
 look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check 
why we stopped getting more sand! There's a ferry leaving soon that is headed over in 
that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait 
for the ferry, maybe you can help us with our food production problem. The latest Island 
Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also 
lists what type of soil to use with each kind of seed, what type of fertilizer to use 
with each kind of soil, what type of water to use with each kind of fertilizer, and so 
on. Every type of seed, soil, fertilizer and so on is identified with a number, but
 numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't 
 necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from
 a source category into numbers in a destination category. That is, the section that starts
  with seed-to-soil map: describes how to convert a seed number (the source) to a soil number
   (the destination). This lets the gardener and his team know which soil to use with which 
   seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, 
the maps describe entire ranges of numbers that can be converted. Each line within a map 
contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range
 length of 2. This line means that the source range starts at 98 and contains two values:
  98 and 99. The destination range is the same length, but it starts at 50, so its two values 
  are 50 and 51. With this information, you know that seed number 98 corresponds to soil 
  number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 
96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 
52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 
10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know 
the closest location that needs a seed. Using these maps, find the lowest location number
 that corresponds to any of the initial seeds. To do this, you'll need to convert each seed
  number through other categories until you can find its corresponding location number.
   In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks
like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of
the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with
 seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number
 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds
to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest
location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the
 lowest location number that corresponds to any of the initial seed numbers?
"""

import utils.list
from utils.solver import ProblemSolver


class DefaultIntList(utils.list.defaultlist):
    """
    Override the functionality of defaultlist to pass
    the index we're appending to the fill function
    """

    def __init__(self):
        super(DefaultIntList, self).__init__(int)

    def _fill(self, index):
        while len(self) <= index:
            self.append(self._cls(index))


class Seed(object):
    """
    Given an input almanac, get all the information about a given seed
    """

    def __init__(self, seed, almanac):
        """
        :param Almanac almanac: the almanac to use to describe this seed
        """
        self.seed = seed
        self.soil = almanac.seedToSoilMap.findDestination(self.seed)
        self.fertilizer = almanac.soilToFertilizerMap.findDestination(self.soil)
        self.water = almanac.fertilizerToWaterMap.findDestination(self.fertilizer)
        self.light = almanac.waterToLightMap.findDestination(self.water)
        self.temperature = almanac.lightToTemperatureMap.findDestination(self.light)
        self.humidity = almanac.temperatureToHumidityMap.findDestination(self.temperature)
        self.location = almanac.humidityToLocationMap.findDestination(self.humidity)
        self.attributes = [self.seed, self.soil, self.fertilizer, self.water, self.light, self.temperature,
                           self.humidity, self.location]

    def __str__(self):
        return ' -> '.join([str(i) for i in self.attributes])


class Range(object):
    def __init__(self, rangeLine):
        """

        :param str rangeLine: of the form DestStart SourceStart Length
        """
        self.destStart, self.sourceStart, self.length = [int(i) for i in rangeLine.split(' ')]
        self.sourceEnd = self.sourceStart + self.length
        self.destEnd = self.destStart + self.length

    def isInRange(self, value):
        """
        :param int value: the value to look for in this range
        :return bool: whether the source value is contained by this range
        """
        return self.sourceStart <= value < self.sourceEnd

    def findDestination(self, value):
        """

        :param int value: the source value
        :return int: the destination value in this range
        """
        return (value - self.sourceStart) + self.destStart

    def doesRangeOverlap(self, other):
        """

        :param Range other: the range we want to test against

        :return bool: whether there's any overlap between the source of this range and the source of the input range
        """
        return other.sourceStart >= self.sourceStart or other.sourceEnd <= self.sourceEnd

    def getOverlap(self, other):
        """
        Return multiple ranges, defining the mappings between all the parts that overlap with the current range

        :param Range other: the range we want to build overlaps with
        :return list[Range]: three ranges for the head, heart, and tail of overlaps with the heart range
            describing the input Other's source range with this range as the Dest, while the head and tail ranges
            just map 1:1 for the source range
        """
        


class Mapping(object):
    """
    Contains all the ranges for a given mapping
    """

    def __init__(self, rangeLines):
        """
        :param list[str] rangeLines: the range lines we're working with
        """
        self.ranges = [Range(rangeLine) for rangeLine in rangeLines if rangeLine.strip()]

    def findDestination(self, source):
        """
        Look through all the ranges in this mapping to see if the input source is
        associated with any ranges, and if so return that mapping

        Otherwise, return the source itself

        :param int source: the source we're starting from
        :return int: the destination we're trying to get to
        """
        for range in self.ranges:
            if range.isInRange(source):
                return range.findDestination(source)

        return source


class Almanac(object):
    def __init__(self, inString):
        """
        Parse the input string into an almanac that properly maps seed to soil to fertilizer 
        to water to light to temperature to humidity to location. 

        :param str inString: the raw input from the puzzle after the initial seeds line
        """
        super(Almanac, self).__init__()

        lines = inString.splitlines()

        seedToSoil = 'seed-to-soil map:'
        seedToSoilIndex = lines.index(seedToSoil)
        soilToFertilizer = 'soil-to-fertilizer map:'
        soilToFertilizerIndex = lines.index(soilToFertilizer)
        fertilizerToWater = 'fertilizer-to-water map:'
        fertilizerToWaterIndex = lines.index(fertilizerToWater)
        waterToLight = 'water-to-light map:'
        waterToLightIndex = lines.index(waterToLight)
        lightToTemperature = 'light-to-temperature map:'
        lightToTemperatureIndex = lines.index(lightToTemperature)
        temperatureToHumidity = 'temperature-to-humidity map:'
        temperatureToHumidityIndex = lines.index(temperatureToHumidity)
        humidityToLocation = 'humidity-to-location map:'
        humidityToLocationIndex = lines.index(humidityToLocation)

        self.seedToSoilMap = self._buildMap(lines[seedToSoilIndex + 1:soilToFertilizerIndex - 1])
        self.soilToFertilizerMap = self._buildMap(lines[soilToFertilizerIndex + 1:fertilizerToWaterIndex - 1])
        self.fertilizerToWaterMap = self._buildMap(lines[fertilizerToWaterIndex + 1:waterToLightIndex - 1])
        self.waterToLightMap = self._buildMap(lines[waterToLightIndex + 1:lightToTemperatureIndex - 1])
        self.lightToTemperatureMap = self._buildMap(lines[lightToTemperatureIndex + 1:temperatureToHumidityIndex - 1])
        self.temperatureToHumidityMap = self._buildMap(
            lines[temperatureToHumidityIndex + 1:humidityToLocationIndex - 1])
        self.humidityToLocationMap = self._buildMap(lines[humidityToLocationIndex + 1:])

    @staticmethod
    def _buildMap(rangeLines):
        """
        Make a mapping for a given __ to __ map from the input lines

        :param list[str]: the line ranges you want to build from

        :returns Mapping: a list where the index maps the source value to a dest value
        """
        return Mapping(rangeLines)

    @staticmethod
    def _buildMapDefaultIntList(self, rangeLines):
        """
        This is too slow for words with the actual dataset

        :param rangeLines:
        :return:
        """
        # the defaultintlist class should handle cases where the subsequent ranges
        # overlap with parts of the list that have already been filled
        outList = DefaultIntList()
        for line in rangeLines:
            if line.strip():
                destStart, sourceStart, length = [int(i) for i in line.split(' ')]
                print(destStart, sourceStart, length)
                for i in range(length):
                    outList[sourceStart + i] = destStart + i

        return outList


class Solver(ProblemSolver):
    def __init__(self):
        super(Solver, self).__init__(5)

        self.testDataAnswersPartOne = [35]
        self.testDataAnswersPartTwo = [46]

    def ProcessInput(self, data=None):
        """
        :param str data: the raw input data

        :returns list[int], Almanac: return the seeds to plant, and the generated almanac
        """
        if not data:
            data = self.rawData

        lines = data.splitlines()

        seeds = [int(i) for i in lines[0].split(':')[-1].split(' ') if i.strip()]
        almanac = Almanac('\n'.join(lines[2:]))

        return seeds, almanac

    def SolvePartOne(self, data=None):
        """
        
        :param list[int], Almanac data: the seeds we're meant to locate and the Almanac to help us locate them

        :return int: the lowest location value for our input seeds
        """
        if not data:
            data = self.processed

        # unpack the data
        seeds, almanac = data

        locations = [Seed(seed, almanac).location for seed in seeds]

        return min(locations)

    def SolvePartTwo(self, data=None):
        """
        Instead of looking at the seed values in the almanac as explicit values, treat them as a range
        and return the lowest location from there

        :param list[int], Almanac data: the seeds we're meant to locate and the Almanac to help us locate them
        :return int: the lowest location
        """
        if not data:
            data = self.processed

        # unpack the data
        seeds, almanac = data

        # treat the seed values we have input as ranges as well
        seedRanges = []


if __name__ == '__main__':
    day = Solver()
    day.Run()
