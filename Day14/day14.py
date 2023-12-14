import sys
import re
import time


class RockMap:
    def __init__(self, rock_map: list[str]):
        self.width = len(rock_map[0])
        self.depth = len(rock_map)
        self.rocks = set()
        self.obstacles = set()
        for index, line in enumerate(rock_map):
            self.obstacles.update(
                [(index, item.start()) for item in re.finditer("#", line)]
            )
            self.rocks.update(
                [(index, item.start()) for item in re.finditer("O", line)]
            )

    def slide_north(self):
        moved_rocks = []
        pegged_to = dict()
        queue = sorted(list(self.rocks))
        pegged_to = {rock: 0 for rock in self.rocks}
        while queue:
            rock = queue.pop()
            moving_number = pegged_to[rock] + 1
            while True:
                if rock[0] == 0:
                    for index in range(moving_number):
                        moved_rocks.append((rock[0] + index, rock[1]))
                    break
                next_position = (rock[0] - 1, rock[1])
                if next_position in self.rocks:
                    pegged_to[next_position] = moving_number
                    break
                if next_position in self.obstacles:
                    for index in range(moving_number):
                        moved_rocks.append((rock[0] + index, rock[1]))
                    break
                rock = next_position
        self.rocks = moved_rocks

    def total_load(self) -> int:
        return sum([self.depth - rock[0] for rock in self.rocks])

    def rotate(self):
        self.rocks = set((rock[1], self.depth - 1 - rock[0]) for rock in self.rocks)
        self.obstacles = set(
            [(obstacle[1], self.depth - 1 - obstacle[0]) for obstacle in self.obstacles]
        )
        self.width, self.depth = self.depth, self.width

    def spin_cycle(self):
        for _ in range(4):
            self.slide_north()
            self.rotate()

    def laod_after_cycles(self, num_cycles: int) -> int:
        backup_rocks = [set(self.rocks)]
        while True:
            num_cycles -= 1
            if num_cycles == 0:
                return self.total_load()
            self.spin_cycle()
            try:
                index_cycle = backup_rocks.index(set(self.rocks))
                cycle_length = len(backup_rocks) - index_cycle
                num_cycles %= cycle_length
                self.rocks = list(backup_rocks[index_cycle + num_cycles])
                return self.total_load()
            except ValueError:
                pass
            backup_rocks.append(set(self.rocks))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    rocks = open(file_name).read().strip().split(sep="\n")
    rock_map = RockMap(rocks)
    rock_map.slide_north()
    print(f"The total load is {rock_map.total_load()}")

    num_cycles = 1000000000
    rock_map = RockMap(rocks)
    print(
        f"The total load after {num_cycles} cycles is {rock_map.laod_after_cycles(num_cycles)}"
    )
