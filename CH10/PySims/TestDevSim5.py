#! /usr/bin/python
#-------------------------------------------------------------------------------
# TestDevSim5.py
#-------------------------------------------------------------------------------
# Exercises all four channels. The first channel simply echos input data to a
# specified output. The second channel applies a user-defined functon to the
# input data. The third channel scales data read from a file. The fourth channel
# applies random data to simulate noise.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import  time
from    DevSim  import  DevSim
import  SimLib.RetCodes as RC
import  DevSim.DevSimDefs as DS


def testDevSim5():
    print "Init DevSim"
    simIO = DevSim.DevSim()

    # channel 1
    # echo INCHAN1 to OUTCHAN1, no modifications
    simIO.setInputSrc(DS.INCHAN1, DS.EXT_IN)
    simIO.setOutputDest(DS.OUTCHAN1, DS.INCHAN1)

    # channel 2
    # echo INCHAN1 to OUTCHAN1, apply function
    simIO.setInputSrc(DS.INCHAN2, DS.EXT_IN)
    simIO.setOutputDest(DS.OUTCHAN2, DS.INCHAN2)
    simIO.setFunction(DS.INCHAN2, "x0 * 1.2")

    # channel 3
    # read data from file, scale it and send to OUTCHAN3
    rc = simIO.setDataFile(DS.SRCFILE1, None, "indata1.dat")
    if rc != RC.NO_ERR:
        print "Error opening input data file"
        print "DevSim start aborted"
        return
    simIO.setOutputDest(DS.OUTCHAN3, DS.SRCFILE1)
    simIO.setDataScale(DS.OUTCHAN3, 1.5)

    # channel 4
    # add noise to file data and send to OUTCHAN4
    rc = simIO.setDataFile(DS.SRCFILE2, None, "indata2.dat")
    if rc != RC.NO_ERR:
        print "Error opening input data file"
        print "DevSim start aborted"
        return
    simIO.setOutputDest(DS.OUTCHAN4, DS.SRCFILE2)
    # mix in some noise into the data
    simIO.setRandScale(DS.OUTCHAN4, 0.15)

    simIO.startSim = True
    time.sleep(1)

    loopcount = 0
    while loopcount < 20:
        simIO.sendData(DS.INCHAN1, (loopcount * .25))
        simIO.sendData(DS.INCHAN2, (loopcount * .25))

        rc, dval1 = simIO.readData(DS.OUTCHAN1, block=True)
        rc, dval2 = simIO.readData(DS.OUTCHAN2, block=True)
        rc, dval3 = simIO.readData(DS.OUTCHAN3, block=True)
        rc, dval4 = simIO.readData(DS.OUTCHAN4, block=True)

        print "%2d %4.2f %4.2f %4.2f %4.2f" % (loopcount, dval1, dval2, dval3, dval4)

        loopcount += 1

    simIO.stopSim = True    # set the stop flag
    print "DevSim terminated"


# change the first line to point to the location of your python interpreter,
# if necessary.
if __name__ == '__main__':
    testDevSim5()
