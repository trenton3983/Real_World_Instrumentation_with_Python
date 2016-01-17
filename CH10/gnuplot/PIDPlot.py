#! /usr/bin/python
#-------------------------------------------------------------------------------
# PIDPlot.py
# PID controller demonstation
#-------------------------------------------------------------------------------
# Uses gnuplot to generate a graph of the PID function's output
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import time
import timeit
import os
import PID

def PIDPlot(Kp=1, Ki=0, Kd=0):
    pid = PID.PID()

    pid.SetKp(Kp)
    pid.SetKi(Ki)
    pid.SetKd(Kd)

    time.sleep(.1)
    f = open('pidplot.dat','w')

    sp = 0
    fb = 0
    outv = 0

    print "Kp: %2.3f Ki: %2.3f Kd: %2.3f" %\
           (pid.Kp, pid.Ki, pid.Kd)

    for i in range(1,51):
        # summing node
        err = sp - fb

        # PID block
        outv = pid.GenOut(err)

        # control feedback
        if sp > 0:
            fb += (outv - (1/i))

        # start with sp = 0, simulate a step input at t(10)
        if i > 9:
            sp = 1

        print >> f,"%d  % 2.3f  % 2.3f  % 2.3f  % 2.3f" %\
                   (i, sp, fb, err, outv)
        time.sleep(.05)

    f.close()

gp = os.popen("gnuplot", "w")
print >> gp, "set yrange[-1:2]"

# generate 10 data sets for gnuplot to display. Data is written to a file,
# which gnuplot will read and display
for i in range(0, 10):
    # set Kp parameter for test run
    kpval = 0.9 + (i * .1)
    PIDPlot(kpval)
    # plot it
    print >> gp, "plot 'pidplot.dat' using 1:2 with lines,\
                       'pidplot.dat' using 1:3 with lines"
    # make sure it's all down the pipe
    gp.flush()

raw_input('Press return to exit...\n')
