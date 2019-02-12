#!/usr/local/bin/python3

"""\
Stream g-code to the uArm Swift Pro


---------------------
"""

import serial
import time
import os
import argparse

parser = argparse.ArgumentParser(description='Stream g-code file uArm. (pySerial and argparse libraries required)')
parser.add_argument('gcode_file', type=argparse.FileType('r'),
        help='g-code file to be streamed')
parser.add_argument('device_file',
        help='serial device path')
args = parser.parse_args()

# set when we start running
start = time.time()

# kill uarmcore left running from uArm Studio
os.system('killall uarmcore-2')
time.sleep(2)

# Open serial port at proper baud rate
s = serial.Serial(args.device_file,115200)

# set g-code file to open
f = args.gcode_file

# Wake up grbl
# s.write(str.encode('\r\n\r\n'))
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl
for line in f:
    # we need to skip any blank lines
    if line == '\n' :
        pass
    else :
        l = line.strip() # Strip all EOL characters for consistency
        print('Sending : ' + l)
        s.write(str.encode(l)) # Send g-code block to grbl
        s.write(str.encode('\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        grbl_out_str = grbl_out.decode()
        grbl_out_str.strip()
        print('RESPONSE: ', end = "")
        print(grbl_out_str, end = "")

# Wait here until grbl is finished to close serial port and file.
# next line is broken... fix it later I guess?
#raw_input("  Press <Enter> to exit and disable grbl.") 

# Close file and serial port
f.close()
s.close()

# calculate how long it ran
seconds = time.time() - start
if seconds > 60 :
	minutes = seconds / 60
	print("Drawing took {0:0.1f} minutes".format(minutes))
else :
	print("Drawing took {0:0.1f} seconds".format(seconds))

