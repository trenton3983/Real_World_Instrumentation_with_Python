#! /usr/bin/python
#-------------------------------------------------------------------------------
# console6.py
# Demonstrates the use of the SimpleANSI module.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import random
import time
import datetime
import threading
import SimpleANSI

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
def writeDateTime():
    getDate()
    getTime()

    term.clrEOL(2,15)
    term.movePos(2,15)
    term.writeOutput("%s" % currdate)
    term.clrEOL(3,15)
    term.movePos(3,15)
    term.writeOutput("%s" % currtime)

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
def writeDataVals():
    idx = 0
    for i in range(6,14):
        term.movePos(i,10)
        term.writeOutput("%6.2f" % data_vals[idx])
        idx += 1
    # put cursor below display text when update is done
    term.movePos(16,1)

# generate the main display
def mainScreen():
    term.clrScreen()

    term.movePos(1,1)
    term.writeOutput("Input Data Monitor")

    term.movePos(2,1)
    term.writeOutput("Current Date:")
    term.movePos(3,1)
    term.writeOutput("Current Time:")
    writeDateTime()

    term.movePos(5,1)
    term.writeOutput("Chan    Last Value")

    rownum = 1
    for row in range(6,14):
        term.movePos(row,1)
        term.writeOutput("  %d" % rownum)
        rownum += 1

    writeDataVals()

    term.movePos(15,1)
    term.writeOutput("Enter X to exit.")

# raw_input() handler Thread
def getCommand():
    global exit_loop

    while True:
        instr = raw_input()
        if instr.upper() == 'X':
            exit_loop = True
            break
        time.sleep(0.1)

#---------------------------------------------------------------------
# main loop
#---------------------------------------------------------------------
term = SimpleANSI.ANSITerm(None, 0)

exit_loop = False

# launch the raw_input() handler thread
getinput = threading.Thread(target=getCommand)
getinput.start()

mainScreen()

while exit_loop == False:
    writeDateTime()
    getDataVals()
    writeDataVals()
    time.sleep(0.2)
