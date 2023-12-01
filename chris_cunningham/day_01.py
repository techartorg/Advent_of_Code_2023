from pathlib import Path

inputs = Path(__file__.replace(".py", ".input")).read_text().splitlines()
numbers = [
    *[str(i) for i in range(10)],
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
]


def solve(line: str, d: list[str]) -> int:
    def get(x: (int, int)) -> int:
        return x[0]

    lhs = min(((i, n % 10) for n, c in enumerate(d) if (i := line.find(c)) != -1), key=get, default=(len(line), 0))[1]
    rhs = max(((i, n % 10) for n, c in enumerate(d) if (i := line.rfind(c)) != -1), key=get, default=(-1, 0))[1]
    return lhs * 10 + rhs


print(f"Part One: {sum(solve(l, numbers[:10]) for l in inputs)}")
print(f"Part Two: {sum(solve(l, numbers) for l in inputs)}")
