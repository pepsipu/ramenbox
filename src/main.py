import welcome
import spidev as SPI
import ST7789
from ramencore.cpu import CPU

import time

import RPi.GPIO as GPIO

inputs = {
    21: "key_1",
    20: "key_2",
    16: "key_3",
    6: "stick_up",
    19: "stick_down",
    26: "stick_right",
    5: "stick_left",
    13: "stick_press"
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def button_down(button):
    pass


for i in list(inputs.keys()):
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(i, GPIO.RISING, callback=button_down)

cpu = CPU()
display = ST7789.ST7789(SPI.SpiDev(0, 0))
welcome.welcome_msg(display)

program = "\xa9\x80\x85\x01\x65\x01\x0a"
for i, byte in enumerate(program):
    cpu.mem.write(i, ord(byte))
while True:
    cpu.step()
