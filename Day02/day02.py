import sys
from functools import reduce
from operator import mul


def get_game_id_and_moves(game: str) -> (int, list[str]):
    game = game.split(sep=":")
    game_id = int(game[0].split(sep=" ")[1].removesuffix(":"))
    moves = game[1].split(";")
    return game_id, moves


def return_id_if_possible(game: str, max_nums: dict) -> int:
    game_id, moves = get_game_id_and_moves(game)
    plays_possible = map(lambda x: is_play_possible(x, max_nums), moves)
    return game_id if all(plays_possible) else 0


def is_play_possible(play, max_nums: dict) -> bool:
    play = play.split(sep=",")
    for color in play:
        color = color.strip().split(sep=" ")
        if int(color[0]) > max_nums[color[1]]:
            return False
    return True


def cubes_power(game: str) -> int:
    _, moves = get_game_id_and_moves(game)
    max_values = {"red": 0, "green": 0, "blue": 0}
    for play in moves:
        play = play.split(sep=",")
        for color in play:
            color = color.strip().split(sep=" ")
            max_values[color[1]] = max(max_values[color[1]], int(color[0]))
    return reduce(mul, max_values.values())


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    max_nums = {"red": 12, "green": 13, "blue": 14}
    possible_games = sum(map(lambda x: return_id_if_possible(x, max_nums), text))
    print(f"The sum of ids of possible games is {possible_games}")
    cube_values = sum(map(cubes_power, text))
    print(f"The sum of the cube values is {cube_values}")
