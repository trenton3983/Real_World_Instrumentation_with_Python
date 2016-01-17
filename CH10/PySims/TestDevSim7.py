#! /usr/bin/python
#-------------------------------------------------------------------------------
# TestDevSim6.py
#-------------------------------------------------------------------------------
# Demonstrate cyclic data generation of all four possible waveforms.
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

    # Channel 1
    simIO.setInputSrc(DS.INCHAN1, DS.CYCLIC)
    simIO.setCyclicRate(DS.INCHAN1, 0.1)
    simIO.setCyclicType(DS.INCHAN1, DS.CYCSINE)
    simIO.setCyclicLevel(DS.INCHAN1, 2.5)
    simIO.setCyclicOffset(0)
    simIO.setOutputDest(DS.OUTCHAN1, DS.INCHAN1)

    # Channel 2
    simIO.setInputSrc(DS.INCHAN2, DS.CYCLIC)
    simIO.setCyclicRate(DS.INCHAN2, 0.1)
    simIO.setCyclicType(DS.INCHAN2, DS.CYCPULSE)
    simIO.setCyclicLevel(DS.INCHAN2, 2.5)
    simIO.setCyclicOffset(0)
    simIO.setOutputDest(DS.OUTCHAN2, DS.INCHAN2)

    # Channel 3
    simIO.setInputSrc(DS.INCHAN3, DS.CYCLIC)
    simIO.setCyclicRate(DS.INCHAN3, 0.1)
    simIO.setCyclicType(DS.INCHAN3, DS.CYCRAMP)
    simIO.setCyclicLevel(DS.INCHAN3, 2.5)
    simIO.setCyclicOffset(0)
    simIO.setOutputDest(DS.OUTCHAN3, DS.INCHAN3)

    # Channel 4
    simIO.setInputSrc(DS.INCHAN4, DS.CYCLIC)
    simIO.setCyclicRate(DS.INCHAN4, 0.1)
    simIO.setCyclicType(DS.INCHAN4, DS.CYCSAW)
    simIO.setCyclicLevel(DS.INCHAN4, 2.5)
    simIO.setCyclicOffset(0)
    simIO.setOutputDest(DS.OUTCHAN4, DS.INCHAN4)

    simIO.startSim = True
    time.sleep(1)

    loopcount = 0
    while loopcount < 50:
        dval1 = simIO.readData(DS.OUTCHAN1)[1]
        dval2 = simIO.readData(DS.OUTCHAN2)[1]
        dval3 = simIO.readData(DS.OUTCHAN3)[1]
        dval4 = simIO.readData(DS.OUTCHAN4)[1]
        print "%2d %4.2f %4.2f %4.2f %4.2f" % (loopcount, dval1, dval2, dval3, dval4)
        loopcount += 1

    simIO.stopSim = True    # set the stop flag
    print "DevSim terminated"


# change the first line to point to the location of your python interpreter,
# if necessary.
if __name__ == '__main__':
    testDevSim6()
