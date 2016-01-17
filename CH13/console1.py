#! /usr/bin/python
#-------------------------------------------------------------------------------
# console1.py
# Demonstrates console output using the built-in print method.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import time

ainstat   = ['ACTIVE','OFF','ACTIVE','OFF']
aindata   = [0.0, 0.0, 0.0, 0.0]
discstate = ['OFF','OFF','OFF','OFF','OFF','OFF','OFF','OFF']
discin    = [0,1,0,0,0,0,0,0]

print '\n' * 50
print ""
print "System Status"
print ""
print "Analog Input 0  : %10s  %f" % (ainstat[0], aindata[0])
print "Analog Input 1  : %10s  %f" % (ainstat[1], aindata[1])
print "Analog Input 2  : %10s  %f" % (ainstat[2], aindata[2])
print "Analog Input 3  : %10s  %f" % (ainstat[3], aindata[3])
print ""
print "Discrete Input 0: %3s  %d" % (discstate[0], discin[0])
print "Discrete Input 1: %3s  %d" % (discstate[1], discin[1])
print "Discrete Input 2: %3s  %d" % (discstate[2], discin[2])
print "Discrete Input 3: %3s  %d" % (discstate[3], discin[3])
print "Discrete Input 4: %3s  %d" % (discstate[4], discin[4])
print "Discrete Input 5: %3s  %d" % (discstate[5], discin[5])
print "Discrete Input 6: %3s  %d" % (discstate[6], discin[6])
print "Discrete Input 7: %3s  %d" % (discstate[7], discin[7])
print ""

time.sleep(2)
