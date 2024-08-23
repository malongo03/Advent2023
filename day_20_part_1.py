"""
Module to solve the first star of Day 20 of the Advent of Code 2023, which is
the 39th star overall.
"""
from copy import deepcopy
import sys

def parse_inputs(filename):
    with open(filename, encoding = "utf-8") as f:
        text = f.read().strip().split("\n")
    create_modules = [(line.split()[0][0], line.split()[0][1:])
                      for line in text
                      if line.split()[0][0] != "b"]
    inputs_and_outputs = [(line.split()[0], line.split()[2:])
                          for line in text]
    inputs_and_outputs = [(source.lstrip("&%"), [j.rstrip(",") for j in outputs])
                          for source, outputs in inputs_and_outputs]
    return create_modules, inputs_and_outputs


def elf_computer(filename):
    create_modules, inputs_and_outputs = parse_inputs(filename)

    class Module:
        def __init__(self, module_name):
            self.inputs = {}
            self.outputs = []
            self.signal = False
            self.name = module_name

        def __eq__(self, other):
            equality = self.name == other.name and \
                       self.signal == other.signal
            return equality

        def update_input (self, input_module, new_signal):
            self.inputs[input_module] = new_signal
            if self.update_signal(new_signal):
                return self.__broadcast()
            return [], 0, 0

        def update_signal(self, new_signal):
            return False

        def add_input(self, input_module):
            self.inputs[input_module] = False

        def add_output(self, output):
            self.outputs.append(output)

        def __broadcast(self):
            to_queue = []
            highs = 0
            lows = 0
            for output_module in self.outputs:
                to_queue.append((self.name, self.signal, output_module))
                # print(f"{self.name} --{self.signal}-> {output_module}")
                if self.signal:
                    highs += 1
                else:
                    lows += 1
            to_queue.reverse()
            return to_queue, lows, highs


    class FlipFlop(Module):
        def update_signal(self, new_signal):
            if not new_signal:
                self.signal = not self.signal
                return True
            return False


    class Conjunction(Module):
        def update_signal(self, new_signal):
            new_signal = not all(self.inputs.values())
            self.signal = new_signal
            return True


    class Broadcaster(Module):
        def __init__(self, module_name):
            super().__init__(module_name)
            self.add_input("button")

        def update_signal(self, new_signal):
            self.signal = new_signal
            return True


    modules = {"broadcaster": Broadcaster("broadcaster")}
    for mod_type, name in create_modules:
        if mod_type == "%":
            modules[name] = FlipFlop(name)
        else:
            modules[name] = Conjunction(name)

    for source_mod, outputs in inputs_and_outputs:
        for output_mod in outputs:
            modules[source_mod].add_output(output_mod)
            modules[output_mod] = modules.get(output_mod, Module(output_mod))
            modules[output_mod].add_input(source_mod)

    system_copy = []
    high_low_pulses = []

    for __ in range(1000):
        queue = [("button", False, "broadcaster")]
        low_pulses = 1
        high_pulses = 0
        # print("button --False-> broadcaster")
        while queue:
            source, signal, destination = queue.pop()
            add_to_queue, \
            new_low, \
            new_high = modules[destination].update_input(source, signal)
            queue = add_to_queue + queue
            low_pulses += new_low
            high_pulses += new_high
        # print("System is static")
        if modules in system_copy:
            break
        system_copy.append(deepcopy(modules))
        high_low_pulses.append((low_pulses, high_pulses))

    total_high = [high for _, high in high_low_pulses]
    total_low = [low for low, _ in high_low_pulses]
    return sum(total_high) * sum(total_low)


if __name__ == "__main__":
    print(elf_computer(sys.argv[1]))
