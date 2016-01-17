#! /usr/bin/python
#-------------------------------------------------------------------------------
# Simple Power Controller (SPC) Simulator
#-------------------------------------------------------------------------------
# A simulation of an 8-channel AC power controller.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

import serial
import time
import getopt
import sys
import ConfigParser

import AutoConvert as cvt

# internal psuedo-constants
OK   = 1
ON   = 1
OFF  = 0
ERR  = 0

NORM = 0
HOLD = 1
CONT = 2

# index values for channel status dictionary
PWR  = 0
ECB  = 1
LIM  = 2

# operation control pseudo-constants

CONSOLE = 0         # use console for all I/O
SERIAL = 1          # use serial port for command/response I/O

CHAN_DELAY = 0.5    # operation delay for realism, this can be zero


class SPCSim:

    def __init__(self, iomode=CONSOLE, sioport=None, monitor=False):
        """ SPCSim initialization.

            In serial I/O mode the port MUST be specified.

            If the parameter monitor is True, then SPC will write messages
            to the console at each step in its execution. This can get very
            noisy, so it should not be used unless necessary.
        """
        # initialize internal model variables
        self.seq_order = [1, 2, 3, 4, 5, 6, 7, 8]
        self.seq_dwell = CHAN_DELAY
        self.seq_sem   = NORM

        # initialize all control channels
        # Format:
        # {channel: [state, ECB, limit]}
        self.channel   = {1: [OFF, OK, 2.0],
                          2: [OFF, OK, 2.0],
                          3: [OFF, OK, 2.0],
                          4: [OFF, OK, 2.0],
                          5: [OFF, OK, 2.0],
                          6: [OFF, OK, 2.0],
                          7: [OFF, OK, 2.0],
                          8: [OFF, OK, 2.0]
                          }

        self.sport   = None     # SIO object
        self.sioname = sioport  # SPORT parameter
        self.siobaud = 9600     # SBAUD
        self.siodata = 8        # SDATA
        self.siospar = 'N'      # SPAR
        self.siostop = 1        # SSTOP

        self.monitor = monitor
        self.iomode = iomode

        self.stop_main = False

        # attempt to load config file parameters
        self.LoadCFG()

        # open the serial interface (if used)
        if self.iomode == SERIAL:
            self.sport = self.InitSIO()
            # If mode is set to SERIAL but no serial port is available the
            # output will default to the console.
            #
            # It might make more sense to generate an error message instead,
            # but this approach will help to avoid a surprise crash of the
            # simulator. In a real system it is unlikely that the serial port
            # would not be available, and if there was a problem a front-panel
            # indicator would probably be used to alert the user.
            if self.sport == None:
                self.iomode = CONSOLE
                if self.monitor == True:
                    print "SIO port access error, using CONSOLE mode"

        self.initMsg()


    #===========================================================================
    # Command methods
    #===========================================================================

    def chanSet(self, chan, state, delay=False):
        """ Common channel power control method.

            Used by SetPower() and SetSeq().

            Returns ERR if any channel is in over-current state (ECB tripped).
            Otherwise returns OK.
        """
        ret_val = ERR

        if (state == ON) and (self.channel[chan][LIM] == 0):
            self.channel[chan][PWR] = OFF
            self.channel[chan][ECB] = ERR
        elif (state == ON) and (self.channel[chan][ECB] == ERR):
            self.channel[chan][PWR] = OFF
        else:
            self.channel[chan][PWR] = state
            if delay:
                time.sleep(self.seq_dwell)
            ret_val = OK

        if self.monitor:
            if self.channel[chan][ECB] == ERR:
                print chan, self.channel[chan], "ECB FAULT"
            else:
                print chan, self.channel[chan]

        return ret_val


    def SetAll(self, cmdstrs):
        """ ALL state

            Enables or disables all eight AC channels in sequence order, and
            does not observe channels marked as inactive.

            The state parameter may be 1 (On) or 0 (Off).

            This is basically just a fast version of the SEQ command. In a
            real device setting all the channels ON or OFF would probably
            be done by writing either 0xFF or 0x00 to the control lines
            connected to the internal relay modules, not by stepping through
            each channel.

            When commanding all channels off, the reverse sequence order
            will be used.
        """
        ret_val = ERR        # preset the return value
        got_err = False

        chan_seq = [1,2,3,4,5,6,7,8]

        state = self.getParamValInt(cmdstrs, 1)

        if self.monitor:
            print "ALL", state

        if state in (ON, OFF):
            if state == OFF:
                chan_seq.reverse()

            for n in chan_seq:
                ret_val = self.chanSet(n, state)
                if ret_val == ERR:
                    got_err = False

        if got_err:
            ret_val = ERR

        return ret_val


    def SetPower(self, cmdstrs):
        """ POW ch, state

            Sets the power state of a channel to either On or Off.

            ch is a channel number, and state may be 1 (On) or 0 (Off).
            Responds with 1 if successful, or 0 if the ECB is tripped at
            power-up or some other error occurred. Waits for command
            completion before returning.
        """
        ret_val = ERR

        chan = self.getParamValInt(cmdstrs, 1)
        if chan != -1:
            state = self.getParamValInt(cmdstrs, 2)
            if state != -1:
                if chan in range(1,9):
                    if self.monitor:
                        print "POW", chan, state
                    if state in (ON, OFF):
                        ret_val = self.chanSet(chan, state, delay=True)
                else:
                    if self.monitor:
                        print "POW invalid channel: ", chan
        return ret_val


    def SetSeq(self, cmdstrs):
        """ SEQ state

            Commands the controller to start either a power-up or power-down
            sequence. If no sequence order has been defined using the SOR
            command, the startup order will be from lowest to highest and the
            shutdown order will be the inverse.

            The parameter state may be 1 (startup) or 0 (shutdown). Responds
            with 1 if successful, or 0 if the ECB is tripped for any channel
            at powerup.
        """
        ret_val = ERR

        set_seq = []
        set_seq = self.seq_order[:]
        seq_hist = []
        got_err = False

        state = self.getParamValInt(cmdstrs, 1)

        if self.monitor:
            print "SEQ", state

        if state != -1:
            if state == OFF:
                set_seq.reverse()

            for n in set_seq:
                if n > 0:
                    seq_hist.append(n)
                    ret_val = self.chanSet(n, state, delay=True)
                    if (ret_val != OK) and (state == ON):
                        # if ECB fault detected only exit seq loop if SEM is
                        # set to NORM (0) or HOLD (1), otherwise carry on.
                        if self.seq_sem in (NORM, HOLD):
                            break
                        if self.seq_sem == CONT:
                            got_err = True  # catch error in CONT mode

            if (ret_val != OK) and (state == ON):
                # do a reverse shutdown
                if self.seq_sem == NORM:
                    seq_hist.reverse()
                    for n in seq_hist:
                        self.chanSet(n, OFF)

            if got_err:
                ret_val = ERR

        return ret_val


    def SetSTM(self, cmdstrs):
        """ STM time

            Sets the amount of time to pause between each step in a power-up
            or power-down sequence. The time is specified in seconds as
            an integer value.

            The default pause time is 1 second.

            Responds with 1 if successful, or 0 if the time value is invalid.
        """
        ret_val = ERR

        tmval = self.getParamValFloat(cmdstrs, 1)
        if tmval != -1:
            self.seq_dwell = tmval
            ret_val = OK

            if self.monitor:
                print "STM", tmval

        return ret_val


    def SetOrder(self, cmdstrs):
        """ SOR ch, ch, ch, ch, ch, ch, ch, ch

            Defines the startup and shutdown sequence order. Shutdown is the
            inverse of startup. The list may contain from one to eight channel
            ID entries. Any channel not in the list will be excluded from
            sequencing.

            Expects cmdstrs to be a list containing the commnd and up to eight
            channel ID numbers. If called from the LoadCFG() method the command
            will be ''.

            Responds with 1 if successful, or 0 if a sequence parameter is
            invalid.
        """
        ret_val = ERR
        chanset = []

        if len(cmdstrs) > 1:
            chans = cmdstrs[1:]
            for c in chans:
                chanset.append(int(c))
            self.seq_order = chanset
            ret_val = OK

            if self.monitor:
                print "SOR", chans

        return ret_val


    def SetSEM(self, cmdstrs):
        """ SEM mode

            Sets the error handling for power-up sequencing (sequence error
            mode), where mode is one of the following:

            0   Normal (default) operation. If the ECB for any channel trips,
                the controller will disable power to any channels that are
                already active, in reverse order.

            1   Error hold mode. If the ECB for any channel trips, the
                controller will halt the startup sequence but will not
                disable any channels that are already active.

            2   Error continue mode. If the ECB for any channel trips during
                a startup sequence, the controller will continue the sequence
                with the next channel in the sequence list.

            Responds with 1 if successful, or 0 if the mode is invalid.
        """
        ret_val = ERR

        semval = self.getParamValInt(cmdstrs, 1)
        if semval != -1:
            self.seq_sem = semval
            ret_val = OK

            if self.monitor:
                print "SEM", semval

        return ret_val


    def ChkChan(self, cmdstrs):
        """ CHK ch|0

            Returns the on/off/error status of channel ch as either 1 or 0.
            If ch is set to 0, the statuses of all eight channels are returned
            as a comma-separated list of channel states. Also returns a 0
            character for a channel if that channel's ECB is tripped. Use the
            ERR command to check the ECB state.
        """
        ret_val = ERR

        chan = self.getParamValInt(cmdstrs, 1)
        if chan != -1:
            if chan == 0:
                retlist = []
                for n in self.seq_order:
                    if self.channel[n][PWR] == OFF or self.channel[n][ECB] == ERR:
                        retlist.append(OFF)
                    else:
                        retlist.append(ON)
                return retlist
            else:
                if self.channel[chan][PWR] == OFF or self.channel[chan][ECB] == ERR:
                    ret_val = OFF
                else:
                    ret_val = ON
        return ret_val


    def ChkECB(self, cmdstrs):
        """ ECB ch|0

            Returns the ECB status of channel ch as either 1 (OK) or 0 (error).
            If n is set to 0, the ECB statuses of all eight channels are
            returned as a comma-separated list of states.
        """
        ret_val = ERR

        chan = self.getParamValInt(cmdstrs, 1)
        if chan != -1:
            if chan == 0:
                retlist = []
                for n in self.seq_order:
                    retlist.append(self.channel[n][ECB])
                return retlist
            else:
                ret_val = self.channel[chan][ECB]

        return ret_val


    def SetLimit(self, cmdstrs):
        """ LIM ch|0, amps

            Sets the current limit of the ECB for channel ch. If 0 is given
            for the channel ID, all channels will be assigned the limit value
            specified by the parameter amps.

            Setting the amps value of an ECB to zero will result in a simulated
            ECB failure for that channel when a POW command is issued. Setting
            the limit back to something other than zero and then issuing a RST
            command for that channel will clear the error condition.

            Responds with 1 if successful, or 0 if the channel ID or current
            limit value is invalid.
        """
        ret_val = ERR

        chan = self.getParamValInt(cmdstrs, 1)
        if chan != -1:
            limit = self.getParamValFloat(cmdstrs, 2)
            if limit != -1:
                if chan == 0:
                    for n in range(1,9):
                        self.channel[n][LIM] = limit
                    ret_val = OK
                    if self.monitor:
                        print "LIM", "ALL", limit
                elif chan in range(1,9):
                    self.channel[chan][LIM] = limit
                    ret_val = OK
                    if self.monitor:
                        print "LIM", chan, limit

        return ret_val


    def RstChan(self, cmdstrs):
        """ RST ch

            Attempts to reset the ECB for channel ch.

            If the current limit for the specified channel is set to zero,
            then it cannot be reset. The limit must first be set to some
            value > 0 first.

            Responds with 1 if successful, or 0 if the ECB could not be reset.
        """
        ret_val = ERR

        chan = self.getParamValInt(cmdstrs, 1)
        if chan != -1:
            if self.channel[chan][LIM] != 0:
                self.channel[chan][ECB] = OK
                ret_val = OK

                if self.monitor:
                    print "RST", chan

        return ret_val


    #===========================================================================
    # command parser and helper methods
    #===========================================================================
    # The only command in the set that doesn't use either 1 or 2 integers as
    # parameters is the SOR command. This feature is used to simplify the code
    # by defining a set of utility methods for converting the items in the
    # command string list passed to each command method by Dispatch(). Only
    # the SOR command requires a special case, which is handled by the
    # getParamList() method below.

    def getParamValInt(self, cmdstrs, pidx):
        """ Convert a member element in a list of strings to an integer.

            The parameter pdix specifies which element to extract and convert.

            If the conversion fails the method will return -1 (since zero is a
            valid parameter valid).
        """
        try:
            ret_val = int(cmdstrs[pidx])
        except Exception, e:
            print "Parameter %d Error: %s" % (pidx, str(e))
            ret_val = -1

        return ret_val


    def getParamValFloat(self, cmdstrs, pidx):
        """ Convert a member element in a list of strings to a float.

            The parameter pdix specifies which element to extract and convert.

            If the conversion fails the method will return -1 (since zero is a
            valid parameter valid).
        """
        try:
            ret_val = float(cmdstrs[pidx])
        except Exception, e:
            print "Parameter %d Error: %s" % (pidx, str(e))
            ret_val = -1

        return ret_val


    def getParamList(self, cmdstrs, pcnt):
        """ Convert a list of parameter strings into a list of integers.
        """
        retlist = []
        if (pcnt > 0) and (pcnt < 9):
            if len(cmdstrs) == pcnt + 1:
                for i in range(1,pcnt+1):
                    try:
                        listval = int(cmdstrs[i])
                    except Exception, e:
                        print "Parameter %d Error: %s" % (i, str(e))
                        ret_val = -1
                        break
                    else:
                        retlist.append(listval)
                        return relist
            else:
                print "Invalid number of parameters"
                ret_val = -1
        else:
            print "Parameter count out of range"
            ret_val = -1

        return ret_val


    def Dispatch(self, instr):
        """ Command parser and function dispatcher.

            Note that there is one additional command that is not mentioned
            in the text: "QUIT". This allows the user to exit the simulator
            in a graceful manner. A real device probably wouldn't have a quit
            command, just a master circuit breaker.

            Also, note that Dispatch() will accept a command string either
            with or without commas, using either upper or lower case for the
            command. There may be one or more spaces between the command and
            its parameters. So, a command that looks like this:
                pow 2, 1
            is the same as:
                POW 2 1

            Lastly, this method differs from what is shown in the text in how
            the command input string is converted to upper case. Rather than
            do the conversion for each IF test, it is done only once when the
            command string is processed into individual strings.
.        """
        ret_val = OK

        if self.monitor:
            print "Dispatch"

        # replace all commas with a space character
        strtmp = instr.replace(',',' ')
        # convert to upper case
        newinstr = strtmp.upper()
        # split input into separate strings
        cmdstrs = newinstr.split()

        # check for the quit command and immediately return if found, else
        # do the usual parse and dispatch.
        if cmdstrs[0] == "QUIT":
            self.stop_main = True
        else:
            if len(cmdstrs) >= 1:
                if cmdstrs[0] == "DMP":
                    self.dumpCFG()
                elif len(cmdstrs) >= 2:
                    if len(cmdstrs[0]) == 3:
                        if cmdstrs[0] == "ALL":
                            ret_val = self.SetAll(cmdstrs)
                        elif cmdstrs[0] == "POW":
                            ret_val = self.SetPower(cmdstrs)
                        elif cmdstrs[0] == "SEQ":
                            ret_val = self.SetSeq(cmdstrs)
                        elif cmdstrs[0] == "STM":
                            ret_val = self.SetSTM(cmdstrs)
                        elif cmdstrs[0] == "SOR":
                            ret_val = self.SetOrder(cmdstrs)
                        elif cmdstrs[0] == "SEM":
                            ret_val = self.SetSEM(cmdstrs)
                        elif cmdstrs[0] == "CHK":
                            ret_val = self.ChkChan(cmdstrs)
                        elif cmdstrs[0] == "ECB":
                            ret_val = self.ChkECB(cmdstrs)
                        elif cmdstrs[0] == "LIM":
                            ret_val = self.SetLimit(cmdstrs)
                        elif cmdstrs[0] == "RST":
                            ret_val = self.RstChan(cmdstrs)
                        else:
                            print "Invalid command code"
                            ret_val = ERR
                        self.SendResp(ret_val)
                    else:
                        print "Invalid command string"
                        ret_val = ERR
                        self.SendResp(ret_val)
            else:
                print "Invalid command input"
                ret_val = ERR
                self.SendResp(ret_val)


    #===========================================================================
    # Command interface methods
    #===========================================================================
    def initMsg(self):
        self.SendResp("\r\n")
        self.SendResp("SPC Simulator")
        self.SendResp("Enter 'quit' to exit")
        self.SendResp("\r\n")


    def InitSIO(self):
        """ Opens a serial port for command I/O."""

        # check to see if a serial port name is defined (it needs to be).
        if self.sioname == None:
            return None

        # Note that the parameter value definitions in pySerial equate directly
        # to what one would expect to see. In other words, serial.PARITY_NONE
        # is just 'N', serial.EIGHTBITS is 8, and serial.STOPBITS_ONE is 1.
        # So there's no reason to convert what we already have, we can just
        # use the values as-is.

        try:
            sport = serial.Serial(port=self.sioname,
                                  baudrate=self.siobaud,
                                  bytesize=self.siodata,
                                  parity=self.siospar.upper(),
                                  stopbits=self.siostop)
        except Exception, e:
            print "SIO error: %s" % str(e)
            return None

        if self.monitor:
            print "SIO initialized"

        return sport


    def GetCommand(self):
        """ Wait for a command from the host.

            If in serial I/O mode we wait for something to appear on the
            serial input. If in command line (CONSOLE) mode raw_input is
            used instead.

            In serial mode the command input will be echoed back. Only a
            CR character is considered to be a valid EOF. An LF character
            is simply ignored.
        """
        instr = ""
        while len(instr) < 1:
            if self.iomode == CONSOLE:
                print ">",
                instr = raw_input()
            else:
                self.sport.write("> ")
                inch = ''
                while inch != '\r':
                    inch = self.sport.read()
                    if inch not in ('\n', '\r'):
                        self.sport.write(inch)
                        instr += inch
                self.sport.write("\r\n")
        return instr


    def SendResp(self, respval):
        """ Send a response to the host.

            Appends a CR-LF pair to the end of the output string.
        """
        if self.iomode == CONSOLE:
            print respval
        else:
            self.sport.write("%s\r\n" % respval)


    #===========================================================================
    # Conifiguration handler
    #===========================================================================

    # The optional spc.ini file is used to define non-default values for things
    # like the ECB trip limits, sequence order, and sequence pause time. If the
    # serial port is not specified It MUST be used
    # to define the port for the serial I/O, as there is no default for this.
    #
    # The SPC expects the INI file to reside in the same directory as SPCSim.py
    # with the name "spc.ini".
    #
    # [SPC]
    # SPORT     Defines the serial port to use (COM2, /dev/tty0, etc.)
    # SBAUD     Specifies the baud rate (default is 9600 baud)
    # SDATA     Specifies the data bits (default is 8)
    # SPAR      Specifies the data parity (default is none, 'N')
    # SSTOP     Specifies the number of stop bits (default is 1)
    # ECBn      Sets the ECB trip limit for channel n (n can be 1 through 8)
    #           The default ECB trip limit is 2.0 amps
    # SOR       Defines the start sequence order as a list of channel numbers
    # STM       Sets the STM pause time
    # SEM       Set the sequence error mode

    def getOpt(self, cfgobj, section, option):
        """ Utility method to fetch data from a parameter file.

            Instead of falling down and emitting a traceback this method will
            just return ERR if a section or parameter cannot be found in a
            parameter file.
        """
        rc = ERR
        optstr = ""
        if cfgobj.has_section(section):
            if cfgobj.has_option(section, option):
                optstr = cfgobj.get(section, option)
                rc = OK
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
        cfg.read('spc.ini')

        # see if a config file was read, don't bother looking for data if it
        # isn't available
        if len(cfg.items('SPC')) == 0:
            if self.monitor == True:
                print "Configuration file data not loaded"
        else:
            if self.monitor == True:
                print "Loading parameters from spi.ini"

            # don't override the SIO port name if it was passed in via a
            # command line parameter
            if self.sioname == None:
                optret = self.getOpt(cfg, 'SPC', 'SPORT')
                if optret[0] == OK:
                    self.sioname = optret[1]

            optret = self.getOpt(cfg, 'SPC', 'SBAUD')
            if optret[0] == OK:
                self.siobaud = int(optret[1])
            optret = self.getOpt(cfg, 'SPC', 'SDATA')
            if optret[0] == OK:
                self.siodata = int(optret[1])
            optret = self.getOpt(cfg, 'SPC', 'SPAR')
            if optret[0] == OK:
                self.siospar = optret[1]
            optret = self.getOpt(cfg, 'SPC', 'SSTOP')
            if optret[0] == OK:
                self.siostop = int(optret[1])
    
            optret = self.getOpt(cfg, 'SPC', 'ECB1')
            if optret[0] == OK:
                cmdlist = ['', '1']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB2')
            if optret[0] == OK:
                cmdlist = ['', '2']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB3')
            if optret[0] == OK:
                cmdlist = ['', '3']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB4')
            if optret[0] == OK:
                cmdlist = ['', '4']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB5')
            if optret[0] == OK:
                cmdlist = ['', '5']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB6')
            if optret[0] == OK:
                cmdlist = ['', '6']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB7')
            if optret[0] == OK:
                cmdlist = ['', '7']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)

            optret = self.getOpt(cfg, 'SPC', 'ECB8')
            if optret[0] == OK:
                cmdlist = ['', '8']
                cmdlist.append("%2.1f" % float(optret[1]))
                self.SetLimit(cmdlist)
    
            optret = self.getOpt(cfg, 'SPC', 'SOR')
            if optret[0] == OK:
                cmdlist = ['']
                # use AutoConvert to translate string list into a real list
                seqlist, rtype = cvt.AutoConvert(optret[1])
                for c in seqlist:
                    cmdlist.append(c)
                self.SetOrder(cmdlist)
    
            optret = self.getOpt(cfg, 'SPC', 'STM')
            if optret[0] == OK:
                cmdlist = ['']
                cmdlist.append(optret[1])
                self.SetSTM(cmdlist)
    
            optret = self.getOpt(cfg, 'SPC', 'SEM')
            if optret[0] == OK:
                cmdlist = ['']
                cmdlist.append(optret[1])
                self.SetSEM(cmdlist)


    def dumpCFG(self):
        """ Utility method to dump the current config paramter values.
        """
        self.SendResp("SIO Name      : %s" % self.sioname)
        self.SendResp("SIO Baud      : %d" % self.siobaud)
        self.SendResp("SIO Data Bits : %d" % self.siodata)
        self.SendResp("SIO Parity    : %s" % self.siospar)
        self.SendResp("SIO Stop Bits : %d" % self.siostop)
        self.SendResp("Seq Order     : %s" % str(self.seq_order))
        self.SendResp("Seq Delay     : %3.2f" % self.seq_dwell)
        self.SendResp("Seq Mode      : %d" % self.seq_sem)
        self.SendResp("")
        self.SendResp("Channel 1     : %s" % str(self.channel[1]))
        self.SendResp("Channel 2     : %s" % str(self.channel[2]))
        self.SendResp("Channel 3     : %s" % str(self.channel[3]))
        self.SendResp("Channel 4     : %s" % str(self.channel[4]))
        self.SendResp("Channel 5     : %s" % str(self.channel[5]))
        self.SendResp("Channel 6     : %s" % str(self.channel[6]))
        self.SendResp("Channel 7     : %s" % str(self.channel[7]))
        self.SendResp("Channel 8     : %s" % str(self.channel[8]))


    #===========================================================================
    # Simulator main loop
    #===========================================================================
    def RunSim(self):
        """ The main loop of the simulator.

            RunSim will loop until a QUIT command is entered by the user or the
            the interpreter is aborted.
        """
        if self.monitor:
            print "Main loop start"

        while not self.stop_main:
            instr = self.GetCommand()
            self.Dispatch(instr)
        self.SendResp("SPCSim terminated\r\n")

        if self.sport != None:
            self.sport.close()


def SPC(mode, port, mon):
    sim = SPCSim(iomode=mode, sioport=port, monitor=mon)
    sim.RunSim()


#===============================================================================
# this will launch SPCSim from a command line start. It accepts up to three
# parameters.
if __name__ == '__main__':
    mode = CONSOLE
    port = None
    mon  = False

    opt_codes   = "i:p:m:"
    opts, args  = getopt.getopt(sys.argv[1:], opt_codes)

    for opt in opts:
        opt_char, opt_val = opt

        # get I/O mode
        if opt_char == '-i':
            if len(opt_val) > 0:
                try:
                    mode = int(opt_val)
                except:
                    mode = CONSOLE
            #endif
        #endif

        # get serial port name
        if opt_char == '-p':
            if len(opt_val) > 0:
                try:
                    port = opt_val
                except:
                    port = None
            #endif
        #endif

        # get monitor mode
        if opt_char == '-m':
            if len(opt_val) > 0:
                try:
                    mon = int(opt_val)
                except:
                    mon = False
            #endif
        #endif

    SPC(mode, port, mon)
