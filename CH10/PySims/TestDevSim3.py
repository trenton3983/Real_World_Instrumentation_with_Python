#! /usr/bin/python
#-------------------------------------------------------------------------------
# TestDevSim3.py
#-------------------------------------------------------------------------------
# Demonstrates the use of a user-defined function string.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import  time
from    DevSim  import  DevSim
import  SimLib.RetCodes as RC
import  DevSim.DevSimDefs as DS


def testDevSim3():
    print "Init DevSim"
    simIO = DevSim.DevSim()

    # set up the simulated device
    simIO.setInputSrc(DS.INCHAN1, DS.EXT_IN)
    simIO.setOutputDest(DS.OUTCHAN1, DS.INCHAN1)
    simIO.setFunction(DS.INCHAN1, "x0 * 2")

    simIO.startSim = True
    time.sleep(1)

    loopcount = 0
    while loopcount < 10:
        # send data to simulator
        simIO.sendData(DS.INCHAN1, loopcount)

        # acquire data input from simulator with function applied
        rc, simdata = simIO.readData(DS.OUTCHAN1)
        if rc != RC.NO_ERR:
            print "DevSim returned: %d on read" % rc
            break

        print "%d %f" % (loopcount, simdata)

        loopcount += 1
    # loop back for more

    simIO.stopSim = True
    print "DevSim terminated"


# change the first line to point to the location of your python interpreter,
# if necessary.
if __name__ == '__main__':
    testDevSim3()
