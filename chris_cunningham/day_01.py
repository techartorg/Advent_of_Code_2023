from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
words_to_nums = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def solve(d: dict[str, int]) -> int:
    def get(x):
        return x[0]

    result = 0

    for line in inputs:
        l_word = min(((i, v) for k, v in d.items() if (i := line.find(k)) != -1), key=get, default=(9001, 0))
        r_word = max(((i, v) for k, v in d.items() if (i := line.rfind(k)) != -1), key=get, default=(-1, 0))
        result += l_word[1] * 10 + r_word[1]

    return result


numbers = {str(i): i for i in range(1, 10)}
print(f"Part One: {solve(numbers)}")

print(f"Part Two: {solve(numbers | words_to_nums)}")
