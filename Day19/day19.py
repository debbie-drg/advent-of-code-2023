import sys
from copy import deepcopy


def parse_workflow(workflow: str) -> list:
    workflow = workflow.removesuffix("}")
    workflow = workflow.split(",")
    parsed_workflow = []
    for element in workflow:
        current_instruction = element.split(":")
        parsed_workflow.append(current_instruction)
    return parsed_workflow


def workflows_dict(workflows: list[str]) -> dict[str, list]:
    workflows_dict = dict()
    for workflow in workflows:
        name, workflow = workflow.split("{")
        workflow = parse_workflow(workflow)
        workflows_dict[name] = workflow
    return workflows_dict


def parse_part(part: str) -> dict[str, int]:
    part = part.removeprefix("{").removesuffix("}")
    part = part.split(",")
    part_dict = dict()
    for value in part:
        variable, value = value.split("=")
        part_dict[variable] = int(value)
    return part_dict


class Interval:
    def __init__(
        self,
        extremes: dict = {
            "x": [1, 4000],
            "m": [1, 4000],
            "a": [1, 4000],
            "s": [1, 4000],
        },
    ):
        self.extremes = extremes

    def combinations(self) -> int:
        result = 1
        for interval in self.extremes.values():
            result *= interval[1] - interval[0] + 1
        return result

    def value(self) -> int:
        return sum([value[0] for value in self.extremes.values()])


def eval_parts(workflows_dict: dict, parts: list[str] | None = None) -> int:
    if parts is None:
        queue = [[Interval(), "in"]]
        intervals = True
    else:
        queue = []
        for part in parts:
            part = parse_part(part)
            to_add_interval = deepcopy(Interval())
            for variable in part:
                to_add_interval.extremes[variable] = [part[variable], part[variable]]
            queue.append([to_add_interval, "in"])
        intervals = False
    processed_intervals = []
    while queue:
        current_interval, workflow = queue.pop()
        if workflow == "A":
            processed_intervals.append(current_interval)
            continue
        if workflow == "R":
            continue
        workflow = workflows_dict[workflow]
        for instruction in workflow:
            if len(instruction) == 2:
                variable = instruction[0][0]
                variable_range = current_interval.extremes[variable]
                cutoff = int(instruction[0][2:])
                symbol = instruction[0][1]
                if symbol == "<":
                    if variable_range[1] < cutoff:
                        queue.append([current_interval, instruction[1]])
                        break
                    if variable_range[0] < cutoff <= variable_range[1]:
                        new_interval = deepcopy(current_interval)
                        new_interval.extremes[variable] = [
                            variable_range[0],
                            cutoff - 1,
                        ]
                        queue.append([new_interval, instruction[1]])
                        current_interval.extremes[variable] = [
                            cutoff,
                            variable_range[1],
                        ]
                if symbol == ">":
                    if variable_range[0] > cutoff:
                        queue.append([current_interval, instruction[1]])
                        break
                    if variable_range[0] <= cutoff < variable_range[1]:
                        new_interval = deepcopy(current_interval)
                        new_interval.extremes[variable] = [
                            cutoff + 1,
                            variable_range[1],
                        ]
                        queue.append([new_interval, instruction[1]])
                        current_interval.extremes[variable] = [
                            variable_range[0],
                            cutoff,
                        ]
            else:
                queue.append([current_interval, instruction[0]])
    if intervals:
        return sum([interval.combinations() for interval in processed_intervals])
    return sum([interval.value() for interval in processed_intervals])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    workflows, parts = open(file_name).read().strip().split("\n\n")
    workflows = workflows.splitlines()
    parts = parts.splitlines()

    workflows = workflows_dict(workflows)
    print(f"The sum of the values of accepted parts is {eval_parts(workflows, parts)}")
    print(f"The number of accepted combinations is {eval_parts(workflows)}")
