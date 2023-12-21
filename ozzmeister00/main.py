'''
Setup the environment and run the solver for a given day, because
the Code app on iPad doesn't seem to set up its environment all that well
'''

import argparse
import importlib
import os
import sys


sys.path.append(os.path.split(__file__)[0])


def runDay(dayNumber):
    """
    Imports the solver for the specified day, instantiates it, and runs it

    :param str dayNumber: numeral of which day to try and run
    """    
    
    moduleName = f"solutions.day{dayNumber.zfill(2)}"
    solverDay = importlib.import_module(moduleName)
    solver = solverDay.Solver()
    solver.Run()


def main():
    parser = argparse.ArgumentParser(prog="AoC Solver", description="Runs a specific AoC day solver")
    parser.add_argument("day")

    args = parser.parse_args()

    if args.day.isnumeric():
        runDay(args.day)
    else:
        raise IOError(f"Day must be a numeral")

if __name__ == '__main__':
    main()