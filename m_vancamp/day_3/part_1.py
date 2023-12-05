import dataclasses
import re

with open("input.txt") as fp:
    data = fp.read()


lines = list(line.strip() for line in data.splitlines())


@dataclasses.dataclass
class Part:
    ID: int
    Neighbours: list = None


parts = list()

for i in range(len(lines)):
    lines_to_check = list()
    if i > 0:
        lines_to_check.append(lines[i-1])
    lines_to_check.append(lines[i])
    if i < (len(lines) - 1):
        lines_to_check.append(lines[i + 1])

    line = lines[i]

    find_numbers = re.compile(r"([0-9]+)")
    # -- this sequence captures anything except periods and numerals
    find_symbols = re.compile(r"([^0-9\.])")

    for match in re.finditer(find_numbers, line):
        span = list(match.span())

        start = span[0] - 1 if span[0] > 0 else 0
        end = span[1] + 1 if span[1] < len(line) else len(line)

        part = Part(int(match.groups()[0]))
        neighbours = list()

        for check in lines_to_check:
            for index in range(start, end):
                if check[index] != "." and not check[index].isdigit():
                    neighbours.append(check[index])

        part.Neighbours = neighbours
        parts.append(part)


print(sum(list(gear.ID for gear in parts if len(gear.Neighbours))))
