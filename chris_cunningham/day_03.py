from pathlib import Path
from typing import Iterator
from itertools import product
from math import prod

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()

Pt = tuple[int, int]
numbers: list[tuple[int, list[Pt]]] = []
symbols: set[Pt] = set()
gears: set[Pt] = set()
pts_to_numbers: dict[Pt, int] = {}


def neighbours(point: Pt) -> Iterator[Pt]:
    x, y = point
    for offset_x, offset_y in product([-1, 0, 1], repeat=2):
        yield x + offset_x, y + offset_y


def is_adjacent(number: tuple[int, list[Pt]]) -> bool:
    _, coords = number
    return any(any(pt in symbols for pt in neighbours(start)) for start in coords)


for y, line in enumerate(inputs):
    num_buff: str = ""
    num_pts: list[Pt] = []

    for x, char in enumerate(line):
        if char.isdigit():
            num_buff += char
            num_pts.append((x, y))
            continue

        if not char.isdigit() and num_buff != "":
            new_number = int(num_buff)
            numbers.append((int(num_buff), [*num_pts]))
            pts_to_numbers |= {i: new_number for i in num_pts}
            num_buff = ""
            num_pts.clear()

        if char != ".":
            symbols.add((x, y))

        if char == "*":
            gears.add((x, y))

    if num_buff != "":
        new_number = int(num_buff)
        numbers.append((int(num_buff), [*num_pts]))
        pts_to_numbers |= {i: new_number for i in num_pts}

part_one = sum(i[0] for i in numbers if is_adjacent(i))
print(f"Part One: {part_one}")

part_two = 0
for gear in gears:
    ratios = set(r for i in neighbours(gear) if (r := pts_to_numbers.get(i, 0)) != 0)
    if len(ratios) == 2:
        part_two += prod(ratios)

print(f"Part Two: {part_two}")
