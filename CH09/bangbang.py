#-------------------------------------------------------------------------------
# bangbang.py
# A simple implementation of a bang-bang controller.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import time     # needed for sleep

# psuedo-constants
OFF = 0
ON  = 1

H = 2.0             # hysteresis range
delay_time = 0.1    # loop delay time

# replace these as appropriate to refer to real input and output
temp_sense = 0
device     = 0

def BangBang():
    do_loop = True
    sys_state = OFF

    while (do_loop):
        if not do_loop:
            break

        curr_temp = Acquire(temp_sense)     # dummy placeholder

        if curr_temp <= set_temp - H:
            sys_state = OFF

        if curr_temp >= set_temp + H:
            sys_state = ON

        # it is assumed that setting the port with the same value isn't
        # going to cause any problems, and the output will only change
        # when the input changes
        SetPort(device, sys_state)          # dummy placeholder

        time.sleep(delay_time)
