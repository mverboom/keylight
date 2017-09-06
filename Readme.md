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

The script originally worked by poking around some bytes, but in more recent
kernels there is support for the keyboard backlight through /sys, which is a lot
nicer.

## Requirements

You will need python evdev to run this script. Also, you need to be root and do some
searching to start the script with the correct values for your laptop.

## Finding the keyboard

Now with the information on the backlight found, we need to find the keyboard device. Just
run

`keylight.py -l`

for a list of input devices. The output can look something like this:

```
keylight.py -l
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
('/dev/input/event0', 'Lid Switch', 'PNP0C0D/button/input0')
```

My keyboard is /dev/input/event3.

You start the script with the right device like this:

`keylight.py -d /dev/input/event3`

## Finding a key combination

When the command is run, it is not controlling the backlight. There is a keycombiantion
(default is windows key + F12) which activates it.

To find another key combination, you can use the script to dump keys:

`keylight.py --keys`

When running this and pressing ctrl+shift you will get:

```
Showing pressed key codes. Press ctrl-c to abort
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
KeyboardInterrupt
```

The tricky bit here is finding which codes correspond to the ctrl+shift. In this example
it is 29,42.

To start the script with this key combination, use:

`keylight.py --hotkeys=29,42`

## Example

For my laptop, with windowskey + F12 as hotkey, I start the command like this:

`keylight.py --hotkeys=88,12 -t 5 -d /dev/input/event3`

## Installation for systemD
* Check-out the software in /opt/keylight
* Copy keylight.service to /etc/systemd/system
* Edit /opt/keylight/keylight.conf
* Reload systemd
`systemctl daemon-reload`
* Enable and start the service
```
systemctl enable keylight
systemctl start keylight
```
