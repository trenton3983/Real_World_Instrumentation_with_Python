#! /usr/bin/python
#-------------------------------------------------------------------------------
# TestDevSim4.py
#-------------------------------------------------------------------------------
# Reads data from an input file and passes the data to the output. A
# data file containing at least 20 ASCII numeric values, one value per record,
# must exist in the current directory. Noise, in the form of random numbers,
# is applied to the data.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import  time
from    DevSim  import  DevSim
import  SimLib.RetCodes as RC
import  DevSim.DevSimDefs as DS


def testDevSim4():
    print "Init DevSim"
    simIO = DevSim.DevSim()

    # define the source file to use
    rc = simIO.setDataFile(DS.SRCFILE1, None, "indata1.dat")
    if rc != RC.NO_ERR:
        print "Error opening input data file"
        print "DevSim start aborted"
    else:
        # set up the simulated device
        simIO.setOutputDest(DS.OUTCHAN1, DS.SRCFILE1)

        # mix in some noise into the data
        simIO.setRandScale(DS.OUTCHAN1, 0.25)

        simIO.startSim = True
        time.sleep(1)

        loopcount = 0
        while loopcount < 20:
            # read and print data from file
            rc, dval = simIO.readData(DS.OUTCHAN1, block=True)
            if rc == RC.NO_ERR:
                print "%2d - %4.3f" % ((loopcount + 1), float(dval))
            else:
                print "%2d - error: %d" % rc
            loopcount += 1

        # done. close all files and exit
        simIO.stopSim = True
        print "DevSim terminated"


# change the first line to point to the location of your python interpreter,
# if necessary.
if __name__ == '__main__':
    testDevSim4()
