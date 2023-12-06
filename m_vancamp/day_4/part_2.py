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

    _Value: int = -1

    def copy(self):
        return Game(self.ID, self.WinningNumbers, self.Numbers)

    @property
    def value(self):
        if self._Value != -1:
            return self._Value

        self._Value = 0

        for number in self.Numbers:
            if number in self.WinningNumbers:
                self._Value += 1

        return self._Value


games = dict()

for line in lines:
    capture_groups = test_regex if is_test else true_regex
    for match in re.finditer(capture_groups, line):
        game_id = int(match.groups()[0])
        winning_numbers = list(int(nr) for nr in match.groups()[1].strip().split(" ") if nr)
        game_numbers = list(int(nr) for nr in match.groups()[3].strip().split(" ") if nr)

        game = Game(game_id, winning_numbers, game_numbers)
        games[game_id] = game


nr_games = len(games)

game_ids = list(games.keys())

# -- initialize card counter
game_counter = dict()
for game_id in game_ids:
    game_counter[game_id] = 1


for game_id in game_ids:
    print(game_id)
    game = games[game_id]
    if not game.value:
        continue

    for iteration in range(game_counter[game_id]):
        for j in range(game.value):
            index = game_id + j + 1
            if index > nr_games:
                continue
            game_counter[index] += 1


value = 0
for game_id in game_counter:
    print(game_id, game_counter[game_id])
    value += game_counter[game_id]
print(value)
