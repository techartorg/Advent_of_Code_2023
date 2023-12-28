"""
Tools for grabbing input data from Advent of Code directly via Chrome's cookies

NOTE: ONLY SEND API REQUESTS ONCE EVERY FIFTEEN MINUTES AND ALWAYS CACHE INPUTS LOCALLY
"""


def downloadPuzzleInput(year: int, day: int) -> str:
    """
    Attempt to download the puzzle input form AdventOfCode.com/Year/day/DAY

    # TODO: Look at https://github.com/wimglenn/advent-of-code-data/tree/main/aocd for inspiration

    :param year: From which year do you want to download the puzzle data?
    :param day: For which day do you need the puzzle data
    :return: the puzzle data pulled directly from the web
    """
    pass


def getPuzzleInput(year: int, day: int) -> str:
    """
    Attempts to load the puzzle input for the given year and day, and if
    the input data file is not found, it will attempt to download and cache
    the data before returning the result

    :param year: The year for which you want the data
    :param day: The puzzle day for which you want the data
    :return str: The raw puzzle data from Advent of Code
    """
    pass


def cachePuzzleInput(data: str, day: int) -> bool:
    """
    Store the input puzzle data to a text file in the inputData directory
    using the common schema for doing so

    :param data: The data to cache
    :param day: the day we're caching
    :return: success of the operation
    """
    pass