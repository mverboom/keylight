# Keylight.py

Keylight is a hack to make the backlight of the keyboard turn on when you're typing, and
turn off again after you've stopped typing.

The script was inspired by a few postings I found on the Thinklight that is on several
Thinkpad laptops. My T440s has a backlit keyboard which I don't use often, because when
I stop typing it is just sitting there draining the battery.

If you're interested, be aware this script uses root rights and evdev to monitor the
keyboard. So it's not exactly the most secure solution..

I'm not sure if the script will work with any laptops other then Thinkpads, but who
knows.

Oh, this is one of my first python scripts, so don't expect anything fancy inside ;)

## Requirements

You will need python evdev to run this script. Also, you need to be root and do some
searching to start the script with the correct values for your laptop.

## Finding the bytes

The script is quite a hack, it basically changes the value in the ACPI embedded controller
that is related to the backlight. To start you need to figure out for your laptop which
byte it is and what the values are. To do this you need to insert the ec_sys kernel
module

`modpobe ec_sys`

Then the following file should be available with the contents of the embedded controller:

`/sys/kernel/debug/ec/ec0/io`

Now, try to start the following command to look for any changes in the content:

`watch xxd /sys/kernel/debug/ec/ec0/io`

You should end up with somthing like this:

`Every 2.0s: xxd /sys/kernel/debug/ec/ec0/io                         Mon Dec  7 19:58:34 2015

0000000: a605 a8c2 0086 0500 0009 4700 0005 8000  ..........G.....
0000010: 0000 ffff f03c 0001 7bff 0000 ffff 9d00  .....<..{.......
0000020: 0000 0000 0000 00d8 0000 0000 6900 6e80  ............i.n.
0000030: 0000 0000 7004 0000 84c3 3018 0050 0000  ....p.....0..P..
0000040: 0000 0000 0000 0446 4218 0000 0000 0000  .......FB.......
0000050: 0080 020c 0001 0203 0405 0607 ec62 2975  .............b)u
0000060: 11e1 ba4d 0700 0000 0000 0000 0000 0000  ...M............
0000070: 0000 0000 0800 0000 2800 0000 0000 0000  ........(.......
0000080: 0010 0506 0000 0300 0000 0000 0000 2b00  ..............+.
0000090: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000a0: 3404 a208 6f00 3100 0ffe 492c ffff c000  4...o.1...I,....
00000b0: 0000 0000 0000 0000 0000 2d05 0096 0100  ..........-.....
00000c0: 0000 0000 0000 0000 005a 0002 0000 1000  .........Z......
00000d0: 16c0 c001 0000 0000 0000 0000 0000 0000  ................
00000e0: 0000 0000 0000 0000 1090 df17 e42e 4403  ..............D.
00000f0: 474a 4854 3235 5757 1b67 7282 0000 0000  GJHT25WW.gr.....`

Now while watching this, turn the backlight on and off and see which byte is changing.
Once you found it, find the position of the byte that is changing. Next, note the byte
values that are related to off and on.

These values can be used to start the script with:

`keylight.py --offset=13 --ledon=0x45 --ledoff=0x05`

## Finding the keyboard

Now with the information on the backlight found, we need to find the keyboard device. Just
run

`keylight.py -l`

for a list of input devices. The output can look something like this:

`keylight.py -l
Available input devices:
('/dev/input/event13', 'TPPS/2 IBM TrackPoint', 'synaptics-pt/serio0/input0')
('/dev/input/event12', 'SynPS/2 Synaptics TouchPad', 'isa0060/serio1/input0')
('/dev/input/event11', 'Integrated Camera', 'usb-0000:00:14.0-8/button')
('/dev/input/event10', 'PC Speaker', 'isa0061/input0')
('/dev/input/event9', 'HDA Intel PCH Headphone', 'ALSA')
('/dev/input/event8', 'HDA Intel PCH Dock Headphone', 'ALSA')
('/dev/input/event7', 'HDA Intel PCH Mic', 'ALSA')
('/dev/input/event6', 'HDA Intel PCH Dock Mic', 'ALSA')
('/dev/input/event5', 'ThinkPad Extra Buttons', 'thinkpad_acpi/input0')
('/dev/input/event4', 'Video Bus', 'LNXVIDEO/video/input0')
('/dev/input/event3', 'AT Translated Set 2 keyboard', 'isa0060/serio0/input0')
('/dev/input/event2', 'Power Button', 'LNXPWRBN/button/input0')
('/dev/input/event1', 'Sleep Button', 'PNP0C0E/button/input0')
('/dev/input/event0', 'Lid Switch', 'PNP0C0D/button/input0')`

My keyboard is /dev/input/event3.

You start the script with the right device like this:

`keylight.py -d /dev/input/event3`

## Finding a key combination

When the command is run, it is not controlling the backlight. There is a keycombiantion
(default is windows key + F12) which activates it.

To find another key combination, you can use the script to dump keys:

`keylight.py --keys`

When running this and pressing ctrl+shift you will get:

`Showing pressed key codes. Press ctrl-c to abort
[]
[29]
[29, 42]
[42]
[]
[29]
[29, 46]
^CTraceback (most recent call last):
  File "./keylight.py", line 71, in <module>
    for event in dev.read_loop():
  File "/usr/local/lib/python2.7/dist-packages/evdev/device.py", line 280, in read_loop
    r, w, x = select([self.fd], [], [])
KeyboardInterrupt`

The tricky bit here is finding which codes correspond to the ctrl+shift. In this example
it is 29,42.

To start the script with this key combination, use:

`keylight.py --hotkeys=29,42`

## Example

For my laptop, with windowskey + F12 as hotkey, I start the command like this:

`keylight.py --hotkeys=88,12 --offset=13 --ledon=0x45 --ledoff=0x05 -t 5 -d /dev/input/event3`
