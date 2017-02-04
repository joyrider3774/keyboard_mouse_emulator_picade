# Keyboard to mouse emulator for picade / keyboard encoders / arcade cabinets

I Created this python script to use with my [Picade][picadesite]. It emulates mouse movement using keyboard keys as well as support remapping of 6 extra keys to other keys (an emulator or game) expects to be pressed. I have created this specifically for scummvm on which runs on my Raspberry Pi using the [Retropie][retropiesite] images. The script however is very small and can be easily modified to be used with any keyboard or keyboard encoder and it's easy to add extra keys if your arcade cabinet has more pushbuttons.

It currently supports the following:
  - Switch between emulated mouse mode and your keyboard /  arcade stick & buttons (if using a keyencoder)
  - Emulates 8 way mouse movement, mouse button left, middle and right
  - 6 Extra keys available to be (re)mapped to any key you like
  - easy to configure
  - uses [python-evdev][python-evdevsite] so should (theoretically) normally work with any linux variant / system
  - made with retropie in mind, it uses the runcommand addon scripts to start and stop the emulator when scummvm starts (as an exmaple)

### Installation

the repository contains 3 scripts:
 - [keyboardmouseemulator.py][keyboardmouseemulator.py]: the main emulator file at least this file is needed
 - [listdevices.py][listdevices.py]: helper script to identify your keyboard / keyboard encoder `/dev/input/event?` device and list the keys you can use for the configuration. 
 - [findoutkeycodes.py][findoutkeycodes.py]: helper script to show you the numerical values of the keycodes, you can use this to easily find out the keycode for the button you pressed (key on your keybboard / keyencoder)

The keyboard to mouse emulator uses [python][python], [python-evdev][python-evdevsite], pkill these are all pre-installed on the raspberry pi image i had used but i'm not certain if that's always the case so you should check if python is installed and if you can run the pkill command.

the 3 python scripts need to be copied from the repository to the /opt/retropie/configs/all folder on the raspberry pi. You can do this using the samba share, ssh file transfer, ftp or any other means you have to access the files on your retropie image.

### Configuration
you can skip configuration if you are planning on using this with a picade for scummvm the defaults should be correct

##### Specifying the input device 
[findoutkeycodes.py][findoutkeycodes.py] and [keyboardmouseemulator.py][keyboardmouseemulator.py] have a variable named `keyboardinputdevice` which should point to the device your keyboard encoder / keyboard uses (attached to your joysticks / buttons on the picade). The default value is `/dev/input/event0`, i think in most case this might be the correct one if not run [listdevices.py][listdevices.py] using ssh and try to see which yours is using. 

You can run the script like this:
```sh
$ sudo python /opt/retropie/configs/all/listdevice.py
```
it will display a lot of information like this
```
('/dev/input/event0', 'Arduino LLC Arduino Leonardo', 'usb-3f980000.usb-1.3/input2')
{('EV_MSC', 4L): [('MSC_SCAN', 4L)], ('EV_KEY', 1L): [('KEY_ESC', 1L), ('KEY_1', 2L), ('KEY_2', 3L), ('KEY_3', 4L), ('KEY_4', 5L), ('KEY_5', 6L), ('KEY_6', 7L), ('KEY_7', 8L), ('KEY_8', 9L), ('KEY_9', 10L), ('KEY_0', 11L), ('KEY_MINUS', 12L), ('KEY_EQUAL', 13L), ('KEY_BACKSPACE', 14L), ('KEY_TAB', 15L), ('KEY_Q', 16L), ('KEY_W', 17L), ('KEY_E', 18L), ('KEY_R', 19L), ('KEY_T', 20L), ('KEY_Y', 21L), ('KEY_U', 22L), ('KEY_I', 23L), ('KEY_O', 24L), ('KEY_P', 25L), ('KEY_LEFTBRACE', 26L), ('KEY_RIGHTB...........
```
The picade i use uses an arduino leonardo for it's keyboard encoder so i know this is the correct one by looking at the name. Once you identified your keyboard / encoder device look for `/dev/input/event0` line this is what you need to place inside `keyboardinputdevice` variable so it looks like this in the code `keyboardinputdevice = '/dev/input/event0'`in both files. 

##### Specifying the buttons and joystick values to be used for mouse emulation mode 
[keyboardmouseemulator.py][keyboardmouseemulator.py] has a section that needs to be modified if you are not using a picade or have no intention on using this only for scummvm on the raspberry pi. You need to specify which keys to use for mouse up / down / left / right (joystick on the picade), mouse button left / middle / right (buttons on the picade) as well as the extra keys you want to use. The default setup is made for scummvm emulator using a picade. these are the values that you need / can change:

these for the mouse emulation
```
MOUSEUP = e.KEY_UP
MOUSEDOWN = e.KEY_DOWN
MOUSELEFT = e.KEY_LEFT
MOUSERIGHT = e.KEY_RIGHT
MOUSEBUTTONLEFT = e.KEY_LEFTSHIFT
MOUSEBUTTONMIDDLE = e.KEY_Z
MOUSEBUTTONRIGHT = e.KEY_X
KEYMODIFIER = e.KEY_C
KEYMOUSEMODE = e.KEY_LEFTSHIFT
```
they key specified in `KEYMODIFIER` is a key (attached to a button on your picade / keyboard / encoder) that needs to be pressed together with the key specified in `KEYMOUSEMODE` to enable mouse emulation. Mouse emulation does not start by default you have to press those keys once when scummvm or any other app starts

