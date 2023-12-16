#! python3.11
"""
--- Day 16: The Floor Will Be Lava ---
With the beam of light completely focused somewhere, the reindeer leads you
deeper still into the Lava Production Facility. At some point, you realize
that the steel facility walls have been replaced with cave, and the
doorways are just cave, and the floor is cave, and you're pretty sure this
is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a
bright light in a cavern up ahead. There, you discover that the beam of
light you so carefully focused is emerging from the cavern wall closest to
the facility and pouring all of its energy into a contraption on the
opposite side.

Upon closer inspection, the contraption appears to be a flat, two-
dimensional square grid containing empty space (.), mirrors (/ and \), and
splitters (| and -).

The contraption is aligned so that most of the beam bounces around the
grid, but each tile on the grid converts some of the beam's light into heat
to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....

The beam enters in the top-left corner from the left and heading to the
right. Then, its behavior depends on what it encounters as it moves:

    If the beam encounters empty space (.), it continues in the same
    direction.
    If the beam encounters a mirror (/ or \), the beam is reflected 90
    degrees depending on the angle of the mirror. For instance, a
    rightward-moving beam that encounters a / mirror would continue upward
    in the mirror's column, while a rightward-moving beam that encounters
    a \ mirror would continue downward from the mirror's column.
    If the beam encounters the pointy end of a splitter (| or -), the beam
    passes through the splitter as if the splitter were empty space. For
    instance, a rightward-moving beam that encounters a - splitter would
    continue in the same direction.
    If the beam encounters the flat side of a splitter (| or -), the beam
    is split into two beams going in each of the two directions the
    splitter's pointy ends are pointing. For instance, a rightward-moving
    beam that encounters a | splitter would split into two beams: one that
    continues upward from the splitter's column and one that continues
    downward from the splitter's column.

Beams do not interact with other beams; a tile can have many beams passing
through it at the same time. A tile is energized if that tile has at least
one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the
contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..

Beams are only shown on empty tiles; arrows indicate the direction of the
beams. If a tile contains beams moving in multiple directions, the number
of distinct directions is shown instead. Here is the same diagram but
instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..

Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the
contraption, you need to start by analyzing the current situation. With the
beam starting in the top-left heading right, how many tiles end up being energized?

Your puzzle answer was 7034.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
As you try to work out what might be wrong, the reindeer tugs on your shirt
and leads you to a nearby control panel. There, a collection of buttons
lets you align the contraption so that the beam enters from any edge tile
and heading away from that edge. (You can choose either of two directions
for the beam if it starts on a corner; for instance, if the beam starts in
the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any
tile in the bottom row (heading upward), any tile in the leftmost column
(heading right), or any tile in the rightmost column (heading left). To
produce lava, you need to find the configuration that energizes as many
tiles as possible.

In the above example, this can be achieved by starting the beam in the
fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..

Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..

Find the initial beam configuration that energizes the largest number of
tiles; how many tiles are energized in that configuration?

Your puzzle answer was 7759.

Both parts of this puzzle are complete! They provide two gold stars: **

"""
import copy
from collections import deque

TEST_DATA = [ r'.|...ϡ....',
              r'|.-.ϡ.....',
              r'.....|-...',
              r'........|.',
              r'..........',
              r'.........ϡ',
              r'..../.ϡϡ..',
              r'.-.-/..|..',
              r'.|....-|.ϡ',
              r'..//.|....'
            ]

ENERGIZED_TILE = '#'

MIRROR_DIAG_BACK = 'ϡ'
MIRROR_DIAG_FWD = '/'
MIRROR_VERTICAL = '|'
MIRROR_HORIZONTAL = '-'

DEBUG = False



class CaveObject():

    def __init__(self, x, y, contents='.'):
        self.id = contents
        self.x = x
        self.y = y
        self.contents = [contents]

    def __repr__(self):
        return f'{str(self.id)}'

    def __str__(self):
        return f'{str(self.id)}'

    @property
    def is_energized(self):
        return bool([x for x in self.contents if x == ENERGIZED_TILE])

    def add_content(self, item):
        if item == '\\':
            item = 'ϡ'

        if item != ENERGIZED_TILE:
            self.id = item

        self.contents.append(item)

    def remove_content(self, item):
        self.contents.remove(item)
        self.id = self.contents[0]


def _print(obj, show_beam = False):
    if show_beam:
        results = []

        for datum in obj:
            if len(datum.contents) == 3:
                results.append(datum.contents[2])
            elif len(datum.contents) == 2:
                results.append(datum.contents[1])
            else:
                results.append(datum.contents[0])

        print(''.join(results))

    else:
        print(''.join(map(str, obj)))



