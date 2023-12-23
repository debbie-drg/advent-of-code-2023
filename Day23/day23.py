import sys


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


DIRECTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}
DIRECTION_SIGN = {
    (1, 0): {"v": 1, "^": -1, ".": 0},
    (-1, 0): {"v": -1, "^": 1, ".": 0},
    (0, 1): {">": 1, "<": -1, ".": 0},
    (0, -1): {">": -1, "<": 1, ".": 0},
}


class Intersection:
    def __init__(
        self,
        position: tuple[int, int],
    ) -> None:
        self.position = position
        self.parents = set()
        self.children = set()

    def __hash__(self) -> int:
        return self.position.__hash__()

    def __repr__(self) -> str:
        return f"Intersection at {self.position} with parents {self.parents} and children {self.children}"


class Maze:
    def __init__(self, maze_map: list[str]) -> None:
        self.intersections = dict()
        self.maze_map = maze_map
        self.build_graph()

    def contiguous_trails(
        self,
        location: tuple[int, int],
        previous_intersection: tuple[int, int],
    ) -> list[tuple[tuple[int, int], int]]:
        neighbours = []
        for direction in DIRECTIONS:
            next_pos = sum_duples(location, direction)
            if next_pos in self.visited and not next_pos in self.intersections:
                continue
            if next_pos == previous_intersection:
                continue
            try:
                character = self.maze_map[next_pos[0]][next_pos[1]]
            except IndexError:
                neighbours.append((next_pos, -2))
                continue
            if character == "#":
                continue
            sign = DIRECTION_SIGN[direction][character]
            neighbours.append((next_pos, sign))
        return neighbours

    def build_graph(self):
        location = (0, 1)
        self.intersections[location] = Intersection(location)
        self.visited = set()
        self.visited.add(location)
        next_position, next_sign = self.contiguous_trails(location, location)[0]
        # Format: location, last intersection, distance, sign
        queue = [(next_position, location, 1, next_sign)]
        while queue:
            location, previous_node, distance, sign = queue.pop()
            if sign == -2:
                self.intersections[location] = Intersection(location)
                self.exit = location
                self.intersections[location].parents.add((previous_node, distance - 1))
                self.intersections[previous_node].children.add((location, distance - 1))
                continue
            self.visited.add(location)
            next_positions = self.contiguous_trails(location, previous_node)
            if len(next_positions) > 1 or location in self.intersections:
                add_to_queue = False
                if not location in self.intersections:
                    self.intersections[location] = Intersection(location)
                    add_to_queue = True
                if sign != -1:
                    self.intersections[previous_node].children.add((location, distance))
                    self.intersections[location].parents.add((previous_node, distance))
                if sign != 1:
                    self.intersections[previous_node].parents.add((location, distance))
                    self.intersections[location].children.add((previous_node, distance))
                distance = 0
                previous_node = location
                sign = 0
            else:
                add_to_queue = True
            distance += 1
            if not add_to_queue:
                continue
            for position, location_sign in next_positions:
                new_sign = sign if location_sign == 0 else location_sign
                queue.append((position, previous_node, distance, new_sign))

    def scenic_path(self):
        visited = set()
        location = (0, 1)
        return self.max_path_to_exit(visited, location)[0]

    def max_path_to_exit(
        self, visited: set, location: tuple[int, int]
    ) -> tuple[int, list[tuple[int, int]]]:
        nodes = [
            node
            for node in self.intersections[location].children
            if node not in visited
        ]
        if not nodes:
            return 0, [location]
        max_distance = 0
        for position, distance in nodes:
            if position == self.exit:
                return distance, [location, self.exit]
            next_distance, path = self.max_path_to_exit(
                visited.union([location]), position
            )
            next_distance = distance + next_distance
            if next_distance > max_distance:
                max_distance = next_distance
                max_path = path
        return max_distance, [location] + max_path


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    maze_map = open(file_name).read().strip().splitlines()
    maze = Maze(maze_map)
    print(f"The maximum distance is {maze.scenic_path()}")
