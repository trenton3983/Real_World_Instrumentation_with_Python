#! /usr/bin/python
#-------------------------------------------------------------------------------
# readascii.py
#-------------------------------------------------------------------------------
# A simple utility to extract data from an ASCII file containing
# columnar data.
#
# Includes the ability to extract a specific column or range of
# columns. Can also skip over an arbitary number of non-columnar
# header lines. Output is printed to stdout.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import sys
import getopt

startcol = 0    # default start is column zero (first)
colspan  = -1   # default span is all columns
hdrskip  = 0    # default header line skip is zero (no header lines)
fname    = ''   # Empty string as default input file name

def usage():
    print "Usage: readascii [options] file_name"
    print "       Options:"
    print "         -c  Start column (default is zero)"
    print "         -s  Column span (default is all columns"
    print "         -h  # of header lines to skip (default is zero)"
    sys.exit(1)

# get command line arguments
if len(sys.argv) > 1:
    try:
        clopts, clargs = getopt.getopt(sys.argv[1:], ':c:s:h:')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    #endtry

    for opt, arg in clopts:
        if opt == "-c":
            startcol = int(arg)
        elif opt == "-s":
            colspan = int(arg)
        elif opt == "-h":
            hdrskip = int(arg)
        else:
            print "Unrecognized option"
            usage()
    if len(clargs) > 0:
        fname = clargs[0]
else:
    usage()
    sys.exit(2) # oops - forget to put this into the code in the book

# attempt to open input file
try:
    fin = open(fname, 'r')
except Exception, err:
    print "Error: %s" % str(err)
    sys.exit(2)

# see if header needs to be skipped
if hdrskip > 0:
    for i in range(0, hdrskip):
        fin.readline()      # just read and discard lines

# read, parse and output the designated fields from the input file
for line in fin:
    lineparts = line.split()
    if colspan == -1:
        colspan = len(lineparts)
    for i in range(startcol, (startcol + colspan)):
        print lineparts[i],
        print " ",
    print ""
