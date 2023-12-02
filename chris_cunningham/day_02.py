from pathlib import Path
from enum import StrEnum, auto
from collections import defaultdict
from math import prod

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
_test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()


class Color(StrEnum):
    Red = auto()
    Green = auto()
    Blue = auto()


Match = dict[Color, int]
Game = list[Match]

limits = {
    Color.Red: 12,
    Color.Green: 13,
    Color.Blue: 14
}


def parse_games(data: list[str]) -> list[Game]:
    result = []
    for line in data:
        _, game = line.split(": ")

        matches = []
        for m in game.split("; "):
            round_dict: defaultdict[Color, int] = defaultdict(int)

            for pair in m.split(", "):
                count, color = pair.split(" ")
                round_dict[Color(color)] = int(count)

            matches.append(round_dict)
        result.append(matches)
    return result


part_one = 0
part_two = 0

for game_num, game in enumerate(parse_games(inputs), start=1):
    g = {Color.Red: 0, Color.Green: 0, Color.Blue: 0}
    isPossible = True
    part_one += game_num

    for match in game:
        g[Color.Red] = max(g[Color.Red], match[Color.Red])
        g[Color.Green] = max(g[Color.Green], match[Color.Green])
        g[Color.Blue] = max(g[Color.Blue], match[Color.Blue])

        if isPossible and any(g[col] > limits[col] for col, count in g.items()):
            isPossible = False
            part_one -= game_num

    part_two += prod(g.values())

print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")
