import welcome
import spidev as SPI
import ST7789
from ramencore.cpu import CPU
import sys
import time
from PIL import Image
import math
import RPi.GPIO as GPIO

inputs_name = {
    21: "key_1",
    20: "key_2",
    16: "key_3",
    6: "stick_up",
    19: "stick_down",
    26: "stick_right",
    5: "stick_left",
    13: "stick_press"
}

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

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

display = ST7789.ST7789(SPI.SpiDev(0, 0))
display.init()
display.clear()
debug = True
cpu = CPU(display, debug=debug)

for i in list(inputs.keys()):
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

welcome.welcome_msg(display)


# load firmware & program right before program code (0x4000) and jmp to it
firmware = open("./firmware/firmware.bin", "rb").read()

# backgrounds can be large
# added option so that way you can load in the background before runtime
if len(sys.argv) > 2:
    background = Image.open(sys.argv[2])
    img = display.ShowImage(background)
    page = cpu.mem.pages[cpu.mem.display_page]
    pixels = 0
    for i in range(240 * 240):
        page["banks"][(i & 0xff00) >> 8][i & 0xff] = (img[pixels] + (img[pixels + 1] >> 8))
        pixels += 2

firmware_location = 0x4000 - len(firmware)
for i, byte in enumerate(firmware):
    cpu.mem.write(i + firmware_location, byte)
program = open(sys.argv[1], "rb").read()
for i, byte in enumerate(program):
    cpu.mem.write(i + 0x4000, byte)
cpu.pc = firmware_location

while True:
    if debug:
        cmd = input("> ")
        args = cmd.split(" ")
        cmd = args[0]
        if cmd == "n":
            if len(args) > 1:
                for i in range(int(args[1])):
                    cpu.step()
            else:
                cpu.step()
        elif cmd == "x":
            print(cpu.mem.read(int(args[1], 16)))
    else:
        cpu.step()
