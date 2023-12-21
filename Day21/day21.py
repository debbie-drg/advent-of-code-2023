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

    def possible_next_moves(self, location: tuple[int, int], in_bounds: bool = False):
        if not in_bounds:
            return [point for point in neighbours(location) if not self.is_rock(point)]
        return [
            point
            for point in neighbours(location)
            if self.in_bounds(point) and not self.is_rock(point)
        ]

    def visitable(
        self,
        num_steps: int,
        until_all: bool = False,
        start: tuple[int, int] | None = None,
        within_grid: bool = False,
    ) -> set | tuple[int, int, int]:
        history = [set(), set()]
        steps_done = 0
        if until_all:
            num_steps = self.width * self.depth
            within_grid = True
        start_position = self.start if start is None else start
        current_positions = set([start_position])
        history[num_steps % 2].add(start_position)
        while True:
            next_positions = set()
            num_steps -= 1
            parity = num_steps % 2
            for position in current_positions:
                next_positions.update(
                    candidate
                    for candidate in self.possible_next_moves(position, within_grid)
                    if candidate not in history[parity]
                )
            if until_all and len(next_positions) == 0:
                break
            steps_done += 1
            current_positions = next_positions
            history[parity].update(next_positions)
            if not until_all and num_steps == 0:
                break
        if not until_all:
            return history[0]
        return (steps_done, len(history[0]), len(history[1]))

    def num_steps_to_fill_side(self) -> tuple[int]:
        return self.visitable(0, True, (self.start[0], 0))

    def num_visitable(self, num_steps: int) -> int:
        return len(self.visitable(num_steps))

    def num_visitable_infinity(self, num_steps: int):
        grid_size = self.width
        half_size = grid_size // 2
        f0 = self.num_visitable(half_size)
        f1 = self.num_visitable(half_size + grid_size)
        f2 = self.num_visitable(half_size + 2 * grid_size)

        # Since there are no obstacles on the diagonal nor mid-lines, the rate of visits increases in a
        # grid form. This is quadratic growth and we can interpolate the polinomial with 3 values.
        # Luckily, requested step size allows for this, as it is perfectly divisible by the grid size
        # once we walk the half grid size from the first square.

        remaining = (num_steps - half_size) // grid_size
        a0 = f0
        a1 = f1 - f0
        a2 = f2 - f1
        return a0 + a1 * remaining + (remaining * (remaining - 1) // 2) * (a2 - a1)


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
        num_steps_large = 26501365
        print(
            f"The number of spots that can be visited after walking {num_steps} steps is {garden.num_visitable(num_steps)}"
        )
        print(f"The number of spots that can be visited after walking {num_steps_large} steps is {garden.num_visitable_infinity(num_steps_large)}")
