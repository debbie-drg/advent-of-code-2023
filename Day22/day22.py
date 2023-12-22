import sys
from typing import Self
from bisect import insort
from copy import copy


def parse_bricks(brick_list: list[str]) -> list[tuple[tuple[int, int, int]]]:
    parsed_bricks = []
    for brick in brick_list:
        current_brick = brick.split("~")
        current_brick = [
            tuple(int(element) for element in coordinates.split(","))
            for coordinates in current_brick
        ]
        parsed_bricks.append(current_brick)
    parsed_bricks.sort(key=lambda x: x[0][2])
    return [tuple(brick) for brick in parsed_bricks]


def interval_intersect(interval_1: tuple[int, int], interval_2: tuple[int, int]):
    return not (interval_1[1] < interval_2[0] or interval_2[1] < interval_1[0])


class Brick:
    def __init__(self, location: tuple[tuple[int, int, int]]) -> None:
        self.location = location
        self.set_height()
        self.parents = []
        self.children = []

    def set_height(self):
        self.lower_height = self.location[0][2]
        self.upper_height = self.location[1][2]

    def lower(self, new_bottom_height: int):
        altitude = self.location[1][2] - self.location[0][2]
        self.location = tuple(
            [
                (self.location[0][0], self.location[0][1], new_bottom_height),
                (
                    self.location[1][0],
                    self.location[1][1],
                    new_bottom_height + altitude,
                ),
            ]
        )
        self.set_height()

    def overlaps(self, other: Self):
        x_interval_1 = (self.location[0][0], self.location[1][0])
        y_interval_1 = (self.location[0][1], self.location[1][1])
        x_interval_2 = (other.location[0][0], other.location[1][0])
        y_interval_2 = (other.location[0][1], other.location[1][1])
        return interval_intersect(x_interval_1, x_interval_2) and interval_intersect(
            y_interval_1, y_interval_2
        )

    def can_remove(self) -> bool:
        for parent in self.parents:
            if len(parent.children) == 1:
                self.can_be_removed = False
                return False
        self.can_be_removed = True
        return True

    def fall_if_removed(self) -> int:
        if self.can_be_removed:
            return 0
        return self.chain_fall(set([self]))

    def chain_fall(self, falling: set[Self]):
        count = 0
        to_fall = set()

        for parent in self.parents:
            if parent in falling:
                continue
            is_supported = False
            for child in parent.children:
                if child not in falling:
                    is_supported = True
                    break
            if not is_supported:
                count += 1
                falling.add(parent)
                to_fall.add(parent)

        for brick in to_fall:
            count += brick.chain_fall(falling)

        return count

    def __repr__(self) -> str:
        return f"Brick at {self.location}"

    def __hash__(self) -> int:
        return self.location.__hash__()


class BrickWall:
    def __init__(self, bricks: list[str]) -> None:
        self.bricks = set()
        self.unprocessed_bricks = parse_bricks(bricks)
        self.populated_heights_top = []
        self.populated_heights_bottom = []
        self.place_bricks()
        self.fill_connections()

    def get_bricks_top(self, top_height: int):
        return [brick for brick in self.bricks if brick.upper_height == top_height]

    def get_bricks_bottom(self, bottom_height: int):
        return [brick for brick in self.bricks if brick.lower_height == bottom_height]

    def place_brick(self, brick: Brick):
        bottom_height = brick.lower_height
        top_height = brick.upper_height
        self.bricks.add(brick)
        if bottom_height not in self.populated_heights_bottom:
            insort(self.populated_heights_bottom, bottom_height)
        if top_height not in self.populated_heights_top:
            insort(self.populated_heights_top, top_height)

    def place_bricks(self):
        for brick in self.unprocessed_bricks:
            brick = Brick(brick)
            if brick.lower_height == 1:
                self.place_brick(brick)
                continue
            lower_heights = [
                height
                for height in self.populated_heights_top
                if height < brick.lower_height
            ]
            placed = False
            for height in reversed(lower_heights):
                for placed_brick in self.get_bricks_top(height):
                    if brick.overlaps(placed_brick):
                        brick.lower(placed_brick.upper_height + 1)
                        self.place_brick(brick)
                        placed = True
                        break
                if placed:
                    break
            if not placed:
                brick.lower(1)
                self.place_brick(brick)

    def fill_connections(self):
        for height in self.populated_heights_top:
            if not height + 1 in self.populated_heights_bottom:
                continue
            possible_children = self.get_bricks_top(height)
            possible_parents = self.get_bricks_bottom(height + 1)
            for children in possible_children:
                for parent in possible_parents:
                    if children.overlaps(parent):
                        children.parents.append(parent)
                        parent.children.append(children)

    def vaporizable(self):
        return sum(brick.can_remove() for brick in self.bricks)

    def count_would_fall(self):
        return sum(brick.fall_if_removed() for brick in self.bricks)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    bricks = open(file_name).read().strip().splitlines()
    brick_wall = BrickWall(bricks)
    print(f"The number of vaporizable bricks is {brick_wall.vaporizable()}")
    print(f"The sum of all falling blocks is {brick_wall.count_would_fall()}")
