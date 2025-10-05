#!/bin/bash
arduino-cli compile --fqbn arduino:avr:uno ~/Arduino/$1
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno ~/Arduino/$1
