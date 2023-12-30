import dataclasses


@dataclasses.dataclass
class Record:
    values: list = None

    @classmethod
    def derive_values(cls, values):
        result = list()
        for i in range(1, len(values)):
            result.append(values[i] - values[i-1])
        return result

    @classmethod
    def predict_derivation(cls, derivations, values):
        return values[-1] + derivations[-1]

    def predict_value(self):
        derivations = list()

        done = False
        values = self.values
        while not done:
            values = self.derive_values(values)
            derivations.append(values[:])
            done = all([v == 0 for v in values])

        derivations[-1].append(0)
        derivations.insert(0, self.values)

        result = derivations[-1]
        for derivation in list(reversed(derivations))[1:]:
            val = self.predict_derivation(result, derivation)
            result = derivation[:] + [val]

        return result[-1]


def load_data(is_test=False):
    with open('input.txt' if not is_test else 'test_input.txt') as fp:
        lines = fp.readlines()

    records = list()
    for line in lines:
        values = [int(v) for v in line.split(' ')]
        records.append(Record(values))

    return records


if __name__ == '__main__':
    data = load_data(False)
    print(sum(list([record.predict_value() for record in data])))
