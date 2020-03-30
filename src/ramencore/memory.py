class Memory:
    mem = [0] * 0xffff

    def read(self, address, sign=False):
        res = self.mem[address]
        if sign and res > 127:
            return -((res ^ 0xff) + 1)
        return res

    def write(self, address, data):
        self.mem[address] = data
