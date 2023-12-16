import sys
from multiprocessing import Pool

DIRECTIONS = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
MIRROR_DIRECTIONS = {
    "/": {"E": "N", "N": "E", "S": "W", "W": "S"},
    "\\": {"N": "W", "W": "N", "S": "E", "E": "S"},
}

SPLIT_DIRECTIONS = {
    "|": {"N": ["N", "O"], "S": ["S", "O"], "E": ["N", "S"], "W": ["N", "S"]},
    "-": {"N": ["E", "W"], "S": ["E", "W"], "E": ["E", "O"], "W": ["W", "O"]},
}


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class Beam:
    def __init__(
        self, location: tuple[int, int] = (0, 0), direction: str = "E"
    ) -> None:
        self.location = location
        self.direction = direction

    def next_location(self) -> tuple[int, int]:
        return sum_duples(self.location, DIRECTIONS[self.direction])

    def move(self, next_location_symbol: str) -> str:
        next_location = self.next_location()
        self.location = next_location
        if next_location_symbol in ["|", "-"]:
            directions = SPLIT_DIRECTIONS[next_location_symbol][self.direction]
            self.direction = directions[0]
            return directions[1]
        if next_location_symbol in ["/", "\\"]:
            self.direction = MIRROR_DIRECTIONS[next_location_symbol][self.direction]
        return "O"


class MirrorMap:
    def __init__(self, map: list[str]):
        self.map = map
        self.width = len(self.map[0])
        self.depth = len(self.map)

    def position_in_map(self, position: tuple[int, int]) -> bool:
        if position[0] < 0:
            return False
        if position[1] < 0:
            return False
        if position[0] >= self.depth:
            return False
        if position[1] >= self.width:
            return False
        return True

    def count_energized(
        self, start_position: tuple[int, int] = (0, 0), start_direction: str = "E"
    ) -> int:
        history = set()
        visited = set()
        beams = self.start_beams(start_position, start_direction)
        visited.add(beams[0].location)
        while beams:
            beam = beams.pop()
            next_location = beam.next_location()
            if not self.position_in_map(next_location):
                continue
            next_location_symbol = self.map[next_location[0]][next_location[1]]
            new_beam_direction = beam.move(next_location_symbol)
            if ((next_location, beam.direction)) in history:
                continue
            history.add((next_location, beam.direction))
            beams.append(beam)
            if new_beam_direction != "O":
                beams.append(Beam(next_location, new_beam_direction))
            visited.add(next_location)
        return len(visited)

    def start_beams(
        self, start_position: tuple[int, int] = (0, 0), start_direction: str = "E"
    ) -> list[Beam]:
        start_position_tile = self.map[start_position[0]][start_position[1]]
        move_direction = DIRECTIONS[start_direction]
        pre_start_position = (
            start_position[0] - move_direction[0],
            start_position[1] - move_direction[1],
        )
        beam = Beam(pre_start_position, start_direction)
        second_beam_direction = beam.move(start_position_tile)
        beams = [beam]
        if second_beam_direction != "O":
            beams.append(Beam(start_position, second_beam_direction))
        return beams

    def start_north(self, position: tuple[int, int]) -> int:
        return self.count_energized(position, "S")

    def start_south(self, position: tuple[int, int]) -> int:
        return self.count_energized(position, "N")

    def start_east(self, position: tuple[int, int]) -> int:
        return self.count_energized(position, "W")

    def start_west(self, position: tuple[int, int]) -> int:
        return self.count_energized(position, "E")

    def check_all(self) -> int:
        pool = Pool(8)

        row_starts = [(row, 0) for row in range(self.depth)]
        max_left = max(pool.map(self.start_west, row_starts))

        row_ends = [(row, self.width - 1) for row in range(self.depth)]
        max_right = max(pool.map(self.start_east, row_ends))

        column_starts = [(0, col) for col in range(self.width)]
        max_top = max(pool.map(self.start_north, column_starts))

        column_ends = [(self.depth - 1, col) for col in range(self.width)]
        max_bottom = max(pool.map(self.start_south, column_ends))

        return max(max_top, max_bottom, max_left, max_right)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    world_map = open(file_name).read().strip().splitlines()
    mirror_map = MirrorMap(world_map)
    print(f"A total of {mirror_map.count_energized()} tiles have been energized.")
    print(f"The maximum of tiles that can be energized is {mirror_map.check_all()}.")
