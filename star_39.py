from copy import deepcopy

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
        def __init__(self, name):
            self.inputs = {}
            self.outputs = []
            self.signal = False
            self.name = name

        def __eq__(self, other):
            equality = self.name == other.name and \
                       self.signal == other.signal
            return equality


        def update_input (self, input_module, signal):
            self.inputs[input_module] = signal
            if self.update_signal(signal):
                return self.__broadcast()
            return [], 0, 0

        def update_signal(self, signal):
            return False

        def add_input(self, input_module):
            self.inputs[input_module] = False

        def add_output(self, output):
            self.outputs.append(output)

        def __broadcast(self):
            to_queue = []
            high_pulses = 0
            low_pulses = 0
            for output_module in self.outputs:
                to_queue.append((self.name, self.signal, output_module))
                # print(f"{self.name} --{self.signal}-> {output_module}")
                if self.signal:
                    high_pulses += 1
                else:
                    low_pulses += 1
            to_queue.reverse()
            return to_queue, low_pulses, high_pulses


    class Flip_flop(Module):
        def update_signal(self, signal):
            if not signal:
                self.signal = not self.signal
                return True
            return False


    class Conjunction(Module):
        def update_signal(self, signal):
            new_signal = not all(self.inputs.values())
            self.signal = new_signal
            return True


    class Broadcaster(Module):
        def __init__(self, name):
            super().__init__(name)
            self.add_input("button")

        def update_signal(self, signal):
            self.signal = signal
            return True


    modules = {}
    modules["broadcaster"] = Broadcaster("broadcaster")
    for mod_type, name in create_modules:
        if mod_type == "%":
            modules[name] = Flip_flop(name)
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
    print(elf_computer("day_20.txt"))