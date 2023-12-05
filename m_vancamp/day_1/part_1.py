with open("input.txt") as fp:
    lines = fp.readlines()

numerals = list(set("0123456789"))

result = 0

for line in lines:
    line = line.strip('\n')
    digits = [c for c in line if c in numerals]
    if not digits:
        raise Exception(f"No digits found in line {line}")
    number = int(digits[0] + digits[-1])
    result += number

print(result)
