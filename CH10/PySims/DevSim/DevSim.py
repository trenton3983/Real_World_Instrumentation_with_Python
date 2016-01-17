#-------------------------------------------------------------------------------
# DevSim.py
#-------------------------------------------------------------------------------
# Generic device I/O simulator
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
""" DevSim - Simulated Device I/O
"""
import  time
import  random
import  threading
import  math

import  SimLib.RetCodes as RC
import  SimLib.FileUtils
import  DevSimDefs as DS
from    SimLib.FileUtils import ASCIIDataRead   # class import

import  ConfigParser
import  SimLib.AutoConvert as cvt

#-------------------------------------------------------------------------------
class DevSim():
    """ Implements a simulated I/O device.

        This class implements a simulated direct-access I/O device
        (such as a DAQ type card) with four input channels and four
        output channels. Inputs and outputs may include optional user-
        defined processing to generate simulated stimulus-response
        behaviors. The outputs may also be driven by external data
        input files.
    """
    def __init__(self):
        """ Initialize internal simulator operational parameterss and buffers
        """
        #-----------------------------------------------------------------------
        # Internal data initialization
        #-----------------------------------------------------------------------

        # Primary simulator cyclic time (main loop)

        self.simtime    = 0.25                      #: 250 ms default start rate

        # There are 4 input source MUXs: INCHAN1..INCHAN4
        # Each with two possible inputs: EXT_IN or CYCLIC

        self.in_src     = [0, 0, 0, 0]              #: Input source MUX list

        # Cyclic data source control variables. A cyclic source is defined by
        # cyclictype, and may be one of CYCNONE, CYCSINE, CYCPULSE, CYCRAMP,
        # or CYCSAW.

        self.cyclictype = [0, 0, 0, 0]              #: cyclic type codes
        self.cycliclvl  = [0.0, 0.0, 0.0, 0.0]      #: max data value
        self.cyclicrate = [0.2, 0.2, 0.2, 0.2]      #: cyclic rates
        self.cyclicdata = [0.0, 0.0, 0.0, 0.0]      #: output from cyclic thread
        self.cycoffset  = [0.0, 0.0, 0.0, 0.0]      #: offset for sine cyclic data
        self.sineval    = 0
        self.sineinc    = 0
        self.pulsecnt   = 0
        self.pulse_out  = 0
        self.pulseflip  = False
        self.ramp_out   = 0
        self.ramp_cnt   = 0
        self.saw_out    = 0
        self.saw_cnt    = 0
        self.saw_dir    = 1

        # External input data buffers hold the data pushed into the simulator
        # by a call to the sendData() method from an external source. They
        # retain the last value until a new value is received.

        self.inbuffer   = [0.0, 0.0, 0.0, 0.0]      #: ext input data buffers

        # databuffer contains either the external data or cyclic data
        # (whichever was selected via input MUX (the value in in_src) for
        # the four input channels after it has been processed by the user-
        # defined function for that channel, if any.

        self.databuffer = [0.0, 0.0, 0.0, 0.0]      #: post-func data buffers

        # Four optional user-supplied functions, one per input channel
        # (implemented post-input MUX): INCHAN1..INCHAN4

        self.userexp    = ["", "", "", ""]          #: User-defined functions
        self.x0         = 0                         #: user-accessible data var
        self.x1         = 0                         #: user-accessible data var

        # There are four possible file inputs. They are referenced as
        # SRCFILE1..SRCFILE4, but are normalized to 0..3 when used to access
        # the contents of these list objects.

        self.filename   = ["", "", "", ""]          #: data source file names
        self.fileref    = [None, None, None, None]  #: file object refs
        self.filetrig   = [0, 0, 0, 0]              #: file read event flags
        self.filebuffer = [0.0, 0.0, 0.0, 0.0]      #: file input data buffers

        # When a file read is complete and data is available this flag is set
        # to True. It is reset to False when the data is transferred from the
        # filebuffer object to the output buffer via the output MUX. A file
        # read will not occur unless the flag is False.

        self.in_file    = [0, 0, 0, 0]              #: file data available flags

        # Each input channel mau be assigned one of three trigger modes:
        # NO_TRIG, EXT_TRIG, and INT_TRIG. Only the cyclic data sources and
        # file input handlers respond to trigger events. A trigger event is
        # not a real event, per se, but rather a flag (trigevt) that is set
        # True to indicate a trigger action.

        self.trigger    = [0, 0, 0, 0]              #: trigger modes
        self.trigevt    = [0, 0, 0, 0]              #: trigger event flags

        # There are 4 output source MUXs, each with eight possible inputs:
        # INCHAN1..INCHAN4 and SRCFILE1..SRCFILE4

        self.out_src    = [0, 0, 0, 0]              #: Output source MUX list

        # Output buffers and data scaling parameters. The list outbuffer
        # contains four buffer variables for data available to be read by
        # external code via the readData() method. Data is preserved after
        # a read, and is only changed when an input source generates new
        # data to propogate through the simulator.
        #
        # Setting outscale to 1.0 and randscale to 0.0 results in no changes
        # to the output data (setting randscale to 0.0 effectively disables
        # any random data value scaling).

        self.outscale   = [1.0, 1.0, 1.0, 1.0]      #: output scaling factor
        self.randscale  = [0.0, 0.0, 0.0, 0.0]      #: random scaling factor
        self.outbuffer  = [0.0, 0.0, 0.0, 0.0]      #: output buffer buffers
        self.outavail   = [0, 0, 0, 0]              #; output data available flags

        # The object attributes startSim and stopSim control the main loop.
        # The loop will pend until startSim is true, and will run until the
        # variable stopSim is True. Once startSim is set True its value is
        # no longer relevant. Here's the truth table:
        #
        # startSim    stopSim     State
        # --------    --------    ------------------
        #  False       False      Pending
        #  True        False      Running
        #  N/A         True       Stop and Terminate
        #  N/A         True       Stop and Terminate

        self.startSim   = False                     #: simulator thread start flag
        self.stopSim    = False                     #: simulator thread stop flag

        # The debug flags controls the generation of messages to stdout while
        # the simulator is running. It is set using a parameter data file (an
        # INI file).

        self.debug      = False                     #: debug message output control

        #-----------------------------------------------------------------------
        # Simulator configuration load and startup
        #-----------------------------------------------------------------------

        # Get startup configuration parameters
        self.LoadCFG()

        # Start simulator
        self.__run()


    #---------------------------------------------------------------------------
    # Parameter accessor methods
    #---------------------------------------------------------------------------
    # These methods simply set or return parameter values from the
    # object attributes (variable) defined in the __init__() method.
    #---------------------------------------------------------------------------

    def setSimTime(self, rate):
        """ Set the overall cycle time of the simulation.

            Sets the main loop time of the simulator. This is, in
            effect, the amount of time the main loop will suspend
            between each loop iteration. The time is specified in
            fractional seconds.

            @param rate:        simulator cycle time
            @return:            Nothing
        """
        self.simtime = rate


    def getSimTime(self):
        """ Returns current simulator cycle time.

            @return:            simulator cycle time
        """
        return self.simtime


    def setInputSrc(self, inchan, source):
        """ Select the data source for an input channel.

            inchan may be any valid input channel number from 0 to 3.
            The source parameter may be one of EXT_IN (default) or
            CYCLIC. The input source may be changed on-the-fly at
            any time.

            @param inchan:      Channel number [0..3]
            @param source:      Input channel type code

            @return:            NO_ERR or BAD_PARAM
        """
        # inchan selects input multiplixer
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            # source selects MUX input
            if (source == DS.EXT_IN) or (source == DS.CYCLIC):
                self.in_src[inchan] = source
                return RC.NO_ERR
        # else
        return RC.BAD_PARAM


    def getInputSrc(self, inchan):
        """ Returns current input source for specified channel.

            inchan may be any valid input channel number from 0 to 3.

            Returns 2-tuple with either NO_ERR and the input source,
            or BAD_PARAM and None.

            @param inchan:      Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        # inchan selects input multiplixer
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            # return MUX setting
            return RC.NO_ERR, self.in_src[inchan]
        # else
        return RC.BAD_PARAM, None


    def setOutputDest(self, outchan, source):
        """ Selects the data source for an output channel.

            outchan may be any valid output channel MUX number between 0
            and 3. The source parameter may be one of INCHAN1,
            INCHAN2, INCHAN3, INCHAN4, SRCFILE1, SRCFILE2, SRCFILE3
            or SRCFILE4 (i.e. 0 through 7).

            @param outchan:     Channel number [0..3]
            @param source:      See description above [0..7]

            @return:            NO_ERR or BAD_PARAM
        """
        # outchan selects the output MUX
        if (outchan >= DS.OUTCHAN1) and (outchan <= DS.OUTCHAN4):
            # source selects the MUX input
            if (source >= DS.INCHAN1) and (source <= DS.SRCFILE4):
                self.out_src[outchan] = source
                return RC.NO_ERR
        # else
        return RC.BAD_PARAM


    def getOutputDest(self, outchan):
        """ Returns the current output channel data source selection.

            Returns 2-tuple with either NO_ERR and the output ID,
            or BAD_PARAM and None.

            @param outchan:     Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        # outchan selects the output MUX
        if (outchan >= DS.OUTCHAN1) and (outchan <= DS.OUTCHAN4):
            # return MUX setting
            return RC.NO_ERR, self.out_src[outchan]
        # else
        return RC.BAD_PARAM, None


    def setDataScale(self, outchan, scale):
        """ Sets output channel input data scaling factor.

            Each output channel may have an optional multiplicative
            scaling factor applied. The scaling factor is a float
            value, it may be less than 1.0, and it may be negative.

            Data scaling is applied before the data is summed with
            the random "noise" data just prior to being written into
            the output buffer.

            @param outchan:     Channel number [0..3]
            @param scale:       Scaling value for specified channel

            @return:            NO_ERR or BAD_PARAM
        """
        rc = RC.BAD_PARAM

        if (outchan >= DS.OUTCHAN1) and (outchan <= DS.OUTCHAN4):
            self.outscale[outchan] = scale
            rc = RC.NO_ERR

        return rc


    def getDataScale(self, outchan):
        """ Returns current output data scaling for specified channel.

            Returns 2-tuple with either NO_ERR and the current data
            scaling, or BAD_PARAM and None.

            @param outchan:     Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (outchan >= DS.OUTCHAN1) and (outchan <= DS.OUTCHAN4):
            return RC.NO_ERR, self.outscale[outchan]
        # else
        return RC.BAD_PARAM, None


    def setRandScale(self, outchan, scale):
        """ Sets output channel random data scaling factor.

            Each output channel may have an optional multiplicative
            scaling factor applied to injected random data. If the
            scaling is set to zero, then no random values are summed
            into the data.

            @param outchan:     Channel number [0..3]
            @param scale:       Scaling value for random data

            @return:            NO_ERR or BAD_PARAM
        """
        rc = RC.BAD_PARAM

        if (outchan >= DS.OUTCHAN1) and (outchan <= DS.OUTCHAN4):
            self.randscale[outchan] = scale
            rc = RC.NO_ERR

        return rc


    def getRandScale(self, outchan):
        """ Returns the random data scaling for a specified channel.

            Returns 2-tuple with either NO_ERR and the current random
            data scaling, or BAD_PARAM and None.

            @param outchan:     Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (outchan >= DS.OUTCHAN1) and (outchan <= DS.OUTCHAN4):
            return RC.NO_ERR, self.randscale[outchan]
        # else
        return RC.BAD_PARAM, None


    def setTriggerMode(self, inchan, mode):
        """ Sets the trigger mode for a particular input channel.

            The trigger mode may be one of DS.NO_TRIG (0), DS.EXT_TRIG
            (1), or DS.INT_TRIG (2).

            In DS.NO_TRIG mode all cyclic sources run continuously at
            the clock rate set by the setCyclicClock() method, and
            data source file reads do not occur until an output channel
            is accessed.

            In DS.EXT_TRIG mode cyclic sources perfom a single
            operation and file sources are read once for each trigger
            occurrence.

            In DS.INT_TRIG mode cyclic sources perfom a single cycle
            and data source files are read once each time an output
            channel is accessed.

            @param inchan:      Channel number [0..3]
            @param mode:        Input channel trigger mode

            @return:            NO_ERR or BAD_PARAM
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            if mode in (DS.NO_TRIG, DS.EXT_TRIG, DS.INT_TRIG):
                self.trigger[inchan] = mode
                return RC.NO_ERR
        # else
        return RC.BAD_PARAM


    def getTrigMode(self, inchan):
        """ Returns current trigger mode for specified channel.

            Returns 2-tuple with either NO_ERR and the current
            trigger mode for the specified channel, or BAD_PARAM
            and None.

            @param inchan:      Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            return RC.NO_ERR, self.trigger[inchan]
        # else
        return RC.BAD_PARAM, None


    def setFunction(self, inchan, funcstr=""):
        """ Applies a function to the input channel data.

            A user-supplied function expression is applied to the
            input channel data using predefined variables:

            x0 = input data
            x1 = previous (1/z) data

            The function is a string. It may reference the x0 and x1
            variables but may not contain an equals sign. The result
            is used as the data input to the output channels. Passing
            None or an empty string disables the application of a
            function to the data.

            @param inchan:      Channel number [0..3]
            @param funcstr      Function string (see description)

            @return:            NO_ERR or BAD_PARAM
        """
        rc = RC.BAD_PARAM

        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            if (type(funcstr) == str) and (len(funcstr) > 0):
                self.userexp[inchan] = funcstr
                rc = RC.NO_ERR

        return rc


    def getFunction(self, inchan):
        """ Returns current function string for specified channel.

            Returns 2-tuple with either NO_ERR and the current
            functin string for the specified channel, or BAD_PARAM
            and None.

            @param inchan:      Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            return RC.NO_ERR, self.userexp[inchan]
        # else
        return RC.BAD_PARAM, None


    def setCyclicRate(self, inchan, rate):
        """ Sets the iteration rate of a cyclic data source.

            The parameter rate defines the internal rate of a cyclic
            data source in fractional seconds. Note that this is the
            period of the output, not the frequency. Also note that
            the rate of a cyclic data source is independant of the
            cyclic rate of the simulator's main loop.

            @param inchan:      Channel number [0..3]
            @param rate:        Cyclic rate

            @return:            NO_ERR or BAD_PARAM
        """
        rc = RC.BAD_PARAM

        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            self.cyclicrate[inchan] = rate
            rc = RC.NO_ERR
        return rc


    def getCyclicRate(self, inchan):
        """ Returns current cyclic source rate for specified channel.

            Returns a 2-tuple with either NO_ERR and the current
            cyclic rate of the specified channel, or BAD_PARAM
            and None.

            @param inchan:      Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            return RC.NO_ERR, self.cyclicrate[inchan]
        # else
        return RC.BAD_PARAM, None


    def setCyclicType(self, inchan, cyctype):
        """ Defines the output waveshape of a cyclic data source.

            The available wave shapes are sine, pulse, ramp, and
            sawtooth. A cyclic source may also be set to generate a
            constant output value, and the value may be changed at
            any time while the simulator is active. This, in effect,
            emulates a variable voltage source.

            CYCNONE     Constant output level
            CYCSINE     Sine wave
            CYCPULSE    50% duty-cycle pulse (i.e., a square wave)
            CYCRAMP     Ramp wave shape with leading slope
            CYCSAW      Sawtooth wave with symmetrical rise/fall

            @param inchan:      Channel number [0..3]
            @param cyctype:     Cyclic waveshape

            @return:            NO_ERR or BAD_PARAM
        """
        rc = RC.BAD_PARAM

        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            if cyctype in (DS.CYCNONE, DS.CYCSINE, DS.CYCPULSE, DS.CYCRAMP, DS.CYCSAW):
                self.cyclictype[inchan] = cyctype
                rc = RC.NO_ERR
        return rc


    def getCyclicType(self, inchan):
        """ Returns current cyclic type for specified channel.

            Returns 2-tuple with either NO_ERR and the current
            cyclic waveshape of the specified channel, or BAD_PARAM
            and None.

            @param inchan:      Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            return RC.NO_ERR, self.cyclictype[inchan]
        # else
        return RC.BAD_PARAM, None


    def setCyclicLevel(self, inchan, level):
        """ Sets the output level for a cyclic source in CYCNONE mode.
            The output level is the peak value of the cyclic waveform,
            relative to zero.

            @param inchan:      Channel number [0..3]
            @param cyctype:     Cyclic output level

            @return:            NO_ERR or BAD_PARAM
        """
        rc = RC.BAD_PARAM

        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            self.cycliclvl[inchan] = level
            rc = RC.NO_ERR
        return rc


    def getCyclicLevel(self, inchan):
        """ Returns current cyclic level for specified channel.

            Returns 2-tuple with either NO_ERR and the current
            cyclic level of the specified channel, or BAD_PARAM
            and None.

            @param inchan:      Channel number [0..3]

            @return:            2-tuple, rc and value (see desc.)
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            return RC.NO_ERR, self.cycliclvl[inchan]
        # else
        return RC.BAD_PARAM, None


    def setCyclicOffset(self, offset):
        """ Sets cyclic sine source offset value.

            The offset is applied to the output of a sine cyclic data
            source, which has the effect of introducing either a positve
            or negative offset (or bias, if you prefer). It is not a form
            of scaling, and applies only to the sine cyclic data source.

            @param offset:      Cyclic offset level
        """
        self.cycoffset = offset


    def getCyclicOffset(self):
        """ Returns the current cyclic since source offset value.

            @return:            Cyclic offset value
        """
        return self.cycoffset


    def setDataFile(self, infile, path, filename, recycle=True):
        """ Opens a data file for input as a data source.

            If path is not specified the default is assumed to be the
            current working directory.

            The input file must be in one of the four formats
            supported by the module FileUtils and the ASCIIDataRead
            class.

            If the parameter 'recycle' is True, then the file will be
            reset to the start and re-read when an EOF is encountered.
            The default behavior is to recycle the data file.

            If a data source file is already opened for a given input
            channel and this method is called, then the currently open
            file will be closed and the new file will be opened.

            Returns OPEN_ERR if file open failed or BAD_PARAM if infile
            is invalid, and NO_ERR otherwise.

            @param infile:      File index (SRCFILE1..SRCFILE4)
            @param path:        File path (or None)
            @param filename:    File name
            @param recycle:     Controls recycling (see desc)

            @return:            NO_ERR, OPEN_ERR, or BAD_PARAM
        """
        if (infile >= DS.SRCFILE1) and (infile <= DS.SRCFILE4):

            # translate to range [0..4]
            fileidx = infile - 4

            fsrc = ASCIIDataRead()

            rc = fsrc.openInput(path, filename)

            if rc != RC.NO_ERR:
                return RC.OPEN_ERR
            else:
                self.filename[fileidx] = filename
                self.fileref[fileidx] = fsrc
                if self.debug:
                    print "Data file set: ", self.filename[fileidx]
                return RC.NO_ERR

        return RC.BAD_PARAM


    #---------------------------------------------------------------------------
    # Input/Output Methods
    #---------------------------------------------------------------------------

    def genTrigger(self, inchan):
        """ Generates a trigger event.

            Depending on the trigger mode, a trigger event will result
            in one iteration of a cyclic data source, or one record
            read from a data input file.

            @param inchan:      Input channel for event

            @return:            NO_ERR or BAD_PARAM
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            # do not set a trigger flag unless it's already False.
            if self.trigevt[inchan] == False:
                self.trigevt[inchan] = True
            return RC.NO_ERR
        # else
        return RC.BAD_PARAM


    def sendData(self, inchan, dataval):
        """ Write data into the simulator.

            Writes caller-supplied data into the specified channel.
            The data in the buffer will be read out on each cycle of
            the simulator.

            @param inchan:      Input channel for incoming data
            @param dataval:     Data to write into input buffer

            @return:            NO_ERR or BAD_PARAM
        """
        if (inchan >= DS.INCHAN1) and (inchan <= DS.INCHAN4):
            self.inbuffer[inchan] = dataval
            if self.debug:
                print "inchan: %d  data: " % inchan, self.inbuffer[inchan]
            return RC.NO_ERR
        # else
        return RC.BAD_PARAM


    def readData(self, outchan, block=True, timeout=10.0):
        """ Read data from the simulator.

            The data available for the specified channel is returned
            to the caller. If blocking is enabled then this method
            will block the return to the caller until the data becomes
            available or the timeout period has elapsed.

            Note that the time also applies to the file data read flag
            detection. 10 seconds is just an overly cautious default value.

            Returns a 2-tuple consisting of the return code and the
            data value from the output channel. If the return code is
            not NO_ERR the data value will be zero.

            This method has a bit of whirly-twirly going on. Read the
            comments, and also refer to the __fileData(), __fileRead, and
            __simLoop() methods to see how the various flags interact with
            one another to synchronize data input, particularly file data
            input.

            @param outchan
        """
        rc = RC.NO_ERR
        retdata = 0.0

        # File input that is not externally triggered needs to be invoked
        # here (this is the dashed line in the DevSim diagram in the book).
        # The in_file flag is used to signal that data has been read from
        # an input file, but it does not mean that the data has been moved
        # through to the output buffer. The outavail flag is used for that
        # purpose.
        if self.fileref[outchan] != None:
            if self.trigger[outchan] != DS.EXT_TRIG:
                # trigger a file input
                self.filetrig[outchan] = True
            # wait for data to become available
            stime = time.time()
            while (self.in_file[outchan] != True):
                time.sleep(0.1)
                if time.time() - stime > timeout:
                    rc = RC.TIMEOUT
                    if self.debug:
                        print "File trigger response timeout"
                    break
            if self.in_file[outchan]:
                self.in_file[outchan] = False

        # Check to make sure we're still good to go (i.e. we didn't get a
        # timeout waiting for the file read flag).
        if rc == RC.NO_ERR:
            # In this section the code waits for the outavail flag to be
            # set, indicating that the data has been transferred from
            # either the input data buffer or from the file data buffer
            # into the output buffer, with scaling and noise applied as
            # appropriate.
            #
            # If blocking mode is enabled then it will wait for the data
            # available flag (outavail[]) to be set to True.
            if block:
                stime = time.time()
                while self.outavail[outchan] == False:
                    time.sleep(0.1)
                    if time.time() - stime > timeout:
                        rc = RC.TIMEOUT
                        if self.debug:
                            print "Output data available timeout"
                        break
    
                # reset the data available flag if no timeout occurred
                if rc == RC.NO_ERR:
                    self.outavail[outchan] = False

        if rc == RC.NO_ERR:
            retdata = self.outbuffer[outchan]

        return rc, retdata


    #---------------------------------------------------------------------------
    # Configuration parameters handler
    #---------------------------------------------------------------------------
    def getOpt(self, cfgobj, section, option):
        """ Utility method to fetch data from a parameter file.

            Instead of falling down and emitting a traceback this method will
            just return ERR if a section or parameter cannot be found in a
            parameter file.
        """
        rc = RC.CFG_ERROR
        optstr = ""
        if cfgobj.has_section(section):
            if cfgobj.has_option(section, option):
                optstr = cfgobj.get(section, option)
                rc = RC.NO_ERR
        return rc, optstr


    def LoadCFG(self):
        """ Read parameter entries in the spi.ini file if it exists.

            With the exception of the serial port parameters, this method
            takes advantage of the command input functions that already exist
            to handle the data type conversions and set the appropriate
            internal parameters.

            There is no type or range checking done here. For the operational
            parameters that's handled in the command processor methods. If
            bogus values are provided for the serial port, then they will be
            caught when the port is opened.

            The command input functions expect to get a list containing at
            least two elements: the command and a parameter. In the code of
            the SOR function it expects a list with up to nine elements. So,
            a dummpy element ('') is placed at the start of a list containing
            the data from the INI file, and then passed to the appropriate
            function.
        """
        cfg = ConfigParser.ConfigParser()
        cfg.read('devsim.ini')

        # see if a config file was read, don't bother looking for data if it
        # isn't available
        try:
            seclen = len(cfg.items('DEVSIM'))
        except Exception, e:
            print "Config error: %s" % str(e)
            return None

        if seclen == 0:
            print "Configuration file data not loaded"
        else:
            optret = self.getOpt(cfg, 'DEVSIM', 'debug')
            if optret[0] == RC.NO_ERR:
                # AutoConvert returns a 2-tuple (value, type) but we just want
                # the data value.
                self.debug = cvt.AutoConvert(optret[1])[0]


    #---------------------------------------------------------------------------
    # Internal Processing Methods
    #---------------------------------------------------------------------------

    def __getCycData(self, inchan):
        """ Fetches the data generated by a cyclic thread object.

            The most recent data generated by a cyclic thread object
            is read and returned to the caller.
        """
        return self.cyclicdata[inchan]


    def __doUserFunc(self, inchan, indata):
        """ Evaluates a user function string.
        """
        result = indata

        if len(self.userexp[inchan]) > 0:
            self.x1 = self.x0
            self.x0 = indata

            x0 = self.x0
            x1 = self.x1

            try:
                result =  eval(self.userexp[inchan])
            except Exception, e:
                print str(e)

        return result


    def __getRandom(self):
        """ Returns a random number.
        """
        return random.random()


    def __scaleData(self, inval, scaleval):
        """ Applies scaling to a data value and returns it.
        """
        return inval * scaleval


    #-----------------------------------------------------------------
    # Cyclic data source methods
    #-----------------------------------------------------------------
    def __genSine(self, cycliclvl):
        """ Cyclic sine wave data generator.
        """
        self.sineval = (cycliclvl * math.sin(self.sineinc))
        self.sineinc += 0.1
        if self.sineinc == 359:
            self.sineinc = 0
        return (self.sineval + self.cycoffset)


    def __genPulse(self, cycliclvl):
        """ Cyclic pulse data generator.
        """
        if self.pulsecnt >= 20:
            if self.pulseflip:
                self.pulse_out = 0.0
                self.pulseflip = False
                self.pulsecnt = 0
            else:
                self.pulse_out = cycliclvl
                self.pulseflip = True
                self.pulsecnt = 0

        self.pulsecnt += 1

        return self.pulse_out


    def __genRamp(self, cycliclvl):
        """ Cyclic ramp wave data generator.
        """
        step = cycliclvl/100.0

        if self.ramp_cnt >= 100:
            self.ramp_out = 0
            self.ramp_cnt = 0
        else:
            self.ramp_out += step
            self.ramp_cnt += 1

        return self.ramp_out


    def __genSaw(self, cycliclvl):
        """ Cyclic sawtooth wave data generator.
        """
        step = cycliclvl/50.0

        if self.saw_dir == 1:
            self.saw_out += step
        else:
            self.saw_out -= step

        self.saw_cnt += 1

        if self.saw_cnt == 51:
            if self.saw_dir == 1:
                self.saw_dir = 0
                self.saw_cnt = 0
            else:
                self.saw_dir = 1
                self.saw_cnt = 0

        return self.saw_out


    def __genCyclic(self, inchan):
        """ Cyclic data generator dispatcher.

            Invokes the cyclic data source generator corresponding to
            the currently selected cyclic data source.

            Returns nothing.
        """
        if self.cyclictype[inchan] == DS.CYCNONE:
            self.cyclicdata[inchan] = self.cycliclvl[inchan]

        elif self.cyclictype[inchan] == DS.CYCSINE:
            self.cyclicdata[inchan] = self.__genSine(self.cycliclvl[inchan])

        elif self.cyclictype[inchan] == DS.CYCPULSE:
            self.cyclicdata[inchan] = self.__genPulse(self.cycliclvl[inchan])

        elif self.cyclictype[inchan] == DS.CYCRAMP:
            self.cyclicdata[inchan] = self.__genRamp(self.cycliclvl[inchan])

        elif self.cyclictype[inchan] == DS.CYCSAW:
            self.cyclicdata[inchan] = self.__genSaw(self.cycliclvl[inchan])


    # THREAD
    def __cyclic(self, inchan):
        """ Cyclic data sources main thread.

            Handles trigger events and invokes the cyclic source
            function dispatcher, __genCyclic().

            Returns nothing.
        """
        while self.stopSim != True:
            # In NO_TRIG mode all cyclic source run continuously at
            # the clock rate set by the setCyclicClock() method.
            #
            # In EXT_TRIG mode cyclic sources perfom a single
            # operation.
            #
            # In INT_TRIG mode cyclic sources perfom a single
            # operation.
            if self.trigger[inchan] == DS.NO_TRIG:
                self.__genCyclic(inchan)

            elif self.trigger[inchan] == DS.EXT_TRIG:
                if self.trigevt[inchan] == True:
                    self.__genCyclic(inchan)
                    self.trigevt[inchan] = False

            elif self.trigger[inchan] == DS.INT_TRIG:
                if self.trigevt[inchan] == True:
                    self.__genCyclic(inchan)
                    self.trigevt[inchan] = False

            time.sleep(self.cyclicrate[inchan])


    def __fileRead(self, inchan):
        if self.fileref[inchan] != None:
            rc, fdata = self.fileref[inchan].getData()
            if rc == RC.NO_ERR:
                self.filebuffer[inchan] = fdata
                self.in_file[inchan] = True

    # THREAD
    def __fileData(self, inchan):
            # In NO_TRIG mode data source file reads do not occur
            # until an output channel is accessed.
            #
            # In EXT_TRIG mode file sources are read once for each
            # trigger occurance.
            #
            # In INT_TRIG mode data source files are read once each
            # time an output channel is accessed (same as NO_TRIG
            # mode).
        while self.stopSim != True:
            if self.trigger[inchan] == DS.EXT_TRIG:
                if self.trigevt[inchan] == True:
                    self.__fileRead(inchan)
                    self.trigevt[inchan] = False
            else:
                if self.filetrig[inchan] == True:
                    self.__fileRead(inchan)
                    self.filetrig[inchan] = False

            time.sleep(self.simtime)


    #-----------------------------------------------------------------
    # Simulator main loop
    #-----------------------------------------------------------------
    # THREAD
    def __simLoop(self):
        """ Simulator main loop.

            The main loop continuously checks for input data (either
            from an external caller or from a cyclic source) for each
            input channel. If data is available it starts the
            processing chain that will ultimately result in the data
            appearing in the output buffers.

            The main loop runs forever as a thread. All externally
            supplied data is buffered, and all output data is buffered.
            When running in cyclic mode the output buffers will be
            overwritten with new data as it becomes available.
        """
        # wait for start signal then release the main thread
        wait_start = True
        if self.debug:
            print "waiting..."

        # wait for the startSim flag to go True
        while wait_start:
            if self.startSim == True:
                if self.debug:
                    print "running..."
                wait_start = False
            else:
                time.sleep(0.1)     # wait 100 ms

        # and we're off, run until stopSim is set to True
        while self.stopSim != True:
            # scan through all four input channels, get available data and
            # write it into the input data buffers (databuffer). File input
            # is handled as part of the output loop, below.
            for ichan in range(0, 4):
                if self.in_src[ichan] == DS.EXT_IN:
                    indata = self.inbuffer[ichan]
                else:
                    indata = self.__getCycData(ichan)

                # if a user-supplied function is defined, then apply
                # it to the data
                self.databuffer[ichan] = self.__doUserFunc(ichan, indata)

            # step through each MUX channel, fetch file data (if available),
            # apply scaling and noise, and write the data into the output
            # buffer.
            for ochan in range(0,4):
                # get MUX channel source ID
                mux_src = self.out_src[ochan]

                # handle ext and cyclic data sources
                if (mux_src >= DS.INCHAN1) and \
                   (mux_src <= DS.INCHAN4):
                    outdata = self.databuffer[mux_src]

                # fetch file data (if configured to do so)
                if (mux_src >= DS.SRCFILE1) and \
                   (mux_src <= DS.SRCFILE4):
                    outdata = self.filebuffer[mux_src-4]  # normalize index

                randdata = self.__getRandom()

                oscaled = self.__scaleData(outdata, self.outscale[ochan])
                rscaled = self.__scaleData(randdata, self.randscale[ochan])

                self.outbuffer[ochan] = oscaled + rscaled
                self.outavail[ochan] = True

            time.sleep(self.simtime)


    #-----------------------------------------------------------------
    # Simulator launch
    #-----------------------------------------------------------------
    def __run(self):
        """ Simulator start.

            Instantiates the main loop thread, Sets up the cyclic and
            file I/O threads, and then waits for the start flag to go
            True. When the start flag becomes True the main loop
            thread is started.
        """
        # input thread object lists
        self.cycThread  = [None, None, None, None]
        self.fileThread = [None, None, None, None]

        # create the cyclic and file input handling threads,
        # four of each
        for inch in range(0,4):
            self.cycThread[inch]  = threading.Thread(target=self.__cyclic, args=[inch])
            self.fileThread[inch] = threading.Thread(target=self.__fileData, args=[inch])

            # start the cyclic and file I/O threads just created
            self.cycThread[inch].start()
            self.fileThread[inch].start()

        # give I/O threads a chance to run
        time.sleep(0.5)

        simloop = threading.Thread(target=self.__simLoop)
        simloop.start()             # start it up
        print "DevSim started"

        # At this point control passes back to the caller that invokved DevSim.
        # DevSim will continue to run in the context of the caller until the
        # stopSim flag is set to True.
