README.txt (for SPCSim)
================================================================================
This file is part of the source code provided with the book "Real-World
Instrumentation Using Python" by J. M. Hughes, published by O'Reilly Media,
December 2010, ISBN 978-0-596-80956-0.
================================================================================

You can start SPCSim.py by typing the following at a command prompt:

    python SPCSim.py <command line parameters>

or, if you're running it on Linux and the file permissions are set correctly,
you should be able to just type SPCSim.py.

In order to run SPCSim in serial I/O mode you'll need to either have a second
PC available, or you'll need to install com0com for Windows, or tty0tty for
Linux. At the other end of the serial I/O channel you can use a terminal
emulator to communicate with SPCSim, or you could create a nice GUI to emulate
the front panel of a real device.

The configuration parameters file (a so-called INI file) named spc.ini is
provided. You can edit it to suit yourself, or just not use it all. If you do
elect to use it it needs to reside in the same directory with SPCSim.py.

Note that SPCSim is completely command-driven. In other words, when it's
waiting for input via the command channel (be it serial or console), it is
doing nothing else--the main loop is blocked. It would be a straightforward
task to change the command input to a threaded mode of operation, and let the
main loop run continuously with a time delay at the end of each cycle. This,
in turn, would open up the possibility of continuously checking the ECB states
and updating the internal state data accordingly.

There are a couple of special commands that you should be aware of: QUIT and
DMP. The QUIT command, as the name implies, shuts down SPCSim. The DMP command
is useful if you want to see how a command has altered the contents of the
internal state variables in the simulator. Both commands work in either then
control or serial I/O modes.

Lastly, here are the command line switches for SPCSim:

-i n        Interface type: n = 0: console, n = 1: serial I/O

-p name     Serial I/O port name (i.e. COM4 or /dev/tty2)

-m n        Monitor mode: n = 0: off, n = 1: on

The monitor mode will cause SPCSim to emit messages indicating internal
activities to whatever is currently defined as stdout. It provides a peek
into the internals of the simulator. In console mode this can become a
little annoying, but in serial mode it is not obtrusive.

Simulating an ECB fault

To simulate an ECB fault first set the limit for a channel to 0. When the
channel is next powered on, either via an ALL, SEQ, or POW command, the ECB
will be marked as failed.

To clear an ECB fault set the current limit for the faulted channel to some
non-zero value, and then issue an RST command for the channel to clear the
fault.

The DMP command may be used to observe the changes in the channel state data.
