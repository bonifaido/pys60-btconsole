#!/usr/bin/env python

import serial
import readline
import time
import sys

bluetooth = serial.Serial(port="/dev/tty.Bluetooth-PDA-Sync", timeout=10, rtscts=True)
bluetooth.open()
if bluetooth.isOpen():
	print "Bluetooth is open now."
	print "Waiting for device to connect..."
else:
	print "Failed to open Bluetooth connection."
	sys.exit(0)

out_line = ""

while True:
	
	while True:
		in_line = bluetooth.readline()
		if bluetooth.inWaiting() == 0:
			in_line = bluetooth.readline()
			if in_line != ">>> \r\n":
				print in_line,
				break
		if (bluetooth.inWaiting() - 4) <= 0:
			break
		if in_line != out_line+"\r\n": # skip the comingback check string
			print in_line,
		time.sleep(0.2)
		if (bluetooth.inWaiting() - 4) <= 0:
			break
	
	out_line = raw_input(">>> ")
	while out_line == "":
		out_line = raw_input(">>> ")
	bluetooth.write(out_line + "\r\n")
	if out_line == "exit":
		bluetooth.close()
		sys.exit(0)
	bluetooth.flush()
	bluetooth.flushInput()
	#bluetooth.flushOutput()

bluetooth.close()
