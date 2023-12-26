import dataclasses


@dataclasses.dataclass
class Node:
    Name: str

    # -- these are simply string patterns to serve to fill node lookups later.
    left_node: str
    right_node: str

    # -- these are node lookups
    Left: object = None
    Right: object = None

    def go(self, direction):
        if direction == 'L':
            return self.go_left()
        if direction == 'R':
            return self.go_right()

    def go_left(self):
        return self.Left

    def go_right(self):
        return self.Right


def load_data(is_test=False):
    with open('input.txt' if not is_test else 'test_input.txt') as fp:
        lines = fp.readlines()

    loaded_instructions = lines[0].strip()
    nodes_data = list([line.strip() for line in lines[2:]])

    result = dict()

    for node_data in nodes_data:
        name, _, left_right = node_data.partition('=')
        name = name.strip()
        left, right = left_right.strip().strip('()').split(',')
        left, right = left.strip(), right.strip()

        result[name] = Node(name, left, right)

    # -- pair nodes with their lookups
    for node_name in result:
        result[node_name].Left = result[result[node_name].left_node]
        result[node_name].Right = result[result[node_name].right_node]

    return loaded_instructions, result


def traverse_nodes(instructions, nodes):
    current_node = nodes['AAA']

    counter = 1
    while current_node.Name != 'ZZZ':
        for i in range(len(instructions)):
            direction = instructions[i]
            current_node = current_node.go(direction)
            if current_node.Name == 'ZZZ':
                break
            counter += 1

    # -- this should not occur
    return counter


if __name__ == '__main__':
    inst, data = load_data(False)
    num_steps = traverse_nodes(inst, data)
    print(num_steps)
