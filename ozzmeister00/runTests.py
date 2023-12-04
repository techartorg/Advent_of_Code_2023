'''
Setup the environment and run all the tests in the Tests directory because
the Code app on iPad doesn't seem to set up its environment all that well
'''

import unittest
import os
import sys

PROJECT_DIR = os.path.split(__file__)[0]

sys.path.append(PROJECT_DIR)

def Main():
    """
    Discover all the tests in the tests directory adjacent this file and run them
    """
    loader = unittest.TestLoader()
    suite = loader.discover(PROJECT_DIR)

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    Main()