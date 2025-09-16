#!/bin/bash

if [ -e /home/pi/cs-rereminibot/minibot/pi_scripts/pi_zero_script.py ]; then
  cd /home/pi/cs-rereminibot
  sudo python minibot/pi_scripts/pi_zero_script.py
  sudo reboot -h now
else
  read -p "No pi_zero_script.py"
fi
