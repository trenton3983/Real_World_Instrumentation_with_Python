#! /usr/bin/python
#-------------------------------------------------------------------------------
# curses1.py
# Demonstrates the use of Python's curses module.
# Translated from the console6.py example.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import random
import time
import datetime
import curses
import traceback

data_vals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
currdate = ""
currtime = ""
updt_cnt1 = 0
updt_cnt2 = 0

ran = random.random

def getDate():
    global currdate

    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    yr = str(currdatetime[0])
    currdate = "%02d"%int(yr[2:]) + "%02d"%currdatetime[1] + "%02d"%currdatetime[2]

def getTime():
    global currtime

    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    currtime = "%02d:"%currdatetime[3] + "%02d:"%currdatetime[4] + "%02d"%currdatetime[5]

# write data and time to display
def writeDateTime(win):
    getDate()
    getTime()

    win.move(2,15)
    win.clrtoeol()
    win.addstr("%s" % currdate)
    win.move(3,15)
    win.clrtoeol()
    win.addstr("%s" % currtime)
    win.refresh()

# get simulated data input values
def getDataVals():
    global data_vals, updt_cnt1, updt_cnt2

    data_vals[0] = ran() * 10.0
    data_vals[1] = ran() * 10.0

    if updt_cnt1 >= 4:
        for i in range(2,5):
            data_vals[i] = ran() * 10.0
        updt_cnt1 = 0
    else:
        updt_cnt1 += 1

    if updt_cnt2 >= 10:
        for i in range(4,8):
            data_vals[i] = ran() * 10.0
        updt_cnt2 = 0
    else:
        updt_cnt2 += 1

# write channel data values
def writeDataVals(win):
    idx = 0
    for i in range(6,14):
        win.move(i,10)
        win.clrtoeol()
        win.addstr("%6.2f" % data_vals[idx])
        idx += 1

    win.refresh()
    # put cursor below display text when update is done
    win.move(16,1)

# generate the main display
def mainScreen(win):
    win.erase()

    win.move(1,1)
    win.addstr("Input Data Monitor")
    win.refresh()

    win.move(2,1)
    win.addstr("Current Date:")
    win.move(3,1)
    win.addstr("Current Time:")
    win.refresh()

    writeDateTime(win)

    win.move(5,1)
    win.addstr("Chan    Last Value")
    win.refresh()

    rownum = 1
    for row in range(6,14):
        win.move(row, 1)
        win.addstr("  %d" % rownum)
        rownum += 1
    win.refresh()

    writeDataVals(win)

    win.move(15,1)
    win.addstr("Enter X to exit.")
    win.refresh()

def mainloop(win):
    win.nodelay(1)  # disable getch() blocking
    # draw the main display template
    mainScreen(win)

    # run until the user wants to quit
    while 1:
        # check for keyboard input
        inch = win.getch()
        # getch() will return -1 if no character is available
        if inch != -1:
            # see if inch is really a character
            try:
                instr = str(chr(inch))
            except:
                # just ignore non-character input
                pass
            else:
                if instr.upper() == 'X':
                    break
        writeDateTime(win)
        getDataVals()
        writeDataVals(win)
        time.sleep(0.2)

def startup():
    # borrowed the idea of using a try-except wrapper around the
    # initialization from David Mertz.
    try:
        # Initialize curses
        stdscr = curses.initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        mainloop(stdscr)                # Enter the main loop

        # Set everything back to normal
        curses.echo()
        curses.nocbreak()

        curses.endwin()                 # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception

if __name__=='__main__':
    startup()
