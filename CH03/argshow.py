#-------------------------------------------------------------------------------
# argshow.py
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
import sys

print "%d items in argument list\n" % len(sys.argv)

i = 1
for arg in sys.argv:
    print "%d: %s" % (i, arg)
    i += 1
