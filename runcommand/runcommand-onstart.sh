#!/usr/bin/env bash

system="$1"

if [ "$system" = "scummvm" ]; 
then
  nohup sudo python /opt/retropie/configs/all/keyboardmouseemulator.py &>/dev/null &
fi