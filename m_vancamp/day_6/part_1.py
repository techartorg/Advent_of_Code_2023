import dataclasses


def get_distance_traveled(time_button_held, race_duration):
    duration = max(0, race_duration - time_button_held)
    return time_button_held * duration


@dataclasses.dataclass
class Race:
    Duration: int = -1
    RecordDistance: int = -1

    def winning_conditions(self):
        result = list()

        for i in range(self.Duration):
            if get_distance_traveled(i, self.Duration) > self.RecordDistance:
                result.append([i, get_distance_traveled(i, self.Duration)])

        return result


def load_data(is_test=False):
    with open('input.txt' if not is_test else 'test_input.txt') as fp:
        lines = fp.readlines()

    durations = list([int(d) for d in lines[0].strip().partition(':')[2].split(' ') if d])
    distances = list([int(d) for d in lines[1].strip().partition(':')[2].split(' ') if d])

    races = list()

    for i in range(len(durations)):
        races.append(Race(durations[i], distances[i]))

    return races


if __name__ == '__main__':
    race_data = load_data(True)

    number = 1
    for race in race_data:
        print(race, race.winning_conditions())
        number *= len(race.winning_conditions())
    print(number)
