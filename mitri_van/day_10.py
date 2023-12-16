#! python3.11
"""
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way
up to the floating metal island. This island is surprisingly cold and there
definitely aren't any thermals to glide on, so you leave your hang glider
behind.

You wander around for a while, but you don't find any people or animals.
However, you do occasionally find signposts labeled "Hot Springs" pointing
in a seemingly consistent direction; maybe you can find someone at the hot
springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal.
As you stop to admire some metal grass, you notice something metallic
scurry away in your peripheral vision and jump into a big pipe! It didn't
look like any animal you've ever seen; if you want a better look, you'll
need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is
densely packed with pipes; it was hard to tell at first because they're the
same metallic silver color as the "ground". You make a quick sketch of all
of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this
    tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe
that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch
would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell
because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop!
This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main
loop: they're the ones connected to S, pipes those pipes connect to, pipes
those pipes connect to, and so on. Every pipe in the main loop connects to
its two neighbors (including S, which will have exactly two pipes
connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles
also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in
the loop that is farthest from the starting position. Because the animal is in
the pipe, it doesn't make sense to measure this by direct distance.
Instead, you need to find the tile that would take the longest number of
steps along the loop to reach from the starting point - regardless of which
way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point
like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop
does it take to get from the starting position to the point farthest from
the starting position?

Your puzzle answer was 6947.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never
emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a
nest, you should calculate how many tiles are contained within the loop.
For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........

The above loop encloses merely four tiles - the two pairs of . in the
southwest and southeast (marked I below). The middle . tiles (marked O
below) are not in the loop. Here is the same loop again with those regions
marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....

In fact, there doesn't even need to be a full tile path to the outside for
tiles to count as outside the loop - squeezing between pipes is also
allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

The above sketch has many random bits of ground, some of which are in the
loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO

In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by
the loop. Here's another example with many bits of junk pipe lying around
that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L

In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the
area within the loop. How many tiles are enclosed by the loop?

"""
import copy

from collections import deque


TEST_DATA_1 = deque([ '-L|F7',
                      '7S-7|',
                      'L|7||',
                      '-L-J|',
                      'L|-JF'
                    ])

TEST_DATA_2 = deque([ '7-F7-',
                      '.FJ|7',
                      'SJLL7',
                      '|F--J',
                      'LJ.LJ'
                    ])

TEST_DATA_3 = deque([ '...........',
                      '.S-------7.',
                      '.|F-----7|.',
                      '.||.....||.',
                      '.||.....||.',
                      '.|L-7.F-J|.',
                      '.|..|.|..|.',
                      '.L--J.L--J.',
                      '...........'
                    ])

PIPE_MAP = { '|': [(0,1), (0,-1)],
             '7': [(0,1), (-1,0)],
             'F': [(0,1), (1,0)],
             '-': [(1,0), (-1,0)],
             'L': [(0,-1), (1,0)],
             'J': [(0,-1), (-1,0)],
           }



class Pipe():

    def __init__(self, id, prop_1, prop_2, quantity=1):
        self.id = id
        self.tunnel = []

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} ({self.prop_1},{self.prop_2})>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id} ({self.prop_1},\n\t\t\t\t{self.prop_2})>"


def _draw_map(data):
    for i in data:
        print(''.join(i))


def _map_tunnel_recurse(tunnel_data, prev_pos, current_tile, tunnel_map, tunnel_idx):

    move_a = PIPE_MAP[current_tile[0]][0]
    move_b = PIPE_MAP[current_tile[0]][1]

    new_pos = [sum(x) for x in zip(move_a, current_tile[1:])]
    if new_pos == prev_pos:
        new_pos = [sum(x) for x in zip(move_b, current_tile[1:])]

    new_tile = [tunnel_data[new_pos[1]][new_pos[0]], new_pos[0], new_pos[1]]

    if new_tile[0] != 'S':
        tunnel_idx += 1
        tunnel_idx = _map_tunnel(tunnel_data, current_tile[1:], new_tile, tunnel_map, tunnel_idx)

    return tunnel_idx#tunnel_map

def _map_tunnel(tunnel_data, prev_pos, current_tile, tunnel_map):
    new_tile = current_tile

    while new_tile[0] != 'S':
        move_a = PIPE_MAP[current_tile[0]][0]
        move_b = PIPE_MAP[current_tile[0]][1]

        new_pos = [sum(x) for x in zip(move_a, current_tile[1:])]
        if new_pos == prev_pos:
            new_pos = [sum(x) for x in zip(move_b, current_tile[1:])]

        new_tile = [tunnel_data[new_pos[1]][new_pos[0]], new_pos[0], new_pos[1]]

        tunnel_map.append(new_tile)

        # Reset variables for the next run
        prev_pos = current_tile[1:]
        current_tile = new_tile

    return tunnel_map


