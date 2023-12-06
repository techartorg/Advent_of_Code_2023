import re
import dataclasses

is_test = False

test_input = "_test_input_1.txt"
true_input = "input.txt"

test_regex = re.compile(r"(?:Card {1,}([0-9]{1,})\:) *(([0-9]{1,} {1,}){5})\| {1,}(([0-9]{1,} *){8})")
true_regex = re.compile(r"(?:Card {1,}([0-9]{1,})\:) *(([0-9]{1,} {1,}){10})\| {1,}(([0-9]{1,} *){25})")


with open(test_input if is_test else true_input) as fp:
    data = fp.read()

lines = list(line.strip() for line in data.splitlines())


@dataclasses.dataclass
class Game:
    ID: int
    WinningNumbers: list
    Numbers: list

    @property
    def value(self):
        result = 0

        for number in self.Numbers:
            if number in self.WinningNumbers:
                if result == 0:
                    result = 1
                else:
                    result *= 2

        return result


games = list()

for line in lines:
    capture_groups = test_regex if is_test else true_regex
    for match in re.finditer(capture_groups, line):
        game_id = int(match.groups()[0])
        winning_numbers = list(int(nr) for nr in match.groups()[1].strip().split(" ") if nr)
        game_numbers = list(int(nr) for nr in match.groups()[3].strip().split(" ") if nr)

        game = Game(game_id, winning_numbers, game_numbers)
        games.append(game)

print(sum(list(game.value for game in games)))
