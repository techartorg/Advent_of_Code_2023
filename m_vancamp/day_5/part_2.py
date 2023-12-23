import dataclasses
import random


@dataclasses.dataclass
class DataMap:
    ID: str
    RangeMaps: list

    TargetMap: object = None
    _cache: dict = None

    def __init__(self, map_id, range_maps):
        self.ID = map_id
        self.RangeMaps = sorted(range_maps)
        self._cache = dict()

    def lookup_value(self, value):
        start_index = 0
        half_index = int(len(self.RangeMaps) / 2.0)

        if value > self.RangeMaps[half_index].SourceRangeStart:
            start_index = half_index

        for index in range(start_index, len(self.RangeMaps)):
            if self.RangeMaps[index].maps_value(value):
                return self.RangeMaps[index].map_value(value)

        return value

    def traverse_value(self, value):
        if self._cache.get(value):
            return self._cache.get(value)

        lookup = self.lookup_value(value)
        if not self.TargetMap:
            self._cache[value] = lookup
            return lookup

        # print(self.ID, value, lookup)

        result = self.TargetMap.traverse_value(lookup)
        self._cache[value] = result

        return result

    @property
    def source_name(self):
        return self.ID.split("-")[0]

    @property
    def target_name(self):
        return self.ID.split("-")[2]


@dataclasses.dataclass
class DataRangeMap:
    DestinationRangeStart: int = -1
    SourceRangeStart: int = -1
    Range: int = 0

    SourceRangeEnd: int = -1

    def __lt__(self, other):
        return self.SourceRangeStart < other.SourceRangeStart

    def maps_value(self, value):
        return self.SourceRangeStart <= value <= self.SourceRangeEnd

    def map_value(self, value):
        index = value - self.SourceRangeStart
        return self.DestinationRangeStart + index


def setup_data(is_test=False):
    with open("input.txt" if not is_test else "test_input.txt") as fp:
        data = fp.read()

    # -- sanitize input
    lines = list(line.strip() for line in data.splitlines())

    _seeds = list(int(seed) for seed in lines[0].partition(":")[2].split(" ") if seed)

    seed_maps = list()

    current_map = None
    for line in lines[1:]:
        if not line:
            if current_map:
                current_map.RangeMaps = sorted(current_map.RangeMaps)
                seed_maps.append(current_map)
            current_map = None

        else:
            if not current_map:
                new_map_id = line.partition(" ")[0]
                current_map = DataMap(new_map_id, list())

            else:
                values = list(int(val) for val in line.split(" "))
                new_range = DataRangeMap(*values)
                new_range.SourceRangeEnd = new_range.SourceRangeStart + new_range.Range
                current_map.RangeMaps.append(new_range)

    # -- pair maps with their target, so we have a long chain of maps we can traverse like a tree
    for a in seed_maps:
        for b in seed_maps:
            if a is b:
                continue
            if a.target_name == b.source_name:
                a.TargetMap = b
                break

    return _seeds, seed_maps


def process_data(start_seed_nr, nr_seeds, tree):
    lookups = dict()

    for j in range(nr_seeds):
        index = start_seed_nr + j
        lookups[index] = tree.traverse_value(index)
        # print("----------")
        if j % 100000 == 0.0:
            print(j, nr_seeds, f'{float(j) / float(nr_seeds)}')

    return lookups


# this theoretically works but it's much too slow. would have to rewrite it, but abandoning for now.
if __name__ == "__main__":
    seeds, maps = setup_data(is_test=False)
    seed_map = maps[0]

    import cProfile
    profile = cProfile.Profile()
    profile.enable()

    seed_lookups = dict()

    for i in range(int(float(len(seeds)) / 2.0)):
        start = seeds[i * 2]
        seed_nr = seeds[i * 2 + 1]
        print(i, start, seed_nr)
        seed_lookups.update(process_data(start, seed_nr, seed_map))

    profile.disable()
    profile.print_stats("cumtime")

    print(min(seed_lookups.values()))