def render_map(data, tunnel_map):
    render = copy.deepcopy(data)

    for tile, x, y in tunnel_map:
        if tile == '|':
            render[y][x] = '║'
        elif tile == '7':
            render[y][x] = '┐'
        elif tile == 'F':
            render[y][x] = '┌'
        elif tile == '-':
            render[y][x] = '═'
        elif tile == 'L':
            render[y][x] = '└'
        elif tile == 'J':
            render[y][x] = '┘'
        else:
            pass

    return render


def calculate_area(data, tunnel_map):
    area = 0
    open_edge = False

    for row in data:
        in_interior = False
        for idx, tile in enumerate(row):
            x = idx
            y = data.index(row)
            if [tile, x, y] in tunnel_map:
                if tile[0] in ['S', '|', '7', 'F', 'J', 'L']:
                    if open_edge:
                        # in_interior = not in_interior
                        open_edge = False
                    else:
                        in_interior = not in_interior
                        if tile[0] in ['7', 'F', 'J', 'L']:
                            open_edge = True
                elif tile[0] == '-':
                    previous_pipe = tile[0]
                else:
                    pass # Do nothing with '-'
            elif in_interior:
                area += 1

    return area


def find_next_pipe_segment(data, start_pos):
    next_pipe = None
    prev_pipe = None

    x = start_pos[0]
    y = start_pos[1]

    # Check above
    tile = data[y - 1][x]
    if tile in ['|', 'F', '7']:
        if next_pipe is None:
            next_pipe = [tile, x, y - 1]
        else:
            prev_pipe = [tile, x, y - 1]

    # Check right
    tile = data[y][x + 1]
    if tile in ['-', 'J', '7']:
        if next_pipe is None:
            next_pipe = [tile, x + 1, y]
        else:
            prev_pipe = [tile, x + 1, y]

    # Check below
    tile = data[y + 1][x]
    if tile in ['|', 'J', 'L']:
        if next_pipe is None:
            next_pipe = [tile, x, y + 1]
        else:
            prev_pipe = [tile, x, y + 1]

    # Check left
    tile = data[y][x - 1]
    if tile in ['-', 'L', 'F']:
        if next_pipe is None:
            next_pipe = [tile, x - 1, y]
        else:
            prev_pipe = [tile, x - 1, y]


    return next_pipe, prev_pipe


def find_start(data):
    start_found = False
    start_pos = []

    while not start_found:
        for row in data:
            if 'S' in row:
                start_pos = [row.index('S'), data.index(row)]
        break

    next_pipe, prev_pipe = find_next_pipe_segment(data, start_pos)

    return start_pos, next_pipe, prev_pipe


def map_tunnel(data):
    start_pos = []
    tunnel_map = deque()
    tunnel_data = deque(copy.deepcopy(data))

    start_pos, next_pipe, prev_pipe = find_start(data)
    tunnel_map.append(['S', start_pos[0], start_pos[1]])
    tunnel_map.append(next_pipe)
    tunnel_idx = _map_tunnel(tunnel_data, start_pos, next_pipe, tunnel_map)

    return start_pos, tunnel_idx#tunnel_map


def parse_data(raw_data):
    # Parse raw_data into a usable form
    data = [deque([x for x in row]) for row in raw_data]

    return data


def main(raw_data, part_two = False):
    data = parse_data(raw_data)

    start_pos, tunnel_map = map_tunnel(data)
    render = render_map(data, tunnel_map)
    # _draw_map(render)
    area = calculate_area(data, tunnel_map)


    if not part_two:
        print(f'\nThe farthest point from the start is {int(len(tunnel_map)/2)} steps away')
    else:
        print(f'\n{area} tiles are enclosed by the loop')



if __name__ == "__main__":
    input = r"D:\Projects\Advent_of_Code\2023\day_10_input.txt"
    raw_data = []

    with open(input, "r") as input_file:
        raw_data = deque([line for line in input_file.readlines( )])

    # main(TEST_DATA_1)
    # main(TEST_DATA_2)
    # main(raw_data)
    # main(TEST_DATA_1, part_two = True)
    # main(TEST_DATA_2, part_two = True)
    main(TEST_DATA_3, part_two = True)
    # main(raw_data, part_two = True)