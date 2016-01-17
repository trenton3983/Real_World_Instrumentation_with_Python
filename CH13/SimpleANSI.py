#! /usr/bin/python
#-------------------------------------------------------------------------------
# SimpleANSI.py
# A minimal set of functions for ANSI screen control.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
""" Simple VT100/xterm ANSI terminal functions for Python.

    This module is based on C code originally written for use with
    VxWorks running on embedded controllers. It is used to control
    the display of an ANSI capable terminal or terminal emulator.
    It will work with Xterm on Unix and Linux systems, CygWin under
    Windows, and also with Tera Term under Windows.

    The ANSITerm class supports I/O via an ANSI-capable console,
    a serial connection, or a network socket.

    This is not a replacement for curses, and was never intended
    to be. It is a quick and simple way to put formatted data on
    a display, nothing more. It is useful for diagnostics, status
    displays, and simple command interfaces.

    The pseudo-macro CSI is the ANSI "Command Sequence Introducer".

    NOTE: This code has not been tested in all possible environmanets
    for all possible (or feasible) use cases. It may contain errors,
    omissions, or other unpleasant things.
"""

from sys import stdout
import time

ESC = "\x1b"
CSI = ESC+"["

CON = 0
SKT = 1
SIO = 2

class ANSITerm:
    """ Simple ANSI terminal control.

        Supports I/O using the console, a network socket, or a serial
        port.

        When communicating via a network socket, it is assumed that
        the physical port is a socket with send and receive methods,
        and it has already been opened elsewhere.

        When using a serial port, the port must already be open. In
        this case ioport must reference a valid pySerial object.

        The default I/O mode is to use the console, which must support
        ANSI control sequences (otherwise the ANSI sequences will just
        be printed, not interpreted). Also note that all user input
        via the console requires that the Enter key be pressed when
        input is complete. This is an artifact of Python's raw_input()
        function, since it has no native getch() type function.
    """
    def __init__(self, ioport=None, porttype=CON):
        """ Initialize the ANSIterm object.

            If porttype is anything other than CON then ioport must
            reference a valid I/O port object.

            If porttype is CON, then self.port is assigned the value of
            None.

            The defualt I/O method is the console.
        """
        self.pktsize = 1024     # just a default value for SKT mode
        self.port    = ioport   # SKT and SIO port object
        self.portOK  = False    # valid port indicator

        # map to the appropriate I/O handlers
        if porttype == SKT:
            if self.port:
                self.portOK   = True
                self.outfunc  = self.__sktOutput
                self.inpfunc  = self.__sktInput
        elif porttype == SIO:
            if self.port:
                self.portOK   = True
                self.outfunc  = self.__sioOutput
                self.inpfunc  = self.__sioInput
        else:
            self.port     = None
            self.portOK   = True
            self.outfunc  = self.__conOutput
            self.outflush = self.__conFlush
            self.inpfunc  = self.__conInput

    #-----------------------------------------------------------------
    # I/O handlers
    #-----------------------------------------------------------------
    # Although this could have been done without the use of a set of
    # one-line methods, this approach leaves the door open to easily
    # expand this scheme in the future. The inclusion of some type of
    # error handling, for example, or perhaps the abilit to capture
    # and log data I/O.
    #
    # Note that the socket and serial I/O methods assume that a
    # standard Python socket object or a pySerial port object will
    # be used. Another type of I/O object may require different
    # methods for reading and writing.
    #-----------------------------------------------------------------
    def __sktOutput(self, outstr):
        self.port.send(outstr)

    def __sioOutput(self, outstr):
        self.port.write(outstr)

    def __conOutput(self, outstr):
        stdout.write(outstr)

    def __conFlush(self):
        stdout.flush()

    def __sktInput(self):
        return self.port.recv(self.pktsize)

    def __sioInput(self):
        return self.port.readline()

    def __conInput(self):
        return raw_input()     # no prompt is specified for raw_input

    #-----------------------------------------------------------------
    # Cursor Positioning
    #-----------------------------------------------------------------
    def moveHome(self):
        """ Move cursor to upper left corner.
        """
        if self.portOK:
            self.outfunc("%sH" % CSI)
    
    def moveNextline(self):
        """ Move to start of next line.
        """
        if self.portOK:
            self.outfunc("%sE" % ESC)

    def movePos(self, row, col):
        """ Move cursor to screen location row, col.
        """
        if self.portOK:
            self.outfunc("%s%d;%dH" % (CSI, row, col))
    
    def moveUp(self, count):
        """ Move cursor up count rows.
        """
        if self.portOK:
            self.outfunc("%s%dA" % (CSI, count))
    
    def moveDown(self, count):
        """ Move cursor down count rows.
        """
        if self.portOK:
            self.outfunc("%s%dB" % (CSI, count))
    
    def moveFoward(self, count):
        """ Move cursor right count columns.
        """
        if self.portOK:
            self.outfunc("%s%dC" % (CSI, count))
    
    def moveBack(self, count):
        """ Move cursor left count columns.
        """
        if self.portOK:
            self.outfunc("%s%dD" % (CSI, count))

    def indexUp(self):
        """ Move/scroll up one line.
        """
        if self.portOK:
            self.outfunc("%D" % ESC)
    
    def indexDown(self):
        """Move/scroll down one line.
        """
        if self.portOK:
            self.outfunc("%M" % ESC)

    def savePos(self):
        """ Save current cursor position.
        """
        if self.portOK:
            self.outfunc("%ss" % CSI);
    
    def restorePos(self):
        """ Restore cursor to last saved position.
        """
        if self.portOK:
            self.outfunc("%su" % CSI);

    #-----------------------------------------------------------------
    # Display Control
    #-----------------------------------------------------------------
    def clrScreen(self):
        if self.portOK:
            self.outfunc("%s2J" % CSI);
    
    def clrEOL(self, row=None, col=None):
        """ Clear line from given or current position.

            If row and col are None, then the current position is used.
        """
        if self.portOK:
            if row and col:
                self.movePos(row,col);
            self.outfunc("%s0K" % CSI)
    
    def clrLine(self, row=None):
        """ Clear enture line (row) in display.

            If row is None, then the current position is used.
        """
        if self.portOK:
            if row:
                self.movePos(row, 1)
            self.outfunc("%s2K" % CSI)
    
    def resetDev(self):
        """ Reset terminal to initial state.
        """
        if self.portOK:
            self.outfunc("%sc" % ESC)

    #---------------------------------------------------------------------------
    # Input
    #---------------------------------------------------------------------------
    def readInput(self, reset=False):
        """ Get user input and echo to the display.
    
            If a prompt is required it must be generated at the appropriate
            location before this method is called.

            if reset is True, then when the input handler returns the cursor
            will be repositioned to the starting location prior to user input.
            This capability is provided mainly to compensate for the use of
            Python's raw_input() funcion when interacting with a console, as
            the user will need to press the Enter key to complete an input.
        """
        instr = ""
        if self.portOK:
            if reset: self.savePos()
            instr = self.inpfunc()
            if reset: self.restorePos()
            return instr

    #---------------------------------------------------------------------------
    # Output
    #---------------------------------------------------------------------------
    def writeOutput(self, outstr):
        """ Writes an arbitary string at the current cursor position.
        """
        if self.portOK:
            self.outfunc(outstr)
            self.outflush()


