import sys


def contiguous_differences(number_list: list) -> list:
    return [
        number_list[index + 1] - number_list[index]
        for index in range(len(number_list) - 1)
    ]


def next_number(history: str) -> (int, int):
    history = [[int(element) for element in history.split(sep=" ")]]
    while any([value != 0 for value in history[-1]]):
        history.append(contiguous_differences(history[-1]))
    forward_result = backward_result = 0
    for index in range(len(history) - 1, -1, -1):
        forward_result += history[index][-1]
        backward_result = history[index][0] - backward_result
    return forward_result, backward_result


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    number_histories = open(file_name).read().strip().split(sep="\n")
    next_and_previous = [next_number(x) for x in number_histories]
    next_prediction_sum = sum([prediction[0] for prediction in next_and_previous])
    previous_prediction_sum = sum([prediction[1] for prediction in next_and_previous])
    print(f"The sum of the next predictions is {next_prediction_sum}")
    print(f"The sum of the previous predictions is {previous_prediction_sum}")
