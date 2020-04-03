import welcome
import spidev as SPI
import ST7789
from ramencore.cpu import CPU
import sys
import time

import RPi.GPIO as GPIO

# inputs = {
#     21: "key_1",
#     20: "key_2",
#     16: "key_3",
#     6: "stick_up",
#     19: "stick_down",
#     26: "stick_right",
#     5: "stick_left",
#     13: "stick_press"
# }

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
cpu = CPU(display)


def button_down(button):
    cpu.mem.io_byte ^= inputs[button]


for i in list(inputs.keys()):
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(i, GPIO.RISING, callback=button_down)


# welcome.welcome_msg(display)


# load firmware & program right before program code (0x4000) and jmp to it
firmware = open("./firmware/firmware.bin", "rb").read()
firmware_location = 0x4000 - len(firmware)
for i, byte in enumerate(firmware):
    cpu.mem.write(i + firmware_location, byte)
program = open(sys.argv[1], "rb").read()
for i, byte in enumerate(program):
    cpu.mem.write(i + 0x4000, byte)
cpu.pc = firmware_location

debug = False
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
