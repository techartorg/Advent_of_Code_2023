written_numerals = {
    "one": "o1ne",
    "two": "t2o",
    "three": "thr3e",
    "four": "f4ur",
    "five": "f5ve",
    "six": "s6x",
    "seven": "s7ven",
    "eight": "e8ght",
    "nine": "n9ne",
}


with open("input.txt") as fp:
    data = fp.read()
    for wn, sub in written_numerals.items():
        data = data.replace(wn, sub)
    lines = data.splitlines()

numerals = list("123456789")

result = 0

for line in lines:
    line = line.strip('\n')

    digits = [c for c in line if c in numerals]
    if not digits:
        raise Exception(f"No digits found in line {line}")

    number = int(digits[0] + digits[-1])
    result += number

print(result)
