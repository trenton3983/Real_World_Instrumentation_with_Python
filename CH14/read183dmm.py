#!/usr/bin/python
# 183 DMM data capture example
#
# Simple demonstration of data acquistion from a DMM
#
# Source code from the book "Real World Instrumentation with Python"
# By J. M. Hughes, published by O'Reilly.

import serial

# Assume that the serial interface is one of (a) an actual RS-232
# port, (b) an actual RS-232 port with an RS-485 adapter, or (c) a
# USB to RS-232 or RS-485 adapter via a virtual serial port.
sport = serial.Serial()
sport.baudrate = 1200
sport.port = "com17"
sport.setTimeout(2) # give up after 5 seconds
sport.open()

instr = ""
fetch_data = True
short_count = 0
timeout_cnt = 0
maxtries = 5    # timeout = read timeout * maxtries

while fetch_data:
    # send RI command to device


    getstr = True
    # input string read loop - get one character at a time from
    # the DMM to build up an input string
    # an input string
    while getstr:
        inchar = sport.read(1)
        if inchar == "":
            # reading nothing is a sign of a timeout
            print "%s timeout, count: %d" % (inchar, timeout_cnt)
            timeout_cnt += 1
            if timeout_cnt > maxtries:
                getstr = False
        else:
            # see if the terminator character was read and if so
            # then call this input string done
            if inchar == '&':
                getstr = False
            instr += inchar
            timeout_cnt = 0     # reset timeout counter

    # if timeout occurred then don't continue
    if timeout_cnt == 0:
        if len(instr) > 9:
            # chances if this being a valid string are good, so
            # pull out the data
            fcode = instr[0]
            mcode = instr[1]
            rcode = instr[2]
            data = instr[4:len(instr)-1]

            # actual display and/or logging code goes here
            # the print is just a placeholder for this example
            print "%1s %1s %1s ->  %s" % (fcode, mcode, rcode, data)

            # reset the short read counter
            short_count = 0
        else:
            # if we get repeated consecutive short strings then
            # there's a problem
            short_count += 1
            # if it happens 5 times in a row then terminate the
            # loop and exit the script
            if short_count > 5:
                fetch_data = False
        # in any case, clear the input string
        instr = ""
    else:
        # we get to here if a timeout occurred in the input string
        # read loop, so kill the main loop
        fetch_data = False

print "Data acquistion terminated"
