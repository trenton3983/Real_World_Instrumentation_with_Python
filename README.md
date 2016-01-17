Example source code and associated notes for the book "Real-World
Instrumentation with Python" by J. M. Hughes, published by O'Reilly
Media, December 2010, ISBN 978-0-596-80956-0.

Using the Code Examples (from the book Preface)

This book is here to help you get your job done. In general, you may use
the code in this book in your programs and documentation. You do not need
to contact us for permission unless you’re reproducing a significant portion
of the code. For example, writing a program that uses several chunks of code
from this book does not require permission. Selling or distributing a CD-ROM
of examples from O’Reilly books does require permission. Answering a question
by citing this book and quoting example code does not require permission.
Incorporating a significant amount of example code from this book into your
product’s documentation does require permission. We appreciate, but do not
require, attribution. An attribution usually includes the title, author,
publisher, and ISBN. If you feel your use of code examples falls outside
fair use or the permission given above, feel free to contact O'Reilly at
permissions@oreilly.com.

Author's Comments on the Example Code

While I'm reasonably sure that I caught most of the errors that were lurking
in the example code (at least the big, ugly, obvious ones), I'm not perfect.
It's not intended as production code, so it hasn't been tested as rigorously
as it otherwise might have been.

You use the example code at your own risk. I cannot accept any responsibility
for any damages, real or consequential, that might arise from the use of the
software in this collection. It is up to you to determine its suitability and
correctness for a particular application or purpose.

If you have any questions, comments, suggestions, or complaints about this
example code, please post them to the book's web pages at O'Reilly. If you
do find a bug, I'd also like to know about it. If you find a better way to do
something, then it would be great if you could share it that so that others
might benefit from it.

Like the quote from the book above states, this code is intended to help you
get things done. Those who are already adept at Phython should bear in mind
that I didn't try to be clever, or even elegant in some cases. That was not
the point. The point of these examples is to show you, the reader, how things
can be made to work. These are starting points, not conclusions, and they
represent only one possible way of many. Creating the glorious conclusions
is up to you.

J.M. Hughes

================================================================================
Source Files
================================================================================
CH03
    argshow.py              Command-line arguments lister
    docstrings.py           docstrings usage example
    getInfo.py              Example user input and results print to console.
    getInfo2.py             User input with error trapping using try-except.
    globals.py              Accessing global variables example 1
    globals2.py             Accessing global variables example 2
    pgmrand.py              PGM image file generator
    subfuncs.py             Sub-functions example

CH04
    c_switch.c              The C switch construct with break statements.
    get_data.c              Dynamic allocation of structure memory space.
    sine_print.c            Sine generation using the printf function.
    sine_print2.c           Improved sine generation with macros.

CH05
    PDev.h                  Example device API header file.
    PDevAPI.c               Example device wrapper source.

CH09
    PID.py                  PID controller example.
    bangbang.py             Bang-bang controller example.
    propcontrol.py          Proportional controller example.

CH10
    PySims                  Top level package for PySims
        DevSim.pdf          A supplementary document for DevSim.

        TestDevSim1.py      Echos data written into the DevSim simulator to
                            the output.

        TestDevSim2.py      Demonstrates data file input using DevSim. Reads
                            data from an input file and passes the data to
                            the output.

        TestDevSim3.py      Demonstrates the use of DevSim with a user-defined
                            function string.

        TestDevSim4.py      The same as TestDevSim2.py except that noise, in
                            the form of random numbers, is applied to the data.

        TestDevSim5.py      Exercises all four channels. The first channel
                            simply echos input data to a specified output. The
                            second channel applies a user-defined functon to the
                            input data. The third channel scales data read from
                            a file. The fourth channel applies random data to
                            simulate noise.

        TestDevSim6.py      Demonstrate generaton of a sine wave output using
                            a cyclic data generator.

        TestDevSim7.py      Uses all four cyclic sources at the same time.

        PySims/ACSim        AC controller simulator
            SPCSim.py       The complete SPC simulator with serial I/O.

        PySims/DevSim       Device simulator package
            README.txt      Useful information
            DevSim.py       Main DevSim program module.
            DevSimDefs.py   Definitions (pseudo-constants) used in DevSim.

    PySims/SimLib           Simulator support package
        FileUtils.py        Contains the ASCIIDataRead and ASCIIDataWrite classes
        RetCodes.py         Defines global return value pseudo-constants
        TimeUtils.py        Contains a timestamp function and an execution
                            timer class

    gnuplot                 gnuplot demonstration code
        gptest.py           Basic example using open
        PID.py              PID example, used by PIDPlot and PIDPlot2
        PIDPlot.py          Uses popen to communicate with gnuplot
        PIDPlot2.py         Uses the gnuplot.py module

CH11
    AcqData.py              Data acquisition class example
    grabData.py             Error message lock-out example
    sampAvg.py              Data averaging example

