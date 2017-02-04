import signal
from evdev import InputDevice, list_devices,  UInput, AbsInfo, list_devices, events, util, ecodes as e
from time import sleep

#you may change these values below
keyboardinputdevice = '/dev/input/event0'
speed = 5

#for these assign your picade or keyboard controller

#keys to control the mouse and the modifier key
#and mouse modekey if modifier and mousemodekey
#is pressed on the picade / keyboard encoder
#the mouse mode gets activated
MOUSEUP = e.KEY_UP
MOUSEDOWN = e.KEY_DOWN
MOUSELEFT = e.KEY_LEFT
MOUSERIGHT = e.KEY_RIGHT
MOUSEBUTTONLEFT = e.KEY_LEFTSHIFT
MOUSEBUTTONMIDDLE = e.KEY_Z
MOUSEBUTTONRIGHT = e.KEY_X
KEYMODIFIER = e.KEY_C
KEYMOUSEMODE = e.KEY_LEFTSHIFT

#for these choose a key that should be send when in mouse mode
#as well as the key you want it assigned to from your picade
#so basically you can (re)define some extra keys for use in mouse mode

#4 keys, joystick ones not counted are in use, the modifier key
#mouse button left, right and middle
#So on the picade i have 5 extra spare keys to use
#if you need more alter the code to add extra keys for your encoder


#escape to skip scenes intro's on scummvm (default mapping is fine)
KEYMOUSEMODEKEYTOSEND1 = e.KEY_ESC
KEYMOUSEMODEKEYTOPRESS1 = e.KEY_ESC
#enter might be helpfull (default mapping is fine)
KEYMOUSEMODEKEYTOSEND2 = e.KEY_ENTER
KEYMOUSEMODEKEYTOPRESS2 = e.KEY_ENTER
#CTRL is needed in scummvm (for ctrl+f5 -> menu)
#there normally is a CTRL key assinged on the picade's
#keyboard encoder but i wanted the CTRL key to be the 
#the 2nd key (right one) on the front panel 
#that's why i'm remapping this one
KEYMOUSEMODEKEYTOSEND3 = e.KEY_LEFTCTRL
KEYMOUSEMODEKEYTOPRESS3 = e.KEY_S
#F5 is needed as well (for ctrl+f5 -> menu for quiting / saving)
KEYMOUSEMODEKEYTOSEND4 = e.KEY_F5
KEYMOUSEMODEKEYTOPRESS4 = e.KEY_LEFTCTRL
#Y key for answering Y / N questions
KEYMOUSEMODEKEYTOSEND5 = e.KEY_Y
KEYMOUSEMODEKEYTOPRESS5 = e.KEY_LEFTALT
#N key for answering Y / N questions
KEYMOUSEMODEKEYTOSEND6 = e.KEY_N
KEYMOUSEMODEKEYTOPRESS6 = e.KEY_SPACE

#don't change these values below
sleeptime = 0.015
left = False
right = False
up = False
down = False
canquit = False
mousemode = False
modifierkey = False
mousemodekey = False
canchangemousemode = False
keysleeptime = 0.025
devicename = 'SCUMMVM-mouse-emulator'
first = True

mouse = {
    e.EV_KEY : [e.BTN_MOUSE, e.BTN_RIGHT, e.BTN_MIDDLE, 
      KEYMOUSEMODEKEYTOSEND1, KEYMOUSEMODEKEYTOSEND2, 
      KEYMOUSEMODEKEYTOSEND3, KEYMOUSEMODEKEYTOSEND4, 
      KEYMOUSEMODEKEYTOSEND5, KEYMOUSEMODEKEYTOSEND6],
    e.EV_REL : [e.REL_X, e.REL_Y],
    e.EV_MSC : [e.MSC_SCAN]
}

ui = UInput(mouse, name=devicename, version =0x3)

device = InputDevice(keyboardinputdevice)

print(device)

def signal_handler(signal, frame):
  global canquit
  canquit = True

signal.signal(signal.SIGINT, signal_handler)

while not canquit:
  #simulate relative mouse movement
  if (up or right or down or left) and mousemode:
    if up:
      ui.write(e.EV_REL, e.REL_Y, -speed)
    if down:
      ui.write(e.EV_REL, e.REL_Y, speed)
    if left:
      ui.write(e.EV_REL, e.REL_X, -speed)
    if right:
      ui.write(e.EV_REL, e.REL_X, speed)
  ui.syn()

  #keys must be released otherwise when we grab the real input
  #device it never sended a key up making the program running
  #still think the key is pressed
  if not modifierkey and not mousemodekey and canchangemousemode:
    mousemode = not mousemode
    canchangemousemode = False
    if mousemode:
      device.grab()
    else:
      device.ungrab()


  sleep(sleeptime)


  event = device.read_one() 
  if event is None:
    continue

  if event.type == e.EV_KEY:
    keyevent = util.categorize(event)

    if (keyevent.keystate == keyevent.key_down or
      keyevent.keystate == keyevent.key_hold):
        if keyevent.scancode == MOUSEDOWN:
          down = True
        if keyevent.scancode == MOUSEUP:
          up = True
        if keyevent.scancode == MOUSELEFT:
          left = True
        if keyevent.scancode == MOUSERIGHT:
          right = True         
        if keyevent.scancode == KEYMODIFIER:
          modifierkey = True
        if keyevent.scancode == KEYMOUSEMODE:
          mousemodekey = True

    if (keyevent.keystate == keyevent.key_up):
        if keyevent.scancode == MOUSEDOWN:
          down = False
        if keyevent.scancode == MOUSEUP:
          up = False
        if keyevent.scancode == MOUSELEFT:
          left = False
        if keyevent.scancode == MOUSERIGHT:
          right = False
        if keyevent.scancode == KEYMODIFIER:
          modifierkey = False
          if mousemodekey:
            canchangemousemode = True
        if keyevent.scancode == KEYMOUSEMODE:
          mousemodekey = False
          if modifierkey:  
            canchangemousemode = True

    if keyevent.scancode == MOUSEBUTTONLEFT and mousemode:
      ui.write(e.EV_KEY, e.BTN_MOUSE, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == MOUSEBUTTONMIDDLE and mousemode:
      ui.write(e.EV_KEY, e.BTN_MIDDLE, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == MOUSEBUTTONRIGHT and mousemode:
      ui.write(e.EV_KEY, e.BTN_RIGHT, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == KEYMOUSEMODEKEYTOPRESS1 and mousemode:
      ui.write(e.EV_KEY, KEYMOUSEMODEKEYTOSEND1, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == KEYMOUSEMODEKEYTOPRESS2 and mousemode:
      ui.write(e.EV_KEY, KEYMOUSEMODEKEYTOSEND2, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == KEYMOUSEMODEKEYTOPRESS3 and mousemode:
      ui.write(e.EV_KEY, KEYMOUSEMODEKEYTOSEND3, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == KEYMOUSEMODEKEYTOPRESS4 and mousemode:
      ui.write(e.EV_KEY, KEYMOUSEMODEKEYTOSEND4, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == KEYMOUSEMODEKEYTOPRESS5 and mousemode:
      ui.write(e.EV_KEY, KEYMOUSEMODEKEYTOSEND5, keyevent.keystate)
      ui.syn()

    if keyevent.scancode == KEYMOUSEMODEKEYTOPRESS6 and mousemode:
      ui.write(e.EV_KEY, KEYMOUSEMODEKEYTOSEND6, keyevent.keystate)
      ui.syn()

ui.close()

#release the real keyboard / encoder if we are still in mouse mode
if mousemode:
  device.ungrab()
