from pathlib import Path
from math import pow

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
_test = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()

games: list[int] = []

for line in inputs:
    numbers = line.split(": ")[1].split(" | ")
    winning, have = [set(int(j) for j in i.split()) for i in numbers]
    games.append(len(winning & have))

part_one = sum(int(pow(2, i - 1)) for i in games)
print(f"Part One: {part_one}")

stack: list[int] = [*range(len(games))]
part_two = 0

while stack:
    card_num = stack.pop(0)
    part_two += 1
    matches = games[card_num]

    if matches:
        stack = [*range(card_num + 1, card_num + 1 + matches), *stack]

print(f"Part Two: {part_two}")
