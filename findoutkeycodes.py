from evdev import InputDevice, UInput, AbsInfo, list_devices, events, util, ecodes as e
from time import sleep

keyboardinputdevice = '/dev/input/event0'

device = InputDevice(keyboardinputdevice)
print(device.fn, device.name, device.phys)

for event in device.read_loop():
    if event.type == e.EV_KEY:
        keyevent = util.categorize(event)
        print(keyevent.scancode)
