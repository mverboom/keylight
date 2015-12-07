#!/usr/bin/python
#
# Control keyboard backlight (developed for Thinkpad t440s)

import os
from evdev import *
from select import select
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--hotkeys", action="store", type="string", dest="hotkeys", default="88,125", help="Comma seperated list of keycodes that combined form the hotkey to turn backlight on or off (default is winkey + f12).")
parser.add_option("--offset", action="store", type="int", dest="offset", default=13, help="Byte offset in ACPI Embedded Controller to change (default=13).")
parser.add_option("--ledon", action="store", type="int", dest="ledon", default=0x45, help="Value to set in ACPI Embedded Controller to set led backlight on (default is 0x45).")
parser.add_option("--ledoff", action="store", type="int", dest="ledoff", default=0x05, help="Value to set in ACPI Embedded Controller to set led backlight off (default is 0x05).")
parser.add_option("-t", action="store", type="int", dest="timeout", default=5, help="Timeout in seconds after which backlight is turned off (default is 5).")
parser.add_option("-d", action="store", type="string", dest="device", default="/dev/input/event3", help="Which input device to use as keyboard (default is /dev/input/event3).")
parser.add_option("-l", action="store_true", dest="list", default=False, help="List all input devices.")
parser.add_option("--keys", action="store_true", dest="keys", default=False, help="Dump all keycodes to find a keycombination to activate backlight.")

(options, args) = parser.parse_args()

if options.list:
    print "Available input devices:"
    devices = [InputDevice(fn) for fn in list_devices()]
    for dev in devices:
        print(dev.fn, dev.name, dev.phys)
    exit(0)

hotkeys = map(int, options.hotkeys.split(","))

if not os.path.exists(options.device):
    print("Device does not exist.")
    exit(1)
if not os.path.exists("/sys/kernel/debug/ec/ec0/io"):
    print("/sys/kernel/debug/ec/ec0/io does not exist, is module ec_sys inserted?")
    exit(1)

dev = InputDevice(options.device)
light = os.open("/sys/kernel/debug/ec/ec0/io", os.O_RDWR)

if options.keys:
    print "Showing pressed key codes. Press ctrl-c to abort"
    lastkey=0
    for event in dev.read_loop():
        key=dev.active_keys()
        if key != lastkey:
            print key
            lastkey=key

def backlight(state):
    os.lseek(light,options.offset,os.SEEK_SET)
    os.write(light,chr(state))

active = False
state = False
newstate = False
timeout = 0
while 1:
    r,w,x = select([dev.fd], [], [], 1.0)
    if r: 
        for event in dev.read():
            pass
        if  dev.active_keys() == hotkeys:
            active = not active
        else:
           timeout = 0
    else:
        if active:
            timeout=timeout+1
    if timeout > options.timeout:
        newstate = False
    else:
        newstate = True
    if (not active):
        newstate = False

    if newstate != state:
        if newstate:
            backlight(options.ledon)
        else:
            backlight(options.ledoff)
        state=newstate
