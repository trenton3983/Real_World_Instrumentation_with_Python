class AcqData:
    def __init__(self, port_num, timeout):
        self.timeout = timeout
        self.dataport = port_num
        self.dvals = []     # list for acquired data values
        self.dsamps = 0     # number of values actually read
        self.get_rc = 0     # 0 is OK, negative value is an error
        self.get_done = False  # True if thread is finished


    def Trigger(self):
        SendTrigger(self.dataport)


    def _get_data(self, numsamples):
        cnt = 0
        acqfail = False

        while not acqfail:
            self.get_rc, dataval = GetData(self.dataport, self.timeout)
            if self.get_rc == OK:
                self.datasamps = cnt + 1
                self.dvals.append(datavalue)

                cnt += 1
                if cnt > numsamples:
                    break
            else:
                acqfail = True
        self.get_done = True


    def StartDataSamples(self, samplecnt):
        try:
            acq_thread = threading.Thread(target=self._get_data, args=(samplecnt))
            acq_thread.start()

            self.Trigger()       # start the data acquisition

        except Exception, e:
            print "Acquire fault: %s" % str(e)

    def GetDataSamples(self):
        if self.get_done == True:
            return (get_rc, self.dsmaps, self.dvals)
        else:
            return (NOT_DONE, 0, 0)
