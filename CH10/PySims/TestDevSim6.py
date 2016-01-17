#! /usr/bin/python
#-------------------------------------------------------------------------------
# TestDevSim6.py
#-------------------------------------------------------------------------------
# Demonstrate cyclic data generation of a sine wave.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import  time
from    DevSim  import  DevSim
import  SimLib.RetCodes as RC
import  DevSim.DevSimDefs as DS


def testDevSim6():
    print "Init DevSim"
    simIO = DevSim.DevSim()

    # set up the simulated device
    simIO.setInputSrc(DS.INCHAN1, DS.CYCLIC)

    simIO.setCyclicRate(DS.INCHAN1, 0.1)
    simIO.setCyclicType(DS.INCHAN1, DS.CYCSINE)
    simIO.setCyclicLevel(DS.INCHAN1, 2.5)
    simIO.setCyclicOffset(0)

    simIO.setOutputDest(DS.OUTCHAN1, DS.INCHAN1)

    simIO.startSim = True
    time.sleep(1)

    loopcount = 0
    while loopcount < 50:
        print simIO.readData(DS.OUTCHAN1)[1]
        loopcount += 1

    simIO.stopSim = True    # set the stop flag
    print "DevSim terminated"


# change the first line to point to the location of your python interpreter,
# if necessary.
if __name__ == '__main__':
    testDevSim6()
