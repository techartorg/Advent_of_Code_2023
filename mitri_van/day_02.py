#! python3.11
"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just
barely reaches the surface of a large island floating in the sky. You
gently land in a fluffy pile of leaves. It's quite cold, but you don't see
much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the
lack of snow. He'll be happy to explain the situation, but it's a bit of a
walk, so you have some time. They don't get many visitors up here; would
you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either
red, green, or blue. Each time you play this game, he will hide a secret
number of cubes of each color in the bag, and your goal is to figure out
information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will
reach into the bag, grab a handful of random cubes, show them to you, and
then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your
puzzle input). Each game is listed with its ID number (like the 11 in
Game 11: ...) followed by a semicolon-separated list of subsets of cubes
that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, three sets of cubes are revealed from the bag (and then put back
again). The first set is 3 blue cubes and 4 red cubes; the second set is 1
red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green
cubes.

The Elf would first like to know which games would have been possible if
the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag
had been loaded with that configuration. However, game 3 would have been
impossible because at one point the Elf showed you 20 red cubes at once;
similarly, game 4 would also have been impossible because the Elf showed
you 15 blue cubes at once. If you add up the IDs of the games that would
have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded
with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum
of the IDs of those games?

Your puzzle answer was 2449.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any
water! He isn't sure why the water stopped; however, he can show you how to
get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game
you played, what is the fewest number of cubes of each color that could
have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

  - In game 1, the game could have been played with as few as 4 red, 2
    green, and 6 blue cubes. If any color had even one fewer cube, the
    game would have been impossible.
  - Game 2 could have been played with a minimum of 1 red, 3 green, and 4
    blue cubes.
  - Game 3 must have been played with at least 20 red, 13 green, and 6
    blue cubes.
  - Game 4 required at least 14 red, 3 green, and 15 blue cubes.
  - Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue
cubes multiplied together. The power of the minimum set of cubes in game 1
is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up
these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present.
What is the sum of the power of these sets?

Your puzzle answer was 63981.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

test_data = [ 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
              'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
              'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
              'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
              'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
            ]

DEBUG = True

class DiceSet():

    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.red}, {self.green}, {self.blue})>"

    def __lt__(self, other):
        result_red = self.red <= other.red
        result_green = self.green <= other.green
        result_blue = self.blue <= other.blue

        return result_red and result_green and result_blue

    def __gt__(self, other):
        result_red = self.red > other.red
        result_green = self.green > other.green
        result_blue = self.blue > other.blue

        return result_red and result_green and result_blue


class GameObject():

    def __init__(self, id):
        self.id = id
        self.sets = []

    def __repr__(self):
        return f"<{self.__class__.__name__}_{self.id} ({self.sets})>"

    @property
    def cube_power(self):
        red = max([x.red for x in self.sets if x.red != 0])
        green = max([x.green for x in self.sets if x.green != 0])
        blue = max([x.blue for x in self.sets if x.blue != 0])

        return red * green * blue

    def is_valid(self, test_draw):
        result = []
        for _set in self.sets:
            if _set < test_draw:
                result.append(True)
            else:
                result.append(False)
        return all(result)

    def parse_dice_draw(self, dice_draw):
        args = {}

        for draw in dice_draw:
            num_dice, color_dice = draw.split()
            args[color_dice] = int(num_dice)

        self.sets.append(DiceSet(**args))

    def populate_sets(self, data):
        for datum in data:
            dice_draw = datum.split(', ')
            self.parse_dice_draw(dice_draw)


def parse_data(raw_data):
    games = []

    for datum in raw_data:
        result = datum.split(': ')
        game_obj = GameObject(int(result[0].lstrip('Game ')))
        game_obj.populate_sets(result[1].split('; '))
        games.append(game_obj)

    return games


def main(raw_data):
    games= parse_data(raw_data)

    # Part 1
    test_draw = DiceSet(red=12, green=13, blue=14)
    result = []
    for game in games:
        if DEBUG:
            if game.is_valid(test_draw):
                print(f'Game {game.id}: {test_draw}\n{game.sets}\n')
            else:
                print(f'********Game {game.id}: {test_draw}\n{game.sets}\n')
        if game.is_valid(test_draw):
            result.append(game.id)
    result = [game.id for game in games if game.is_valid(test_draw)]

    print(f'The sum of: {result}\n\tis {sum(result)}\n')

    # Part 2
    result_pt2 = []
    for game in games:
        if DEBUG: print(f'Game {game.id}:\tPower = {game.cube_power}')
        result_pt2.append(game.cube_power)

    print(f'\nThe sum of: {result_pt2}\n\tis {sum(result_pt2)}\n')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_02_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.rstrip() for line in input_file.readlines( )]

    # main(test_data)
    main(raw_data)