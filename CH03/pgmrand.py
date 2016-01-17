#-------------------------------------------------------------------------------
# pgmrand.py
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
""" Generates an 8bpp "image" of random pixel values.

The sequence of operations used to create the PGM output file is as follows:
    1. Create the PGM header, consisting of:
        ID string (P5)
        Image width
        Image height
        Image data size (in bits/pixel)
    2. Generate height x width bytes of random values
    3. Write the header and data to an output file
"""
import random as rnd   # use import alias for convenience

rnd.seed()        # seed the random number generator

# image parameters are hard-coded in this example
width  = 256
height = 256
pxsize = 255      # specify an 8 bpp image

# create the PGM header
hdrstr = "P5\n%d\n%d\n%d\n" % (width, height, pxsize)

# create a list of random values from 0 to 255
pixels = []
for i in range(0,width):
    for j in range(0,height):
        # generate random values of powers of 2
        pixval = 2**rnd.randint(0,8)
        # some values will be 256, so fix them
        if pixval > pxsize:
            pixval = pxsize
        pixels.append(pixval)

# convert array to character values
outpix = "".join(map(chr,pixels))

# append the "image" to the header
outstr = hdrstr + outpix

# and write it out to the disk
FILE = open("pgmtest.pgm","w")
FILE.write(outstr)
FILE.close()
