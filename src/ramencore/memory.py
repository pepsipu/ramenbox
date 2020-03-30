class Memory:
    pages = [{
        "banks": [[0] * 0x100] * 0x80,
        "active_bank": 0
    }] * 0x100

    def read(self, address, sign=False):
        page = self.pages[(address & 0xff00) >> 8]
        res = page["banks"][page["active_bank"]][address & 0xff]
        if sign and res > 127:
            return -((res ^ 0xff) + 1)
        return res

    def write(self, address, data):
        page = self.pages[(address & 0xff00) >> 8]
        page["banks"][page["active_bank"]][address & 0xff] = data

    def get_display(self):
        pass
