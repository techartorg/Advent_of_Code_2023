from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
words_to_nums = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

part_one = 0
part_two = 0

empty = ((0, 0), 0)

for line in inputs:
    l_digit = min(((idx, c) for c in range(1, 10) if (idx := line.find(str(c))) != -1), key=lambda x: x[0], default=(9001, 0))
    r_digit = max(((idx, c) for c in range(1, 10) if (idx := line.rfind(str(c))) != -1), key=lambda x: x[0], default=(-1, 0))

    part_one += l_digit[1] * 10 + r_digit[1] if l_digit[0] != r_digit[0] else l_digit[1]

    l_word = min(((i, v) for k, v in words_to_nums.items() if (i := line.find(k)) != -1), key=lambda x: x[0], default=(9001, 0))
    r_word = max(((i, v) for k, v in words_to_nums.items() if (i := line.rfind(k)) != -1), key=lambda x: x[0], default=(-1, 0))

    lhs = l_word[1] if l_word[0] < l_digit[0] else l_digit[1]
    rhs = r_word[1] if r_word[0] > r_digit[0] else r_digit[1]
    part_two += lhs * 10 + rhs


print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")
