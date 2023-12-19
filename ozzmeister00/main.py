'''
Setup the environment and run the solver for a given day, because
the Code app on iPad doesn't seem to set up its environment all that well
'''

import os
import sys

sys.path.append(os.path.split(__file__)[0])

# should only need to change the day number here in order to test new days
import solutions.day08 as today

if __name__ == '__main__':
    day = today.Solver()
    day.Run()