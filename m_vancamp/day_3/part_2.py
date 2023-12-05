import dataclasses
import re

with open("input.txt") as fp:
    data = fp.read()


lines = list(line.strip() for line in data.splitlines())


@dataclasses.dataclass
class Gear:
    Parts: list = None

    @property
    def ratio(self):
        if not len(self.Parts) == 2:
            return 0
        return self.Parts[0] * self.Parts[1]


gears = list()

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
    find_gears = re.compile(r"(\*)")

    for match in re.finditer(find_gears, line):
        idx = match.start()

        part = Gear()
        neighbours = list()

        for check in lines_to_check:
            numbers = re.finditer(find_numbers, check)

            for number in numbers:
                if number.span()[1] > idx - 1 and number.span()[0] <= idx + 1:
                    neighbours.append(int(number.groups()[0]))

        part.Parts = neighbours
        gears.append(part)


print(sum(list(gear.ratio for gear in gears)))
