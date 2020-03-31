from PIL import Image, ImageDraw, ImageFont

screen = Image.new("RGB", (240, 240))


class Memory:
    display_page = 0
    pages = [{
        "banks": [[0] * 0x100] * 0xff,
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

    def display(self, display):
        screen_page = self.pages[self.display_page]
        pixels_plotted = 0
        for i in range(0xe1):
            bank = screen_page["banks"][i]
            for byte in bank:
                screen.putpixel((pixels_plotted % 240, pixels_plotted // 240), 0xff)
                pixels_plotted += 1
        display.ShowImage(screen, 0, 0)
