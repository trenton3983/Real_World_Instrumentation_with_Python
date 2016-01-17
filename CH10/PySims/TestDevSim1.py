#! /usr/bin/python
#-------------------------------------------------------------------------------
# TestDevSim1.py
#-------------------------------------------------------------------------------
# Echos data written into the simulator back to the output.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import  time
from    DevSim  import  DevSim
import  SimLib.RetCodes as RC
import  DevSim.DevSimDefs as DS


def testDevSim1():
    print "Init DevSim"
    simIO = DevSim.DevSim()

    # set up the simulated device
    simIO.setInputSrc(DS.INCHAN1, DS.EXT_IN)
    simIO.setOutputDest(DS.OUTCHAN1, DS.INCHAN1)

    simIO.startSim = True
    time.sleep(1)

    loopcount = 0
    while loopcount < 10:
        simIO.sendData(DS.INCHAN1, (5.0 + loopcount))
        print simIO.readData(DS.OUTCHAN1)
        loopcount += 1

    simIO.stopSim = True    # set the stop flag
    print "DevSim terminated"


# change the first line to point to the location of your python interpreter,
# if necessary.
if __name__ == '__main__':
    testDevSim1()
