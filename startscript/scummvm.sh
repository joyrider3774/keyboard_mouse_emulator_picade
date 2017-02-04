#!/usr/bin/env bash

sudo python /opt/retropie/configs/all/keyboardmouseemulator.py &
/opt/retropie/configs/scummvm/bin/scummvm $@
sudo pkill --signal SIGTERM -f keyboardmouseemulator.py

