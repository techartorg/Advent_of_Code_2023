from __future__ import annotations

from pathlib import Path
from functools import reduce, partial
from typing import Callable

inputs = Path(__file__.replace(".py", ".input")).read_text().split("\n\n")


def range_intersection(lhs: range, rhs: range) -> range | None:
    start = max(lhs.start, rhs.start)
    end = min(lhs.stop, rhs.stop)
    return range(start, end) if end >= start else None


def range_difference(lhs: range, rhs: range) -> list[range]:
    if lhs.start < rhs.start <= lhs.stop <= rhs.stop:
        return [range(lhs.start, rhs.start)]
    elif rhs.start <= lhs.start < rhs.stop < lhs.stop:
        return [range(rhs.stop, lhs.stop)]
    elif lhs.start < rhs.start < rhs.stop < lhs.stop:
        return [range(lhs.start, rhs.start), range(rhs.stop, lhs.stop)]
    elif rhs.start <= lhs.start <= lhs.stop <= rhs.stop:
        return []
    else:
        return [lhs]


class ConverterRange(object):
    src: range
    dst: int

    def __init__(self, dst: int, src: int, _len: int):
        self.dst = dst
        self.src = range(src, src + _len)

    def map_value(self, value: int) -> int | None:
        return value - self.src.start + self.dst if value in self.src else None

    def map_range(self, value: range) -> tuple[range, list[range]] | None:
        inter = range_intersection(value, self.src)
        diff = range_difference(value, self.src)
        return (inter, diff) if inter else None


class Converter(object):
    _ranges: list[ConverterRange]

    def __init__(self, ranges: list[ConverterRange]):
        self._ranges = ranges

    @classmethod
    def parse(cls, data: str) -> Converter:
        return Converter([ConverterRange(*[int(i) for i in line.split(" ")]) for line in data.splitlines()[1:]])

    def map_value(self, value: int) -> int:
        for rng in self._ranges:
            if (new_value := rng.map_value(value)) is not None:
                return new_value
        return value

    def map_range(self, seeds: list[range]) -> list[range]:
        seeds = seeds[:]
        new = []

        while seeds:
            s = seeds.pop()
            for r in self._ranges:
                mapped = r.map_range(s)
                if mapped:
                    inter, diff = mapped
                    new.append(range(r.map_value(inter.start), r.map_value(inter.stop - 1)))
                    seeds += diff
                    break
            else:
                new.append(s)

        return new


converters = [Converter.parse(i) for i in inputs[1:]]

single_converter: Callable[[int], int] = partial(reduce, lambda x, y: y.map_value(x), converters)
seed_nums = [int(i) for i in inputs[0].split(": ")[1].split(" ")]
part_one = min(single_converter(i) for i in seed_nums)
print(f"Part One: {part_one}")

range_converter: Callable[[list[range]], list[range]] = partial(reduce, lambda x, y: y.map_range(x), converters)
seed_iter = iter(seed_nums)
seed_ranges = [range(i, i + next(seed_iter)) for i in seed_iter]

part_two = min(i.start for i in range_converter(seed_ranges))
print(f"Part Two: {part_two}")
