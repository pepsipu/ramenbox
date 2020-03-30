class Addressing:
    def __init__(self, cpu):
        self.cpu = cpu

    def accumulator(self):
        return self.cpu.ac

    def immediate(self):
        self.cpu.pc += 1
        return self.cpu.pc

    def relative(self):
        pass
