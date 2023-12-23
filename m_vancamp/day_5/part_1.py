import dataclasses


@dataclasses.dataclass
class DataMap:
    ID: str
    RangeMaps: list

    TargetMap: object = None

    def map_value(self, value):
        for range_map in self.RangeMaps:
            if range_map.maps_value(value):
                return range_map.map_value(value)
        return value

    def lookup_value(self, value):
        for range_map in self.RangeMaps:
            if range_map.maps_value(value):
                return range_map.map_value(value)
        return value

    def traverse_value(self, value):
        lookup = self.lookup_value(value)
        if not self.TargetMap:
            return lookup
        return self.TargetMap.traverse_value(lookup)

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

    def maps_value(self, value):
        return self.SourceRangeStart <= value <= self.SourceRangeStart + self.Range

    def map_value(self, value):
        index = value - self.SourceRangeStart
        return self.DestinationRangeStart + index


is_test = False

with open("input.txt" if not is_test else "test_input.txt") as fp:
    data = fp.read()

# -- sanitize input
lines = list(line.strip() for line in data.splitlines())

seeds = list(int(seed) for seed in lines[0].partition(":")[2].split(" ") if seed)
maps = list()

current_map = None
for line in lines[1:]:
    if not line:
        if current_map:
            maps.append(current_map)
        current_map = None

    else:
        if not current_map:
            new_map_id = line.partition(" ")[0]
            current_map = DataMap(new_map_id, list())

        else:
            values = list(int(val) for val in line.split(" "))
            new_range = DataRangeMap(*values)
            current_map.RangeMaps.append(new_range)


# -- pair maps with their target, so we have a long chain of maps we can traverse like a tree
for a in maps:
    print(a)
    for b in maps:
        if a is b:
            continue
        if a.target_name == b.source_name:
            a.TargetMap = b
            break


seed_map = maps[0]

lookups = dict()
for seed_number in seeds:
    lookups[seed_number] = seed_map.traverse_value(seed_number)

print(min(lookups.values()))