```
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
#F5 is needed as well (for ctrl+f5 -> menu for quiting + saving in some games)
KEYMOUSEMODEKEYTOSEND4 = e.KEY_F5
KEYMOUSEMODEKEYTOPRESS4 = e.KEY_LEFTCTRL
#Y key for answering Y / N questions
KEYMOUSEMODEKEYTOSEND5 = e.KEY_Y
KEYMOUSEMODEKEYTOPRESS5 = e.KEY_LEFTALT
#N key for answering Y / N questions
KEYMOUSEMODEKEYTOSEND6 = e.KEY_N
KEYMOUSEMODEKEYTOPRESS6 = e.KEY_SPACE
```

These are the extra keys that you can specify you need to specify one key to press on the picade / your keyboard / encoder and key that will be used in the application. For exmple `KEYMOUSEMODEKEYTOSEND4 = e.KEY_F5` and `KEYMOUSEMODEKEYTOPRESS4 = e.KEY_LEFTCTRL` mean that when i press the button attached to `LEFT_CTRL` on my encoder / keyboard that it won't register the key `LEFT_CTRL´ but `F5` instead. So i'm basically remapping my keys to something the application (scummvm) uses.

to find out these values, use the number codes returned by [findoutkeycodes.py][findoutkeycodes.py] or the key names by looking at the output of [listdevices.py][listdevices.py] when running a ssh terminal. When using [findoutkeycodes.py][findoutkeycodes.py] you need to press a button you picade / keyboard / encoder while the script is running, it will then display a unique number for each key you pressed. Note each value down along with the key / button it belangs to.

```sh
$ sudo python /opt/retropie/configs/all/findoutkeycodes.py
```
## Usuage
you basically need a way to start the mouse emulator then start the game (scummvm in my case) and then quit the mouse emulator when the game (scummvm) quits. You need to absolutely do it this way because if you leave the emulator running some other emulators might not register your keyboard encoder anymore the only way to be sure this does not happen is to quit the mouse emulator before starting another emualator / app / game.

### Usuage using scummvm on retropie 4.0.2 and above with the runncommando scripts

you can use the [runcommand-onend.sh][runcommand-onend.sh] and [runcommand-onstart.sh][runcommand-onstart.sh] files and copy them to `/opt/retropie/configs/all/listdevice.py` so on the same location as the other runcommand in the config/all directory of retropie. it contains code to start the mouse emulator when scummvm starts and quits the emulator when scummvm quits.if the files already exist copy everything except the first line to the end of the files

once you start a game using `emulation station` and scummvm is running you need to press the buttons / keys assigned to `KEYMODIFIER` and `MOUSEMODE` at the same time. If you have setup everything correctly the emulator should have been started when scummvm started and you are now in mouse mode, if you use the buttons assigned to `MOUSEUP` `MOUSEDOWN` etc you should see the mouse moving. If not make sure you have specified the correct `/dev/input/event` device in the scripts.
you can switch back to your normal keyboard / encoder / button configuration by pressing both buttons again.

### Usuage using alternative starting method

You can use this [scummvm.sh][scummvm.sh] python script (as an example), that starts the mouse emulator then starts then scummvm emulator and after scummvm quits it quits the mouse emulator. You need to edit your frontend configuration to launch [scummvm.sh][scummvm.sh] instead of the runcommand or instead of directly linking agains the emulator binary.

## Known problems
- Some emulators or games use this emulator instead of the actual connected keyboard / mouse / encoder, if you leave the mouse emulator running, don't leave it running for ever !!! quit it before running another emulator / game / app

   [picadesite]: <https://shop.pimoroni.com/products/picader>
   [retropiesite]: <https://retropie.org.uk>
   [python-evdevsite]: <https://python-evdev.readthedocs.io/en/latest/>
   [python]: <https://www.python.org>
   [keyboardmouseemulator.py]: <https://github.com/joyrider3774/keyboard_mouse_emulator_picade/blob/master/keyboardmouseemulator.py>
   [listdevices.py]: <https://github.com/joyrider3774/keyboard_mouse_emulator_picade/blob/master/listdevices.py>
   [findoutkeycodes.py]: <https://github.com/joyrider3774/keyboard_mouse_emulator_picade/blob/master/findoutkeycodes.py>
   [runcommand-onend.sh]: <https://github.com/joyrider3774/keyboard_mouse_emulator_picade/blob/master/runcommand/runcommand-onend.sh>
   [runcommand-onstart.sh]: <https://github.com/joyrider3774/keyboard_mouse_emulator_picade/blob/master/runcommand/runcommand-onstart.sh>
   [scummvm.sh]: <https://github.com/joyrider3774/keyboard_mouse_emulator_picade/blob/master/startscript/scummvm.sh>
 