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
    """
    A data class to hold a "Range" of values starting from the source, and going as far as Start + Length
    so that for a given Range(15, 4) the result will be:

    Start = 15
    Length = 4
    End = 18
    """
    def __init__(self, *args, **kwargs):
        """
        Make a new range, with a couple of different possible creation methods

        TODO figure out if it's better to do this with __new__ and some static methods
        """
        if not args:
            raise ValueError("Insufficient arguments input to create a Range")

        if isinstance(args[0], str):
            args = [int(i) for i in args[0].split(' ')]

        self.start = args[0]
        self.length = args[1]
        self.last = self.start + self.length - 1

    def __eq__(self, other):
        """
        Determine if this range and the input range match
        """
        if isinstance(other, Range):
            return other.start == self.start and \
                   other.last == self.last and \
                   other.length == self.length

        raise TypeError(f"Cannot test equivalency with {other} since it is of type {type(other)}")

    def __repr__(self):
        return f"Range({self.start}, {self.length})"

    def __str__(self):
        return f"{self.start}->{self.last}"

    def valueInRange(self, value):
        """
        Test if an input value is contained by this range

        :param int value:

        :returns bool:
        """
        return self.start <= value <= self.last

    def overlaps(self, other):
        """
        Test if the input range overlaps with this one at all

        :param Range other:
        
        :returns bool:
        """
        if isinstance(other, Range):
            return other.valueInRange(self.start) or \
                   other.valueInRange(self.last) or \
                   (self.valueInRange(other.start) and \
                   self.valueInRange(other.last))

        raise TypeError(f"Cannot test overlap with non-Range object {other}")

    def getOverlaps(self, other):
        """
        Given an input Range, make a range where the two overlap with each
        other, and also return the remainders on either side of the input range
        
        If there's nothing on either side of the overlap, then head and tail will be n

        :param Range other:
        
        :returns Range, Range, Range: the head, middle, and tail overlaps
        """
        head = overlap = tail = None
        if isinstance(other, Range):
            if self.overlaps(other):

                overlapStart = max(self.start, other.start)
                overlapEnd = min(self.last, other.last)
                overlapLength = overlapEnd - overlapStart + 1

                # if the overlap start is above the input start
                # that means we have a head section of the overlap
                if overlapStart >= self.start and self.start > other.start:
                    head = Range(other.start, self.start - other.start)

                # if the overlap end is below the input end
                # that means we have a tail section of the overlap
                if overlapEnd > self.last:
                    tail = Range(overlapEnd + 1, self.last - overlapEnd)

                # alternatively
                if self.last < other.last:
                    tail = Range(self.last + 1, other.last - self.last)

                # the actual overlapping area
                overlap = Range(overlapStart, overlapLength)

            return head, overlap, tail

        raise TypeError(f"Cannot get overlaps with non-Range object {other}")