CH12
    readascii.py            Columnar data file reader
    AutoConvert.py          Data type convertor
    FileUtils.py            ASCII data file read/write classes
    RetCodes.py             Used by FileUtils
    TimeUtils.py            Used by FileUtils
    ctypes_struct.py        ctypes structure example
    ctypes_struct2.py       ctypes structure example one-step init
    ctypes_struct_file.py   ctypes structure example with file I/O
    ctypes_struct_file2.py  ctypes structure example using an array
    pack_struct.py          struct example
    pack_struct_obj.py      struct object init example
    pack_struct_file.py     struct example with file I/O
    pgmtst.py               Simple PGM file generator
    PGMWrite.py             PGM file generator using struct library module
    datafile.dat            Test input for readascii

CH13
    SimpleANSI.py           Simple ANSI control functions library module
    bgansi.py               ANSI bar graph display example
    console1.py             Demonstrates console output using print method
    console2.py             Demonstrates OS detection
    console3.py             Demonstrates use of raw_input() method
    console4.py             Demonstrates use of thread for raw_input()
    console5.py             Example using mscvrt functions
    console6.py             Demonstrates use of SimpleANSI.py functions
    curses1.py              curses version of console6.py
    curses2.py              Demonstration of a sub-window using curses
    green24.bmp             Used in GUI examples
    green24on.bmp           Used in GUI examples
    red24.bmp               Used in GUI examples
    red24off.bmp            Used in GUI examples
    tkdemo1.py              Tkinter GUI example 1
    tkdemo2.py              Tkinter GUI example 2
    wxexample.py            wxPython GUI example

CH14
    read183dmm.py           Example code to read data from the tpi 183 DMM
    u3ledblink.py           LabJack U3 example


================================================================================
Notes and Errata
================================================================================
CH04: get_data.c

    Include for <stdlib.h> is missing in the book version. This version is
    correct.

CH04: Compiling the C code examples:

    When compiling sine_print and sine_print2, remember to tell the linker
    that it needs to include the math library, like this:

        gcc -o sine_print sine_print.c -lm

    and

        gcc -o sine_print2 sine_print2.c -lm

CH05: PDev.h and PDevAPI.c

    These two files are provided as examples, and possibily as templates for
    you own API "wrapper" for Python. You can use them as a starting points,
    but you will need to modify them for the actual device API you will be
    using in your own project.

    In other words, don't try to compile PDevAPI.c and expect it to do
    something useful. It won't.

CH10: Windows popen Problems

    If you have problems with popen under Windows you may want to look in
    the registery at:

        HKEY_LOCAL_MACHINE > SOFTWARE > Microsoft > Command Processor

    If the AutoRun entry exists, make sure it points to a valid executable
    file. The issue here is that if AutoRun is invalid, the command shell
    will generate an error message when it starts. Under Windows popen only
    creates a single unidirectional pipe, so there's no way for the message
    to come back when the shell is used to launch something like gnuplot.
    As a result it will fail with a cryptic error "Error 22" message. You
    can work around this by using popen3, but the better solution is to
    just fix the error in the registry.

    This happened to me when I unzipped the ansi130 package into a temporary
    directory and then ran its install. It modified the registry to point to
    the location where I unzipped it (I was assuming that it would copy itself
    to a directory in "Program Files" first, but it didn't--bad assumption
    on my part). When the temporary directory went away, ansi130 could no
    longer be found, cmd.exe would complain about it, and popen quit working.
    Ta da.

CH10: DevSim

    DevSim and the test suites, TestDevSim1.py, TestDevSim2.py and
    TestDevSim3.py got out of sync during the development of book and its
    code. The versions in this collection are correct. The code in the book,
    well, not so much. Sorry about that. In an attempt to make up for it I
    have included a seperate document describing DevSim in more detail, and
    there are now 7 test scripts to demonstrate DevSim's capabilities.

CH10: FileUtils.py

    In ASCIIDataRead.openInput() a None value for the path wasn't handled
    correctly. The code now looks like this:

        # if path is none, assume file is in local directory
        if path == None:
            path = './'

CH10: FileUtils.py

    As written in the book, the module FileUtils.py will only work under
    Windows when run as a stand-alone script. The reason is the use of the
    statement:

        fout.openOutput(".\\", "futest.dat")

    in the test section of the module. The version here has been fixed, so
    that it will work correctly with both Windows and Linux.

CH12: FileUtils.py, TimeUtils.py and RetCodes.py

    These are duplicates of the modules found in the CH10/PySims/SimLib
    directory. They should be identical.

CH13: console1.py

    The example output shown in the book doesn't match the code shown
    for console1.py. I've modified console1.py so it now generates what
    is shown in Chapter 13.

CH14: read183dmm.py

    You will most likely need to change the com port name in the code on
    line 16 in order to get this to work for you (assuming you happen to
    have a tpi183 DMM, of course).
