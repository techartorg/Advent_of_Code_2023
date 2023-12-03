from pathlib import Path
from collections import defaultdict
from math import prod

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
Match = dict[str, int]
Game = list[Match]

limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}


def parse_games(data: list[str]) -> list[Game]:
    result = []
    for line in data:
        _, game = line.split(": ")
        if not game.strip():
            continue

        matches = []
        for m in game.split("; "):
            round_dict: defaultdict[str, int] = defaultdict(int)

            for pair in m.split(", "):
                count, color = pair.split(" ")
                round_dict[str(color)] = int(count)

            matches.append(round_dict)
        result.append(matches)
    return result


part_one = 0
part_two = 0

for game_num, game in enumerate(parse_games(inputs), start=1):
    g = {"red": 0, "green": 0, "blue": 0}
    is_possible = True
    part_one += game_num

    for match in game:
        g["red"] = max(g["red"], match["red"])
        g["green"] = max(g["green"], match["green"])
        g["blue"] = max(g["blue"], match["blue"])

        if is_possible and any(g[col] > limits[col] for col, count in g.items()):
            is_possible = False
            part_one -= game_num

    part_two += prod(g.values())

print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")
