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


def get(x: (int, int)) -> int:
    return x[0]


def solve(line: str, d: dict[str, int]) -> int:
    l_word = min(((i, v) for k, v in d.items() if (i := line.find(k)) != -1), key=get, default=(len(line), 0))
    r_word = max(((i, v) for k, v in d.items() if (i := line.rfind(k)) != -1), key=get, default=(-1, 0))
    return l_word[1] * 10 + r_word[1]


numbers = {str(i): i for i in words_to_nums.values()}
print(f"Part One: {sum(solve(l, numbers) for l in inputs)}")
print(f"Part Two: {sum(solve(l, numbers | words_to_nums) for l in inputs)}")
