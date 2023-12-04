"""
--- Day 2: Cube Conundrum ---

You're launched high into the atmosphere! The apex of your trajectory just barely reaches 
the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves.
 It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow.
 He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. 
 They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. 
Each time you play this game, he will hide a secret number of cubes of each color in the bag,
 and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag,
 grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do 
 this a few times per game.

You play several games and record the information from each game (your puzzle input).
 Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a
  semicolon-separated list of subsets of cubes that were revealed from the bag
   (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). 
The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, 
and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained
 only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded 
with that configuration. However, game 3 would have been impossible because at one point the
 Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because 
 the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have 
 been possible, you get 8.

Determine which games would have been possible if the bag had been
 loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. 
 What is the sum of the IDs of those games?

 --- Part Two ---

The Elf says they've stopped producing snow because they aren't getting any water! 
He isn't sure why the water stopped; however, he can show you how to get 
to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you
 played, what is the fewest number of cubes of each color that could have been in
  the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. 
If any color had even one fewer cube, the game would have been impossible.

Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes
 multiplied together. The power of the minimum set of cubes in game 1 is 48.
  In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers
   produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. 
What is the sum of the power of these sets?

 """

import sys

from utils.solver import ProblemSolver

import utils.constants


class Game(object):
    def __init__(self, ID, hintString):
        """
        Object to represent a single "game"

        :param int ID: the ID number of this game
        :param str hintString: a string describing all the revealed rubes
        """
        self.ID = ID

        # store off all the values of revealed colors
        self.colors = {'red':[],
                        'green':[],
                        'blue':[]}

        for turn in hintString.split(';'):
            for hint in turn.split(','):
                value, color = hint.lstrip().split(' ')
                value = int(value)
                self.colors[color].append(value)

    def getMaxRed(self):
        """
        :returns int: the maximum value of Red seen in the game
        """
        return max(self.colors['red'])

    def getMaxGreen(self):
        """
        :returns int: the maximum value of Green seen in the game
        """
        return max(self.colors['green'])

    def getMaxBlue(self):
        """
        :returns int: the maximum value of Blue seen in the game
        """
        return max(self.colors['blue'])

    def isValidGame(self, cubeCounts):
        """
        :param dict[str: int] cubeCount: the max number of each color of cube that 
        could be present in the game

        :returns bool: if no color exceeds the input max count
        """
        return self.getMaxRed() <= cubeCounts['red'] and \
                self.getMaxGreen() <= cubeCounts['green'] and \
                self.getMaxBlue() <= cubeCounts['blue']

    def __str__(self):
        return f"Game {self.ID}: red {self.getMaxRed()}, green {self.getMaxGreen()}, blue {self.getMaxBlue()}"

    def __repr__(self):
        return f"Game({self.ID}, 'red {self.getMaxRed()}, green {self.getMaxGreen()}, blue {self.getMaxBlue()}')"


class Solver(ProblemSolver):
    def __init__(self):
        super(Solver, self).__init__(2)

        self.testDataAnswersPartOne = [8]
        self.testDataAnswersPartTwo = [2286]

    def ProcessInput(self, data=None):
        """
        Process the input data into a list of Game objects

        :param str data:
        :returns list[Game]: The list of game objects
        """
        if not data:
            data = self.rawData

        processed = []

        for line in data.splitlines():
            game, hintString = line.split(': ')
            game, gameID = game.split(' ')
            gameID = int(gameID)

            processed.append(Game(gameID, hintString))

        return processed

    def SolvePartOne(self, data=None):
        """
        :param list[Game] data: the processed list of Games

        :returns int: the sum of the ID numbers of the valid games
        """
        if not data:
            data = self.processed

        colorCounts = {'red': 12,
                        'green': 13,
                        'blue': 14}

        idSum = 0

        for game in data:
            if game.isValidGame(colorCounts):
                idSum += game.ID

        return idSum

    def SolvePartTwo(self, data=None):
        """
        :param list[Game] data: the processed games

        :returns int: the sum of the Power of each game in the list
        """
        if not data:
            data = self.processed

        sumPower = 0

        # the minimum number of cubes that could have been present in any given game
        # is the maximum number of cubes that were seen at any one time
        for game in data:
            sumPower += (game.getMaxRed() * game.getMaxGreen() * game.getMaxBlue())

        return sumPower


if __name__ == '__main__':
    day = Solver()
    day.Run()
