class Tile:
    # -- to be filled in by child classes
    Identifier = None
    # -- to be filled in by child classes
    # -- order: north, east, south, west.
    # -- this field indicates which of those directions support connectors for this type
    Connector_Slots: list = [0, 0, 0, 0]
    Connector_Directions: list = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.value = -1
        self.connectors: list = [None, None, None, None]

    def __repr__(self):
        return f'[{self.__class__.__name__}] ({self.column}, {self.row}) | Distance: {self.value} | Connectors: {self.connectors}'

    @property
    def neighbours(self):
        return list([
            connector
            for connector
            in self.connectors
            if connector is not None
        ])

class VerticalPipe(Tile):
    Identifier = '|'
    # -- support slots in north and south
    Connector_Slots = [1, 0, 1, 0]


class HorizontalPipe(Tile):
    Identifier = '-'
    # -- support slots in east and west
    Connector_Slots = [0, 1, 0, 1]


class NorthEastBend(Tile):
    Identifier = 'L'
    # -- north and east
    Connector_Slots = [1, 1, 0, 0]


class NorthWestBend(Tile):
    Identifier = 'J'
    # -- north and west
    Connector_Slots = [1, 0, 0, 1]


class SouthWestBend(Tile):
    Identifier = '7'
    # -- south and west
    Connector_Slots = [0, 0, 1, 1]


class SouthEastBend(Tile):
    Identifier = 'F'
    # -- South and East
    Connector_Slots = [0, 1, 1, 0]


class Ground(Tile):
    Identifier = '.'


class StartingTile(Tile):
    Identifier = 'S'


tile_factory = [
    HorizontalPipe,
    VerticalPipe,
    SouthEastBend,
    SouthWestBend,
    NorthEastBend,
    NorthWestBend,
    Ground,
    StartingTile
]


def tile_from_string(s) -> type:
    for cls in tile_factory:
        if cls.Identifier == s:
            return cls
    return None


class Grid:

    def __init__(self, num_rows, num_columns):
        self.height = num_rows
        self.width = num_columns

        self.rows = list()
        for y in range(num_rows):
            self.rows.append(list([None for _ in range(num_columns)]))

    def fetch_tile(self, x, y) -> Tile:
        if x < 0:
            return None
        if y < 0:
            return None
        if x > self.width - 1:
            return None
        if y > self.height - 1:
            return None
        return self.rows[y][x]

    def set_up_connections(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.fetch_tile(x, y)
                for i in range(len(tile.Connector_Directions)):
                    direction = tile.Connector_Directions[i]
                    if not any(tile.Connector_Slots):
                        continue
                    # -- leave the slot set to None if there's no connection supported
                    supports_slot = tile.Connector_Slots[i]
                    if supports_slot == 1:
                        neighbour = self.fetch_tile(x + direction[0], y + direction[1])
                        tile.connectors[i] = neighbour

        starting_tile = self.fetch_start_tile()
        x, y = starting_tile.column, starting_tile.row
        for direction in Tile.Connector_Directions:
            neighbour = self.fetch_tile(x + direction[0], y + direction[1])
            if not neighbour:
                continue

            # -- we only have to check in the cardinal directions, as we do not support diagonals
            if direction[0] != 0:
                idx = neighbour.Connector_Directions.index(
                    (-1 * direction[0], direction[1])
                )
                supports_connection = neighbour.Connector_Slots[idx]

                if not supports_connection:
                    continue

                starting_tile.connectors[idx] = neighbour

            elif direction[1] != 0:
                idx = neighbour.Connector_Directions.index(
                    (direction[0], -1 * direction[1])
                )
                supports_connection = neighbour.Connector_Slots[idx]

                if not supports_connection:
                    continue

                starting_tile.connectors[idx] = neighbour

    def add_tile_from_string(self, s: str, row: int, column: int):
        self.add_tile(tile_from_string(s)(column, row), row, column)

    def add_tile(self, tile: Tile, row: int, column: int):
        self.rows[row][column] = tile

    def fetch_start_tile(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.fetch_tile(x, y)
                if tile.Identifier == 'S':
                    return tile
        raise ValueError

    def value_field(self):
        s = ''
        for row in self.rows:
            s += (''.join(list([str(tile.value) if tile.value >= 0 else '.' for tile in row])))
            s += '\n'
        return s

    @property
    def all_tiles(self):
        result = list()
        for y in range(self.height):
            result += self.rows[y]
        return result

    def reset_tiles(self):
        # -- first reset all tile values
        for tile in self.all_tiles:
            tile.value = -1
            if tile.Identifier == 'S':
                tile.value = 0

    def fetch_tiles_by_value(self, value):
        for tile in self.all_tiles:
            if tile.value == value:
                yield tile

    def calculate_distance_values_from_coordinate(self, x, y):
        self.reset_tiles()

        current_value = 0

        while True:
            all_changes = list()
            for tile in self.fetch_tiles_by_value(current_value):
                current_value, changes = self.tick_neighbours(tile)
                all_changes.append(changes)

            if not all(all_changes):
                break

        return current_value

    @staticmethod
    def tick_neighbours(tile):
        changes = False
        for neighbour in tile.neighbours:
            # -- do not return to previously traversed tiles
            if neighbour.value != -1:
                continue
            neighbour.value = tile.value + 1
            changes = True

        return max(list([neighbour.value for neighbour in tile.neighbours])), changes


def load_data(is_test=False):
    with open('input.txt' if not is_test else 'test_input_2.txt') as fp:
        lines = list([line.strip() for line in fp.readlines()])

    num_columns = len(lines[0])
    num_rows = len(lines)

    grid = Grid(num_rows, num_columns)
    for x in range(num_columns):
        for y in range(num_rows):
            grid.add_tile_from_string(lines[y][x], y, x)

    grid.set_up_connections()

    return grid


if __name__ == '__main__':
    data_grid = load_data(False)
    start_tile = data_grid.fetch_start_tile()
    value = data_grid.calculate_distance_values_from_coordinate(start_tile.column, start_tile.row)

    print(data_grid.value_field())
    print(value)
