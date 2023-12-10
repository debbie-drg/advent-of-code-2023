import sys

CONNECTIONS = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    ".": [],
}

NEIGHBOURS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def sum_duples(duple_1: (int, int), duple_2: (int, int)) -> (int, int):
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(location: (int, int)) -> list[(int, int)]:
    return [sum_duples(location, neighbour) for neighbour in NEIGHBOURS]


def connected_to(location: (int, int), pipe_type: str) -> list[(int, int)]:
    return [sum_duples(location, connection) for connection in CONNECTIONS[pipe_type]]


class PipeSystem:
    def __init__(self, pipe_map: list[str]) -> None:
        self.pipe_map = pipe_map
        for index in range(len(self.pipe_map)):
            if "S" in self.pipe_map[index]:
                self.start_position = (index, self.pipe_map[index].index("S"))
        self.infer_start()
        self.main_loop = []

    def pipe_in_position(self, position: (int, int)) -> str:
        return self.pipe_map[position[0]][position[1]]

    def change_in_position(self, position: (int, int), pipe_type: str) -> None:
        self.pipe_map[position[0]] = (
            self.pipe_map[position[0]][: position[1]]
            + pipe_type
            + self.pipe_map[position[0]][(position[1] + 1) :]
        )

    def infer_start(self):
        for connection_type in CONNECTIONS:
            connected_to_start = connected_to(self.start_position, connection_type)
            if all(
                [
                    self.start_position
                    in connected_to(neighbour, self.pipe_in_position(neighbour))
                    for neighbour in connected_to_start
                ]
            ):
                self.change_in_position(self.start_position, connection_type)
                return

    def connected_to(self, position: (int, int)):
        return connected_to(position, self.pipe_in_position(position))

    def max_distance(self) -> int:
        count = 0
        next_neighbours = self.connected_to(self.start_position)
        previous_neighbours = next_neighbours
        while True:
            self.main_loop.extend(next_neighbours)
            if next_neighbours[0] == next_neighbours[1]:
                count += 1
                break
            if next_neighbours[0] in self.connected_to(next_neighbours[1]):
                break
            count += 1
            neighbours_0 = self.connected_to(next_neighbours[0])
            neighbours_1 = self.connected_to(next_neighbours[1])
            new_neighbours = []
            if neighbours_0[0] in previous_neighbours:
                new_neighbours.append(neighbours_0[1])
            else:
                new_neighbours.append(neighbours_0[0])
            if neighbours_1[0] in previous_neighbours:
                new_neighbours.append(neighbours_1[1])
            else:
                new_neighbours.append(neighbours_1[0])
            previous_neighbours = next_neighbours
            next_neighbours = new_neighbours
        self.main_loop = set(self.main_loop)
        return count

    def remove_junk(self):
        if isinstance(self.main_loop, list):
            self.max_distance()
        for index_1 in range(len(self.pipe_map)):
            for index_2 in range(len(self.pipe_map[0])):
                if (index_1, index_2) not in self.main_loop:
                    self.change_in_position((index_1, index_2), ".")

    def count_inside(self):
        self.remove_junk()
        count = 0
        for row in self.pipe_map:
            inside = False
            for char in row:
                if char == "." and inside:
                    count += 1
                if char in ["|", "L", "J"]:
                    inside = not inside
        return count

    def __repr__(self) -> str:
        to_return = "".join([line + "\n" for line in self.pipe_map])
        return to_return + f"Start position: {self.start_position}"


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    pipes = open(file_name).read().strip().split(sep="\n")
    pipe_system = PipeSystem(pipes)
    print(
        f"The maximum distance to a point within the loop is {pipe_system.max_distance()}"
    )
    print(f"The number of tiles inside the loop is {pipe_system.count_inside()}")
