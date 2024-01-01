"""
Functions for testing, instantiating, and running a day's solver
"""

import importlib
import unittest

def _getTestModuleName(day):
    """

    :param int day:
    :return str:
    """
    return f"tests.test_day{str(day).zfill(2)}"


def _getTestClassName(day):
    """

    :param int day:
    :return str:
    """
    return _getTestModuleName(day) + f".TestDay{str(day).zfill(2)}"


def _getModuleName(day):
    """
    Make the module name for the given day

    :param int day:
    :return str:
    """
    return f"solutions.day{str(day).zfill(2)}"


def RunTests(day):
    """
    Finds the tests in the tests directory for the given day, and runs them

    :param int day: which day to try and run on

    :return bool: if the tests were successful
    """
    suite = unittest.loader.TestLoader().loadTestsFromName(_getTestModuleName(day))

    runner = unittest.TextTestRunner()
    results = runner.run(suite)

    return results.wasSuccessful()


def RunDay(day):
    """
    Imports the solver for the specified day, instantiates it, and runs it

    :param int day: which day to try and run
    """
    solverDay = importlib.import_module(_getModuleName(day))
    solver = solverDay.Solver()
    solver.Run()
