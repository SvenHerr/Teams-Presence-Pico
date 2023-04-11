##!/usr/bin/env python
# Python script to show Teams presence status on led
# Author: Sven Herrmann
# Date 08.04.2023

try:
    import sys
    import machine
    import neopixel
    import time
    
except Exception as err:
    print(err)

# configure the UART peripheral for the Raspberry Pi Pico
uart = machine.UART(0, baudrate=9600)

# define a function to send a string over the UART
def send_string(string):
    uart.write(string)

led = machine.Pin(25, machine.Pin.OUT)
led(1)

LedRed = 1
LedGreen = 3
LedYellow = 2
LedBlue = 0

# This is for LED Strips
pin_np = 28
leds = 22
brightness = 10
global np
np = neopixel.NeoPixel(machine.Pin(pin_np, machine.Pin.OUT), leds)


led_red = machine.Pin(LedRed, machine.Pin.OUT)
led_green = machine.Pin(LedGreen, machine.Pin.OUT)
led_yellow = machine.Pin(LedYellow, machine.Pin.OUT)
led_blue = machine.Pin(LedBlue, machine.Pin.OUT)

def setLEDStripeTo(red,  green, blue):
    for i in range (leds):
        np[i] = (red, green, blue)
    np.write()

def leds_off():
    led_red.value(0)
    led_green.value(0)
    led_yellow.value(0)
    led_blue.value(0)
    # This is for LED Strips
    setLEDStripeTo(0,0,0)

def setRedLedOn():
    leds_off()
    led_red.value(1)
    # This is for LED Strips
    setLEDStripeTo(255,0,0)

def setGreenLedOn():
    leds_off()
    led_green.value(1)
    # This is for LED Strips
    setLEDStripeTo(0,255,0)

def setYellowLedOn():
    leds_off()
    led_yellow.value(1)
    # This is for LED Strips
    setLEDStripeTo(255,255,0)

def setBlueLedOn():
    leds_off()
    led_blue.value(1)

while True:
    #send_string('ok\n')
    v = sys.stdin.readline().strip()

    if v =='Available' :
        setGreenLedOn()
    elif v =='BeRightBack' :
        setYellowLedOn()
    elif v =='Busy' :
        setRedLedOn()
    elif v =='DoNotDisturb' :
        setRedLedOn()
    elif v =='Away' :
        setYellowLedOn()
    elif v =='Offline' :
        setBlueLedOn()

# match doesnt work with my version
    # match v:
    #     case 'Available' :
    #         setGreenLedOn()
    #     case 'BeRightBack' :
    #         setYellowLedOn()
    #     case 'Busy' :
    #         setRedLedOn()
    #     case 'DoNotDisturb' :
    #         setRedLedOn()
    #     case 'Away' :
    #         setYellowLedOn()
    #     case 'Offline' :
    #         setBlueLedOn()
    #     case _:
    #         print()