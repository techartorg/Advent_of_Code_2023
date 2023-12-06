from math import sqrt, ceil, prod
from pathlib import Path

inputs = [i.split(':')[1].strip() for i in Path(__file__.replace(".py", ".input")).read_text().splitlines()]


def solve_quad(time: int, distance: int) -> int:
    root = 0.5 * sqrt(time**2 - 4.0 * distance)
    _min = int(time * 0.5 - root) + 1
    _max = int(ceil(time * 0.5 + root)) - 1
    return _max - _min + 1


short_races = zip(*((int(i) for i in line.split()) for line in inputs))
part_one = int(prod(solve_quad(t, d) for t, d in short_races))
print(f"Part One: {part_one}")

long_race = tuple(int(i.replace(" ", "")) for i in inputs)
part_two = int(solve_quad(long_race[0], long_race[1]))
print(f"Part Two: {part_two}")
