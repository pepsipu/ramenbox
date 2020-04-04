screen = [0] * (240 * 240 * 2)


class Memory:
    display_page = 0xfd
    pages = []
    io_byte = 0

    def __init__(self):
        for _ in range(0xff):
            self.pages.append({
                "banks": [[0] * 0x100 for _ in range(0xff)],
                "active_bank": 0
            })

    def read(self, address, sign=False):
        if address == 0xee00:
            return self.io_byte & 0xff
        page = self.pages[(address & 0xff00) >> 8]
        res = page["banks"][page["active_bank"]][address & 0xff]
        if sign and res > 127:
            return -((res ^ 0xff) - 1)
        return res

    def write(self, address, data):
        page = self.pages[(address & 0xff00) >> 8]
        page["banks"][page["active_bank"]][address & 0xff] = data

    def display(self, display):
        screen_page = self.pages[self.display_page]
        pixels_plotted = 0
        for i in range(0xe1):
            bank = screen_page["banks"][i]
            for byte in bank:
                word = byte * 257
                screen[pixels_plotted] = word & 0xff
                screen[pixels_plotted + 1] = (word & 0xff00) >> 8
                pixels_plotted += 2
        display.write_array(screen)