def _traverse_y(data, x, y, reverse = False):
    while 0 <= y < len(data):# or 0 < y < len(data):
        if 0 > x >= len(data[0] - 1):
            if DEBUG: [_print(x, show_beam = True) for x in data]
            break # Out of bounds

        # Energize the current position
        if len(data[y][x].contents) > 3:
            break # Diagonal Mirror energized multiple times
        elif len(data[y][x].contents) > 2:
            if data[y][x].id == MIRROR_HORIZONTAL:
                break # Node already traversed
        else:
            data[y][x].add_content(ENERGIZED_TILE)

        # Move the scan head
        if data[y][x].id == MIRROR_DIAG_BACK:       # \
            if DEBUG: [_print(x, show_beam = True) for x in data]
            if not reverse:
                _traverse_x(data, x + 1, y)
            else:
                _traverse_x(data, x - 1, y, reverse = True)
            break

        elif data[y][x].id == MIRROR_DIAG_FWD:      # /
            if DEBUG: [_print(x, show_beam = True) for x in data]
            if not reverse:
                _traverse_x(data, x - 1, y, reverse = True)
            else:
                _traverse_x(data, x + 1, y)
            break

        elif data[y][x].id == MIRROR_HORIZONTAL:    # -
            if DEBUG:
                [_print(x, show_beam = True) for x in data]
                print('\n')
            _traverse_x(data, x - 1, y, reverse = True)
            _traverse_x(data, x + 1, y)
            break

        else:                                       # | or .
            pass # Do no additional things

        # Move onto the next index
        if reverse:
            y -= 1
        else:
            y += 1

def _traverse_x(data, x, y, reverse = False):
    while 0 <= x < len(data[0]):
        if 0 > y > len(data):
            if DEBUG: [_print(x, show_beam = True) for x in data]
            break # Out of bounds

        # Energize the current position
        if len(data[y][x].contents) > 3:
            break # Diagonal Mirror energized multiple times
        elif len(data[y][x].contents) > 2:
            if data[y][x].id == MIRROR_VERTICAL:
                break # Node already traversed
        else:
            data[y][x].add_content(ENERGIZED_TILE)

        # Move the scan head
        if data[y][x].id == MIRROR_DIAG_BACK:      # \
            if DEBUG: [_print(x, show_beam = True) for x in data]
            if not reverse:
                _traverse_y(data, x, y + 1)
            else:
                _traverse_y(data, x, y - 1, reverse = reverse)
            break

        elif data[y][x].id == MIRROR_DIAG_FWD:     # /
            if DEBUG: [_print(x, show_beam = True) for x in data]
            if not reverse:
                _traverse_y(data, x, y - 1, reverse = True)
            else:
                _traverse_y(data, x, y + 1)
            break

        elif data[y][x].id == MIRROR_VERTICAL:     # |
            if DEBUG:
                [_print(x, show_beam = True) for x in data]
                print('\n')
            _traverse_y(data, x, y - 1, reverse = True)
            _traverse_y(data, x, y + 1)
            break

        else:                                       # - or .
            pass # Do no additional things

        # Move onto the next index
        if reverse:
            x -= 1
        else:
            x += 1


def calculate_energized_tiles(data):
    results = []

    for row_idx, row in enumerate(data):
        for col_idx, item in enumerate(row):
            if item.is_energized:
                results.append(item)

    return len(results)


def fire_beam(data, x = 0, y = 0, reverse = False, part_two = False):
    results = []

    if not part_two:
        _traverse_x(data, x, y)
        result = calculate_energized_tiles(data)
        return result

    else:
        # Fire from the left 0, y
        for y in range(0, len(data)):
            test_data = copy.deepcopy(data)
            _traverse_x(test_data, 0, y)
            result = calculate_energized_tiles(test_data)
            results.append(result)
            # [_print(x, show_beam = True) for x in test_data]
            # print('\n')

        # Fire from the right len(data[0], y, reverse
        for y in range(0, len(data)):
            test_data = copy.deepcopy(data)
            _traverse_x(test_data, len(data) - 1, y, reverse = True)
            result = calculate_energized_tiles(test_data)
            results.append(result)
            # [_print(x, show_beam = True) for x in test_data]
            # print('\n')

        # Fire from the top, x, 0
        for x in range(0, len(data[0])):
            test_data = copy.deepcopy(data)
            _traverse_y(test_data, x, 0)
            result = calculate_energized_tiles(test_data)
            results.append(result)
            # [_print(x, show_beam = True) for x in test_data]
            # print('\n')

        # Fire from the bottom, x, len(data) reverse
        for x in range(0, len(data[0])):
            test_data = copy.deepcopy(data)
            _traverse_y(test_data, x, y, reverse = True)
            result = calculate_energized_tiles(test_data)
            results.append(result)
            # [_print(x, show_beam = True) for x in test_data]
            # print('\n')

    return max(results)


def parse_data(raw_data):
    data = deque([])

    for row_idx, row in enumerate(raw_data):
        datum = deque([])

        for col_idx, item in enumerate(row):
            cave_obj = CaveObject(row_idx, col_idx)
            if item != '.':
                cave_obj.add_content(item)

            datum.append(cave_obj)
        data.append(datum)

    return data



def main(raw_data, part_two = False):
    energized_tiles = []

    data = parse_data(raw_data)
    result = fire_beam(data, part_two=part_two)

    # [_print(x, show_beam = True) for x in data]
    print(f'\n{result} tiles end up being energized.')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_16_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = [line.rstrip() for line in input_file.readlines( )]

    # main(TEST_DATA)
    # main(raw_data)
    # main(TEST_DATA, part_two = True)
    main(raw_data, part_two = True)