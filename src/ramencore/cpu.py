import json
import ramencore.memory as memory
import ramencore.instructions as instructions
import RPi.GPIO as GPIO

inputs = {
    21: 128,
    20: 64,
    16: 32,
    6: 16,
    19: 8,
    26: 4,
    5: 2,
    13: 1
}


class CPU:
    pc = 0
    ac = 0
    x = 0
    y = 0
    sr = 0
    sp = 0
    mem = memory.Memory()
    ops = {}
    custom_ops = {}

    def __init__(self, display):
        self.current_addr_mode = ""
        self.display = display
        op_list = json.load(open("./ramencore/opcodes.json", "r"))
        for op in op_list:
            self.ops[op["byte"]] = {
                "func": getattr(instructions, "_{}".format(op["name"].lower())),
                "addressing": op["addressing"],
                "bytes": op["byte_length"],
                "name": op["name"]
            }
        self.ops[0] = {
            "func": lambda x, y: exit(1),
            "addressing": "im",
            "bytes": 1,
            "name": "quit yes"
        }
        custom_op_list = json.load(open("./ramencore/custom_opcodes.json", "r"))
        for op in custom_op_list:
            self.custom_ops[op["byte"]] = {
                "func": getattr(instructions, "_{}".format(op["name"].lower())),
                "addressing": op["addressing"],
                "bytes": op["byte_length"],
                "name": op["name"]
            }

    def step(self):
        for i in list(inputs.keys()):
            if not GPIO.input(i):
                self.mem.io_byte |= inputs[i]
            else:
                self.mem.io_byte &= (~(inputs[i])) & 0xff
        byte = self.mem.read(self.pc)
        # ramenbox custom instructions are prefixed with 0xff
        if byte == 0xff:
            self.pc += 1
            instruction = self.custom_ops[self.mem.read(self.pc)]
        else:
            instruction = self.ops[byte]
        dump = ""
        for i in range(instruction["bytes"]):
            dump += hex(self.mem.read(self.pc + i)) + " "
        data = 0
        self.current_addr_mode = instruction["addressing"]
        if instruction["addressing"] == "ac":
            data = "ac"
        elif instruction["addressing"] == "i":
            data = self.mem.read(self.pc + 1)
        elif instruction["addressing"] == "r":
            data = self.mem.read(self.pc + 1, sign=True) + self.pc + 2
        elif instruction["addressing"] == "in":
            data = self.mem.read(self.mem.read(self.pc + 1) + (self.mem.read(self.pc + 2) << 8))
        elif instruction["addressing"] == "z":
            data = self.mem.read(self.mem.read(self.pc + 1))
        elif instruction["addressing"] == "zx":
            data = self.mem.read(self.mem.read(self.pc + 1) + self.x) & 0xff
        elif instruction["addressing"] == "zy":
            data = self.mem.read(self.mem.read(self.pc + 1) + self.y) & 0xff
        elif instruction["addressing"] == "a":
            data = self.mem.read(self.pc + 1) + (self.mem.read(self.pc + 2) << 8)
        elif instruction["addressing"] == "ax":
            data = self.mem.read(self.pc + 1) + (self.mem.read(self.pc + 2) << 8) + self.x
        elif instruction["addressing"] == "ay":
            data = self.mem.read(self.pc + 1) + (self.mem.read(self.pc + 2) << 8) + self.y
        elif instruction["addressing"] == "ix":
            page_zero_index = self.mem.read(self.pc + 1) + self.x
            data = self.mem.read(page_zero_index) + (self.mem.read(page_zero_index + 1) << 8)
        elif instruction["addressing"] == "iy":
            page_zero_index = self.mem.read(self.pc + 1)
            data = self.mem.read(page_zero_index) + (self.mem.read(page_zero_index + 1) << 8) + self.y
        print("{}: {} - {}".format(hex(self.pc), dump[:-1], instruction["name"]))
        self.pc += instruction["bytes"]
        print(self)
        instruction["func"](self, data)
        print(self)

    def __repr__(self):
        return "PC: {}, AC: {}, X: {}, Y: {}, SR: {}, SP: {}, IO_B: {}".format(hex(self.pc), hex(self.ac), hex(self.x), hex(self.y), hex(self.sr), hex(self.sp), hex(self.mem.io_byte))
