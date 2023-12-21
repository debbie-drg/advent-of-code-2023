import sys

DIRECTIONS = {(1, 0), (-1, 0), (0, 1), (0, -1)}


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(location: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(location, direction) for direction in DIRECTIONS]


class Garden:
    def __init__(self, garden_map: list[str]) -> None:
        self.rocks = set()
        self.depth = len(garden_map)
        self.width = len(garden_map[0])
        for row_index, row in enumerate(garden_map):
            for col_index, char in enumerate(row):
                if char == "#":
                    self.rocks.add((row_index, col_index))
                elif char == "S":
                    self.start = (row_index, col_index)

    def in_bounds(self, location: tuple[int, int]) -> bool:
        return 0 <= location[0] < self.depth and 0 <= location[1] < self.width

    def is_rock(self, location: tuple[int, int]) -> bool:
        return (location[0] % self.depth, location[1] % self.width) in self.rocks

    def possible_next_moves(self, location: tuple[int, int]):
        return [
            point
            for point in neighbours(location)
            if not self.is_rock(point)
        ]

    def visitable(self, num_steps: int) -> set:
        history = [set(), set()]
        current_positions = set([self.start])
        history[num_steps % 2].add((self.start))
        while True:
            next_positions = set()
            num_steps -= 1
            parity = num_steps % 2
            for position in current_positions:
                next_positions.update(
                    candidate
                    for candidate in self.possible_next_moves(position)
                    if candidate not in history[parity]
                )
            current_positions = next_positions
            history[parity].update(current_positions)
            if num_steps == 0:
                break
        return history[0]

    def num_visitable(self, num_steps: int) -> int:
        return len(self.visitable(num_steps))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    garden_map = open(file_name).read().strip().splitlines()
    garden = Garden(garden_map)
    if file_name == "example.txt":
        to_print = [6, 10, 50, 100, 500, 1000, 5000]
        for steps_number in to_print:
            print(f"{steps_number} steps, {garden.num_visitable(steps_number)} tiles.")
    else:
        num_steps = 64
        print(
            f"The number of spots that can be visited after walking {num_steps} steps is {garden.num_visitable(num_steps)}"
        )