class Mapping(object):
    """
    Helper object that maps an input source Range to a dest Range
    """
    def __init__(self, mappingLine):
        """

        :param str mappingLine: of the form DestStart SourceStart Length
        """
        destStart, sourceStart, length = [int(i) for i in mappingLine.split(' ')]
        self.source = Range(sourceStart, length)
        self.dest = Range(destStart, length)
        self.offset = destStart - sourceStart

    def __repr__(self):
        return f"Mapping('{self.dest.start} {self.source.start} {self.source.length}')"

    def __str__(self):
        return self.__repr__()

    def valueInSourceRange(self, value):
        """
        Return whether or not an input value is contained by the source
        of this mapping

        :param int other:

        :returns bool:
        """
        return self.source.valueInRange(value)

    def findDestination(self, value):
        """
        :param int value: the source value
        :return int: the destination value in this mapping
        """
        if self.valueInSourceRange(value):
            return value + self.offset        
        
        return value

    def mapRangeToDest(self, other):
        """
        Map an input Range to destinations as defined by
        this mapping

        :param Range other:

        :return Range, Mapping, Range: The head range that doesn't overlap with this mapping, the mapping between this
        """
        head, overlap, tail = self.source.getOverlaps(other)
        if overlap:
            overlapMapping = Mapping.fromRange(overlap, self.offset)

            return head, overlapMapping, tail

        return None, None, None

    def doesRangeOverlapSource(self, other):
        """
        Test if the input Range overlaps the source of this Mapping

        :param Range other:
        :returns bool:
        """
        return self.source.getOverlaps(other)

    @staticmethod
    def fromDetails(sourceStart, destStart, length):
        """
        Make a new Range from an actual source start, dest start, and length

        :param int sourceStart: 
        :param int destStart:
        :param int length:
        """
        return Mapping(f"{destStart} {sourceStart} {length}")

    @staticmethod
    def fromRange(sourceRange, offset):
        """
        Make a new mapping from an input Range, with an offset

        :param Range sourceRange:
        :param int offset:

        :return Mapping:
        """
        destStart = sourceRange.start + offset
        return Mapping.fromDetails(sourceRange.start, destStart, sourceRange.length)

    def __eq__(self, other):
        """
        :param Mapping other: the test Mapping
        :return bool: if the input other matches ourself
        """
        if isinstance(other, Mapping):
            return self.source == other.source and \
                   self.dest == other.dest

        return False


class Mappings(list):
    """
    Contains all the mappings from a given type-to-type connection
    """
    def __init__(self, mappingLines):
        """
        :param list[str] mappingLines: the mapping lines we're working with
        """
        self.mappings = [Mapping(mappingLine) for mappingLine in mappingLines if mappingLine.strip()]

    def findDestination(self, source):
        """
        Look through all the ranges in this mapping to see if the input source is
        associated with any ranges, and if so return that mapping

        Otherwise, return the source itself

        :param int source: the source we're starting from
        :return int: the destination we're trying to get to
        """
        for mapping in self.mappings:
            if mapping.valueInSourceRange(source):
                return mapping.findDestination(source)

        return source

    @property
    def destinations(self):
        """
        Just return a list of all the destination ranges contained by this Mappings
        """
        return [dest for mapping.dest in self.mappings]

    def mapSourceOverlaps(self, sourceRanges):
        """
        Map all the values in the input source Ranges to destination values
        regardless of whether or not they're contained in the mapping
        (so that some output Mappings will be 1:1)

        :param list[Range] sourceRanges: all of the unmapped source ranges we need to map

        :param list[Range]: all the destination ranges for the input source ranges
        """
        # Next we need to split those seed ranges into range mappings of seed to soil, regardless of 
        # whether or not there are overlaps

        # copy the list over, we don't want things to get weird
        unmappedSources = [i for i in sourceRanges]
        destinationRanges = []

        maxIters = 10
        iters = 0

        while unmappedSources and iters < maxIters:
            foundOverlap = False
            sourceRange = unmappedSources.pop(0)
            iters += 1

            i = 0

            # iterate through the mappings, but only process one overlap at a time
            while i < len(self.mappings) and not foundOverlap and iters < maxIters:
                iters += 1  # safety
                
                currentMapping = self.mappings[i]
                head, overlap, tail = currentMapping.mapRangeToDest(sourceRange)
                
                if overlap:
                    foundOverlap = True
                    # then add it to the mapping
                    destinationRanges.append(overlap)

                    # if there was a tail of the overlap, return it back to the list of unmapped for later processing
                    if head:
                        unmappedSources.append(head)
                    # same with the tail
                    if tail:
                        unmappedSources.append(tail)

                i += 1

            # if no overlap was found, just create a range mapping Start to itself
            # so we can continue using Range objects for subsequent overlap determinations
            if not foundOverlap:
                destinationRanges.append(Mapping.fromDetails(sourceRange.start, sourceRange.start, sourceRange.length))

        return destinationRanges


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




if __name__ == '__main__':
    day = Solver()
    day.Run()
