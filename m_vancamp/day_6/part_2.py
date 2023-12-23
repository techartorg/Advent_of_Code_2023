import dataclasses


def get_distance_traveled(time_button_held, race_duration):
    duration = max(0, race_duration - time_button_held)
    return time_button_held * duration


@dataclasses.dataclass
class Race:
    Duration: int = -1
    RecordDistance: int = -1

    def nr_winning_conditions(self):
        min_winning_duration = -1
        max_winning_duration = self.Duration

        iterations = 0

        i = 0
        while min_winning_duration == -1:
            if get_distance_traveled(i, self.Duration) > self.RecordDistance:
                min_winning_duration = i
            i += 1
            iterations += 1

        i = self.Duration
        while max_winning_duration == self.Duration:
            if get_distance_traveled(i, self.Duration) > self.RecordDistance:
                max_winning_duration = i
            i -= 1
            iterations += 1

        print(min_winning_duration, max_winning_duration, iterations)

        return max_winning_duration - min_winning_duration + 1


def load_data(is_test=False):
    with open('input.txt' if not is_test else 'test_input.txt') as fp:
        lines = fp.readlines()
    duration = int(lines[0].strip().partition(':')[2].replace(' ', ''))
    distance = int(lines[1].strip().partition(':')[2].replace(' ', ''))
    return Race(duration, distance)


if __name__ == '__main__':
    race_data = load_data(False)
    print(race_data.nr_winning_conditions())
