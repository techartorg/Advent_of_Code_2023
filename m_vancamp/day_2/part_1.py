import dataclasses


@dataclasses.dataclass
class Game:
    ID: int
    Sets: list

    max_red = 12
    max_green = 13
    max_blue = 14

    @property
    def possible(self):
        return len(list(self.impossible_sets)) == 0

    @property
    def impossible_sets(self):
        for i in range(len(self.Sets)):
            if not self.Sets[i].possible(self.max_red, self.max_green, self.max_blue):
                yield i


@dataclasses.dataclass
class Set:
    Red: int = 0
    Green: int = 0
    Blue: int = 0

    def possible(self, max_red, max_green, max_blue):
        return self.Red <= max_red and self.Green <= max_green and self.Blue <= max_blue


with open("input.txt") as fp:
    data = fp.read()
    games = list()
    for line in data.splitlines():
        game_id = line.partition(":")[0].split(" ")[1]

        sets_data = line.partition(":")[2].split(";")
        sets = list()
        for set_data in sets_data:
            draws = set_data.split(",")
            new_set = Set()
            for draw in draws:
                number, colour = draw.strip().split(" ")
                number = int(number)
                if colour == "red":
                    new_set.Red = number
                elif colour == "green":
                    new_set.Green = number
                elif colour == "blue":
                    new_set.Blue = number
            sets.append(new_set)

        game = Game(int(game_id), sets)
        games.append(game)

result = 0
for game in games:
    if game.possible:
        result += game.ID

print(result)
