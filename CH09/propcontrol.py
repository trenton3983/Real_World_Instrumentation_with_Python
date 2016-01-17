#-------------------------------------------------------------------------------
# propcontrol.py
# A simple implementation of a proportional controller.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

""" Simple proportional control.

    Obtains input data for the reference and the feedback, and
    generates a proportional control value using the equation:

    u = Kp(r - b) + P

    b is obtained from c * Kb, where c is the output of the
    controlled device or system (the plant), and Kb is a gain
    applied to scale it into the same range as the r (reference)
    input.

    The external function "Acquire" is a dummy. Replace it with
    a real call to acquire data from the system. The parameters
    to Acquire, rinput and cinput, would refer to a real data
    acquisition input.

    The gain parameters Kp and Kb should be set to something
    meaningful for a specific application. The P parameter is
    the bias to be applied to the output.
"""
# local global variables. Set these using the module.varname
# external access method.
Kp = 1.0
Kb = 1.0
P  = 0

# replace these as appropriate to refer to real inputs
rinput = 0
cinput = 1

def Acquire(port):
    return 1

def PControl():
    rval = Acquire(rinput)
    bval = Acquire(cinput) * Kb
    eval = rval - bval
    return (Kp * eval) + P
