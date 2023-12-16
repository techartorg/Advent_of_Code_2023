#! python3.11
"""
--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm
quickly approaching. When you turn to warn the Elf, she disappears before
your eyes! To be fair, she had just finished warning you about ghosts a few
minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of
documents (your puzzle input) about how to navigate the desert. At least,
you're pretty sure that's what they are; one of the documents contains a
list of left/right instructions, and the rest of the documents seem to
describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate
the network. Perhaps if you have the camel follow the same instructions,
you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You
feel like AAA is where you are now, and you have to follow the left/right
instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next
left/right instruction in your input. In this example, start with AAA and
go right (R) by choosing the right element of AAA, CCC. Then, L means to
choose the left element of CCC, ZZZ. By following the left/right
instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right
instructions, repeat the whole sequence of instructions as necessary: RL
really means RLRLRLRLRLRLRLRL... and so on. For example, here is a
situation that takes 6 steps to reach ZZZ:

    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are
required to reach ZZZ?

Your puzzle answer was 15871.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The sandstorm is upon you and you aren't any closer to escaping the
wasteland. You had the camel follow the instructions, but you've barely
left your starting position. It's going to take significantly more steps to
escape!

What if the map isn't for people - what if the map is for ghosts? Are
ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious
fact: the number of nodes with names ending in A is equal to the number
ending in Z! If you were a ghost, you'd probably just start at every node
that ends with A and follow all of the paths at the same time until they
all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with
A). As you follow each left/right instruction, use that instruction to
simultaneously navigate away from both nodes you're currently on. Repeat
this process until all of the nodes you're currently on end with Z. (If
only some of the nodes you're on end with Z, they act like any other node
and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6
steps.

Simultaneously start on every node that ends with A. How many steps does it
take before you're only on nodes that end with Z?

"""
import math

from collections import defaultdict

TEST_DATA = [ 'RL',
              '',
              'AAA = (BBB, CCC)',
              'BBB = (DDD, EEE)',
              'CCC = (ZZZ, GGG)',
              'DDD = (DDD, DDD)',
              'EEE = (EEE, EEE)',
              'GGG = (GGG, GGG)',
              'ZZZ = (ZZZ, ZZZ)',
            ]

TEST_DATA_2 = [ 'LLR',
                '',
                'AAA = (BBB, BBB)',
                'BBB = (AAA, ZZZ)',
                'ZZZ = (ZZZ, ZZZ)'
            ]

TEST_DATA_3 = [ 'LR',
                '',
                '11A = (11B, XXX)',
                '11B = (XXX, 11Z)',
                '11Z = (11B, XXX)',
                '22A = (22B, XXX)',
                '22B = (22C, 22C)',
                '22C = (22Z, 22Z)',
                '22Z = (22B, 22B)',
                'XXX = (XXX, XXX)'
            ]

INSTRUCTIONS = 'instructions'
DEBUG = True

class Node():

    def __init__(self, id):
        self.id = id
        self.children = []

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} ({self.children})>"

    def __str__(self):
        child_1 = 'None'
        child_2 = 'None'

        if self.children:
            if isinstance(self.children[0], Node):
                child_1 = self.children[0].id
            if isinstance(self.children[1], Node):
                child_2 = self.children[1].id

        return f"<{self.__class__.__name__} {self.id} ({child_1}, {child_2})>"

    def get_child(self, move):
        if move == 'L':
            return self.children[0]

        else:
            return self.children[1]


def add_child(child, parent, data):

    # Child is the parent or Child node already exists
    if child == parent.id:
        parent.children.append(child)

    elif child in data.keys():
        parent.children.append(child)#data[child])

    else:
        new_child = Node(child)
        parent.children.append(child)#new_child)
        data[child] = new_child


def parse_data(raw_data):
    data = defaultdict(list)
    new_parent = None

    data[INSTRUCTIONS] = raw_data[0]

    for line in raw_data[2:]:
        parent, _,  child_1, child_2 = line.replace('(','').replace(',','').replace(')','').split()

        # Create parent
        if parent not in data.keys():
            new_parent = Node(parent)
            data[parent] = new_parent
        else:
            new_parent = data[parent]

        # Create children
        add_child(child_1, new_parent, data)
        add_child(child_2, new_parent, data)

    return data


def walk_nodes(data, starting_move = 'AAA', ending_move = 'ZZZ', part_two = False):
    idx = 0
    steps = 0
    move = starting_move
    success = False

    if not part_two:
        while move != ending_move:
            for i in data[INSTRUCTIONS]:
                if i == 'L':
                    move = data[move].children[0]
                else:
                    move = data[move].children[1]
                steps += 1
                idx += 1

                if move == ending_move:
                    break

    else:
        while not success:
            for i in data[INSTRUCTIONS]:
                if i == 'L':
                    move = data[move].children[0]
                else:
                    move = data[move].children[1]
                steps += 1
                idx += 1
                if move.endswith('Z'):
                    success = True
                    break

    return steps


def main(raw_data, part_two = False):
    result = 0
    results = []
    data = parse_data(raw_data)
    starting_moves = [x for x in data.keys() if x.endswith('A')]

    if not part_two:
        result = walk_nodes(data)
        print(f'\nIt takes {result} steps to reach ZZZ')

    else:
        for move in starting_moves:
            result = walk_nodes(data, starting_move=move, part_two=part_two)
            results.append(result)
        print(f'\nIt takes {math.lcm(*results)} steps to reach nodes that end with Z')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_08_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.rstrip() for line in input_file.readlines( )]

    # main(TEST_DATA)
    # main(TEST_DATA_2)
    # main(raw_data)
    # main(TEST_DATA_3, part_two = True)
    main(raw_data, part_two = True)