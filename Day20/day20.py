import sys
from collections import deque


class ModuleEnsemble:
    def __init__(self, module_data: list[str]) -> None:
        self.low_pulses = 0
        self.high_pulses = 0
        self.button_presses = 0
        self.modules = {"button": Module("button", "button -> ")}
        for module in module_data:
            module_name = (
                module.split("->")[0].strip().removeprefix("&").removeprefix("%")
            )
            if module_name in self.modules:
                self.modules[module_name].set_module(module)
            else:
                self.modules[module_name] = Module(module_name, module)
            for out_module in self.modules[module_name].outputs:
                if out_module not in self.modules:
                    self.modules[out_module] = Module(module_name)
                self.modules[out_module].add_input(module_name)

    def button_press(self):
        self.button_presses += 1
        queue = deque([(False, "button", ["broadcaster"])])
        while queue:
            next_signal_type, current_module, next_modules = queue.popleft()
            if next_signal_type:
                self.high_pulses += len(next_modules)
            else:
                self.low_pulses += len(next_modules)
            current_queue = deque()
            for module in next_modules:
                next_pulses = self.modules[module].in_pulse(
                    current_module, next_signal_type
                )
                if next_pulses is not None:
                    current_queue.appendleft(next_pulses)
            if current_queue:
                queue.extendleft(current_queue)

    def loop_press(self, number_presses: int) -> int:
        for _ in range(number_presses):
            self.button_press()
        return self.high_pulses * self.low_pulses

    def monitor_until_machine_on(self, monitor_module: str) -> int:
        while not self.button_press(monitor_module):
            pass
        return self.button_presses

    def __repr__(self) -> str:
        return str([module for module in self.modules.values()])


class Module:
    def __init__(self, module_name: str, module_data: str | None = None) -> None:
        self.inputs = []
        self.type = None
        self.name = module_name
        if module_data is None:
            return
        self.set_module(module_data)

    def set_module(self, module_data: str):
        module_data, outputs = module_data.split("->")
        module_data = module_data.strip()
        if module_data[0] == "&":
            self.type = "&"
            self.name = module_data[1:]
            self.state = None
        elif module_data[0] == "%":
            self.type = "%"
            self.name = module_data[1:]
            self.on = False
        elif module_data == "broadcaster":
            self.type = module_data
            self.name = module_data
        elif module_data == "button":
            self.type = module_data
            self.name = module_data
            self.outputs = ["broadcaster"]
        else:
            self.type = None
        if self.type != "button":
            self.outputs = [name.strip() for name in outputs.split(sep=",")]

    def add_input(self, module: str):
        if module not in self.inputs:
            self.inputs.append(module)

    def in_pulse(
        self, in_module: str, high: bool = False
    ) -> None | tuple[bool, str, list[str]]:
        if self.type is None:
            return None

        if self.type == "%":
            if high:
                return None
            self.on = not self.on
            return (self.on, self.name, self.outputs)

        if self.type == "&":
            if self.state is None:
                self.state = [False for _ in self.inputs]
            in_index = self.inputs.index(in_module)
            self.state[in_index] = high
            if all(self.state):
                return (False, self.name, self.outputs)
            return (True, self.name, self.outputs)

        if self.type == "broadcaster":
            return (high, self.name, self.outputs)

        if self.type == "button":
            return (False, self.name, self.outputs)

    def __repr__(self) -> str:
        if self.type == "&":
            to_return = "Conjunction"
        elif self.type == "%":
            to_return = "Flip-flop"
        elif self.type == "broadcaster":
            to_return = "Broadcaster"
        elif self.type == "button":
            to_return = "Button"
        elif self.type is None:
            return f"Untyped module '{self.name}' with inputs {self.inputs}"
        else:
            raise ValueError
        to_return += f" module '{self.name}' with inputs {self.inputs} and outputs {self.outputs}"
        return to_return


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    module_list = open(file_name).read().strip().splitlines()
    module_ensemble = ModuleEnsemble(module_list)
    pulses_product = module_ensemble.loop_press(1000)
    print(
        f"The product of high and low pulses sent after 1000 iterations is {pulses_product}"
    )
