from evdev import InputDevice, UInput, AbsInfo, list_devices, events, util, ecodes as e
from time import sleep

speed = 5
sleeptime = 0.015
sleepkeytime = 0.1
left = False
right = False
up = False
down = False

MOUSEUP = e.KEY_UP
MOUSEDOWN = e.KEY_DOWN
MOUSELEFT = e.KEY_LEFT
MOUSERIGHT = e.KEY_RIGHT
MOUSEBUTTONLEFT = e.KEY_LEFTSHIFT
MOUSEBUTTONMIDDLE = e.KEY_Z
MOUSEBUTTONRIGHT = e.KEY_X
KEYMENU = e.KEY_LEFTCTRL

keyboardinputdevice = '/dev/input/event0'
mouse = {
    e.EV_KEY : [e.BTN_MOUSE, e.BTN_RIGHT, e.BTN_MIDDLE, e.KEY_F5],
    e.EV_REL : [e.REL_X, e.REL_Y]
}

ui = UInput(mouse, name='keyboard-mouse-emulator', version =0x3)

device = InputDevice(keyboardinputdevice)
print(device)

while True:
   if up:
     ui.write(e.EV_REL, e.REL_Y, -speed)
   if down:
     ui.write(e.EV_REL, e.REL_Y, speed)
   if left:
     ui.write(e.EV_REL, e.REL_X, -speed)
   if right:
     ui.write(e.EV_REL, e.REL_X, speed)
   
   if up or right or down or left:
     ui.syn()
   
   sleep(sleeptime)

  
   event = device.read_one() 
   if event is None:
     continue

   if event.type == e.EV_KEY:
        keyevent = util.categorize(event)
        
        print(keyevent)
        
        if (keyevent.keystate == keyevent.key_down):
            if keyevent.scancode == MOUSEDOWN:
	        down = True
            if keyevent.scancode == MOUSEUP:
                up = True
            if keyevent.scancode == MOUSELEFT:
                left = True
            if keyevent.scancode == MOUSERIGHT:
                right = True         

        if (keyevent.keystate == keyevent.key_up):
            if keyevent.scancode == MOUSEDOWN:
                down = False
            if keyevent.scancode == MOUSEUP:
                up = False
            if keyevent.scancode == MOUSELEFT:
                left = False
            if keyevent.scancode == MOUSERIGHT:
                right = False

        if keyevent.scancode == MOUSEBUTTONLEFT:
            ui.write(e.EV_KEY, e.BTN_MOUSE, keyevent.keystate)
            ui.syn()
        
        if keyevent.scancode == MOUSEBUTTONMIDDLE:
           ui.write(e.EV_KEY, e.BTN_MIDDLE, keyevent.keystate)
           ui.syn()
        
        if keyevent.scancode == MOUSEBUTTONRIGHT:
           ui.write(e.EV_KEY, e.BTN_RIGHT, keyevent.keystate)
           ui.syn()

        if keyevent.scancode == KEYMENU:
           ui.write(e.EV_KEY, e.KEY_F5, keyevent.key_down)
           ui.write(e.EV_KEY, e.KEY_F5, keyevent.key_up)
           ui.syn()

ui.close()