# self-test
if __name__ == "__main__":
    term = ANSITerm(None, 0)

    term.clrScreen()

    # number the rows on the display from 1 to 24
    for i in range(1,21):
        term.movePos(i,0)
        term.writeOutput("%0d" % i)

    # write some text to the display
    term.movePos(14,4)
    term.writeOutput("* This is line 14, column 4")
    time.sleep(1)
    term.movePos(15,4)
    term.writeOutput("* This is line 15, column 4")
    time.sleep(1)

    # create a diagonal series of characters
    for i in range(2,12):
        term.movePos(i,i+4)
        term.writeOutput("X")
        time.sleep(0.1)

    for i in range(2,12):
        term.movePos(i,i+4)
        term.writeOutput(" ")
        time.sleep(0.1)

    for i in range(2,12):
        term.movePos(i,i+4)
        term.writeOutput("X")
        time.sleep(0.1)

    # do some blinking the hard way
    for i in range(0,10):
        term.movePos(17,10)
        term.writeOutput("blick blink")
        time.sleep(0.5)
        term.clrEOL(17,10)
        time.sleep(0.5)

    term.movePos(18,4)
    term.writeOutput("Did it blink? (y/n): ")
    instr = term.readInput()
    term.movePos(19,4)
    term.writeOutput("You answered %s, thank you for playing." % instr)

    term.movePos(22,1)
    # and that's it
