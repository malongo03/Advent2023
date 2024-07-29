from math import lcm

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
            return []

        def update_signal(self, signal):
            return False

        def add_input(self, input_module):
            self.inputs[input_module] = False

        def add_output(self, output):
            self.outputs.append(output)

        def __broadcast(self):
            to_queue = []
            for output_module in self.outputs:
                to_queue.append((self.name, self.signal, output_module))
                # print(f"{self.name} --{self.signal}-> {output_module}")
            to_queue.reverse()
            return to_queue


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
    modules["rx"] = Module("rx")
    for mod_type, name in create_modules:
        if mod_type == "%":
            modules[name] = Flip_flop(name)
        else:
            modules[name] = Conjunction(name)

    for source_mod, outputs in inputs_and_outputs:
        for output_mod in outputs:
            modules[source_mod].add_output(output_mod)
            modules[output_mod].add_input(source_mod)
    rx_handler = {rx_source: -1 for conjunctor in modules["rx"].inputs
                  for rx_source in modules[conjunctor].inputs}

    button_presses = 0
    while True:
        button_presses += 1
        queue = [("button", False, "broadcaster")]
        # print("button --False-> broadcaster")
        while queue:
            source, signal, destination = queue.pop()
            add_to_queue = modules[destination].update_input(source, signal)
            if destination in rx_handler and modules[destination].signal and \
            rx_handler[destination] == -1:
                rx_handler[destination] = button_presses
            queue = add_to_queue + queue
        # print("System is static")
        if -1 not in rx_handler.values():
            answer = 1
            for loop_len in rx_handler.values():
                answer = lcm(answer, loop_len)
            return answer


if __name__ == "__main__":
    print(elf_computer("day_20.txt"))