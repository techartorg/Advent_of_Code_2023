'''
Setup the environment and run the solver for a given day, because
the Code app on iPad doesn't seem to set up its environment all that well
'''

import argparse
import os
import sys


sys.path.append(os.path.split(__file__)[0])


import solver.runner


def main():
    parser = argparse.ArgumentParser(prog="AoC Solver", description="Runs a specific AoC day solver")
    parser.add_argument("day")

    args = parser.parse_args()

    if args.day.isnumeric():
        if solver.runner.RunTests(args.day):
            solver.runner.RunDay(int(args.day))
    else:
        raise IOError(f"Day must be a numeral")


if __name__ == '__main__':
    main()