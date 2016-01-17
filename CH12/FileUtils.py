#! /usr/bin/python
#-------------------------------------------------------------------------------
# FileUtils.py
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
""" ASCII Data File R/W Utility Classes.

Defines two classes for reading and writing ASCII data records
using text files.

The methods in this module support opening, closing, reading
and writing ASCII data in the form of single-line records. The
class ASCIIDataWrite handles data record writing, and
ASCIIDataRead handles the reading chores. The instantiated
objects maintain their own file object references, and more
than one instance of either class may be active at any one
time.

There are four record formats available, as follows:

4 fields:   [sequence number] [date] [time] [data]
3 fields:   [date] [time] [data]
2 fields:   [sequence number] [data]
1 Field:    [data]

Note that the timestamp is actually two fields: [data] and
[time]. Records with either 2 or 4 fields will contain a
sequence number. Records with only 3 fields will contain the
timestamp fields, but no sequence number. All record formats
contain the data field, and all fields are written as strings.

The [data] field is always written to a file as the string
representation of a floating point value. In other words,
integers will be written with the fractional part set to zero.
"""

import  os

import  TimeUtils           # time and data utilities
import  RetCodes    as RC   # shared return code definitions


class ASCIIDataWrite:
    """ Methods for writing ASCII data records to a file.

        Defines an object for writing ASCII data records to a
        standard "text file". Each object is unique, and more than
        one object may be in use at any one time.
    """
    def __init__(self):
        self.seq_num  = 0
        self.file_ref = None

    
    def openOutput(self, path, file_name, reset_file=False):
        """ Opens a file for ASCII data ouptut.
        
            If path is not specified (an empty string is given as
            the path) then the file will be opened in the current
            execution directory.
        
            If the reset_file parameter is False then file will be
            opened in append mode. If True then file will be opened
            in write mode and any existing data will be deleted if
            the file already exists.
        """
        rc = RC.NO_ERR

        if len(file_name) > 0:
            # create the fully qualified path name
            file_path = os.path.join(path, file_name)
            
            if reset_file:
                fmode = "w"
            else:
                fmode = "a"
    
            try:
                self.file_ref = open(file_path, fmode)
            except Exception, e:
                rc = RC.OPEN_ERR
                print "%s" % str(e)
        else:
            rc = RC.NO_NAME

        return rc
    
    
    def closeOutput(self):
        """ Close an already opened output file.

            If file is not open then an error is returned.
        """
        rc = RC.NO_ERR
  
        if self.file_ref and self.file_ref != None:
            rc = closeFile(self.file_ref)
        else:
            rc = RC.NO_FILE
    
        return rc
    
    
    def writeData(self, dataval, use_sn=False, use_ts=False):
        """ Generates a string containing a data value in ASCII.
        
            If use_ts is False then no timestamp is applied. Otherwise
            a timestamp will be obtained and applied to the output
            string.
        """
        rc = RC.NO_ERR
    
        if use_sn:
            # need to init the sequence number?
            if self.seq_num == 0:
                self.seq_num = 1
            sn = "%02d " % self.seq_num
            self.seq_num += 1
        else:
            sn = ""

        if use_ts:
            ts = TimeUtils.getTS() + " "
        else:
            ts = ""
    
        hdr = sn + ts
    
        # if self.file_ref is None then a file has not yet been
        # opened for this instance
        if self.file_ref == None:
            rc = RC.NO_FILE
    
        # do not proceed if errors encountered
        if rc == RC.NO_ERR:
            try:
                dstr = " %f" % float(dataval)
            except Exception, e:
                rc = RC.INV_DATA
                print "%s" % str(e)

            if rc == RC.NO_ERR:
                outstr = hdr + dstr + "\n"
    
                try:
                    self.file_ref.write(outstr)
                except Exception, e:
                    rc = RC.WRITE_ERR
                    print "%s" % str(e)
    
        return rc


class ASCIIDataRead:
    """ Defines an object for reading ASCII data records from a
        standard text file. Each object is unique, and more than
        one object may be in use at any one time.
    """
    def __init__(self):
        self.file_ref  = None
    

    def openInput(self, path, file_name):
        """ Opens a file for ASCII data input.
        
            If path is not specified (an empty string is given as
            the path) then the function will attempt to open the
            named file in the current execution directory.
        """
        rc = RC.NO_ERR

        # if path is none, assume file is in local directory
        if path == None:
            path = './'

        # create the fully qualified path name
        file_path = os.path.join(path, file_name)

        try:
            self.file_ref = open(file_path, "r")
        except Exception, e:
            rc = RC.OPEN_ERR
            self.file_ref = None

        return rc


    def closeInput(self):
        """ Close an already opened input file.

            If file is not already open then an error is returned.

            Calls the module function closeFile() to do the actual
            close.
        """
        rc = RC.NO_ERR
  
        if self.file_ref and self.file_ref != None:
            rc = closeFile(self.file_ref)
        else:
            rc = RC.NO_FILE
    
        return rc


    def readDataRecord(self):
        """ Read a complete record string and return it as-is.

            Reads one record at a time and returns the entire record
            string as-is from the file. An EOF returns an empty
            record string.

            Return is a 2-tuple consisting of a return code and the
            record string.
        """
        rc = RC.NO_ERR

        # verify that there is a valid file to read from
        if self.file_ref != None:
            # fetch a line from the file
            try:
                record = self.file_ref.readline()
            except Exception, e:
                record = ""
                rc = RC.READ_ERR
        else:
            record = ""
            rc = RC.NO_FILE

        return rc, record

    
    def readDataFields(self):
        """ Read fields from a record in an ASCII data file.
        
            Reads one record at a time, and returns each record
            as a list object with one list element per field. An
            EOF returns an empty list.

            The data for each field is converted from strings to
            the appropriate data type based on the number of fields
            in the record.

            Returns a 2-tuple consisting of a return code and the
            fields list object.
        """
        rc = RC.NO_ERR
        readflds = []
        retflds  = []

        # fetch record string from file
        rc, recstr = self.readDataRecord()

        # split record into component elements               
        if rc == RC.NO_ERR:
            if len(recstr) > 0:
                readflds = recstr.split()

                # Use a try-catch in case data is an invalid type
                # for given conversion to int or float.
                try:
                    if len(readflds) == 4:
                        retflds.append(int(readflds[0]))
                        retflds.append(int(readflds[1]))
                        retflds.append(readflds[2])
                        retflds.append(float(readflds[3]))
                    elif len(readflds) == 3:
                        retflds.append(int(readflds[0]))
                        retflds.append(readflds[1])
                        retflds.append(float(readflds[2]))
                    elif len(readflds) == 2:
                        retflds.append(int(readflds[0]))
                        retflds.append(float(readflds[1]))
                    elif len(readflds) == 1:
                        retflds.append(float(readflds[0]))
                    else:
                        rc = RC.INV_FORMAT
                except Exception, e:
                    print str(e)
                    retflds = []
                    rc = RC.INV_DATA
            else:
                rc = RC.NO_DATA

        return rc, retflds


    def getData(self):
        """ Returns just the data portion of a record.

            Returns a 2-tuple consisting of the return code and the
            data value.

            A record should always have a data field. This method
            returns just the data field, and nothing else, as a
            floating point value. If the data field does not exist
            or if an error occurs retrieving a record, then it will
            return None.
        """
        retdata = None

        rc, infields = self.readDataFields()
        if rc == RC.NO_ERR:
            # assume that readDataFields() has done its job correctly
            # and we have a valid number of fields to work with.
            if len(infields) == 4:
                retdata = float(infields[3])
            elif len(infields) == 3:
                retdata = float(infields[2])
            elif len(infields) == 2:
                retdata = float(infields[1])
            elif len(infields) == 1:
                retdata = float(infields[0])
        return rc, retdata


# Module functions

def closeFile(file_id):
    """ Close an already opened input or output file.

        file_id is a refernce to a Python file object.
    """
    rc = RC.NO_ERR

    try:
        file_id.close()
    except Exception, e:
        rc = RC.INV_FILE
        print "%s" % str(e)

    return rc


if __name__ == "__main__":
    fout = ASCIIDataWrite()

    fin  = ASCIIDataRead()

    fout.openOutput("./", "futest.dat")

    fout.writeData(2.5, use_ts=True)
    fout.writeData(2.6, use_ts=True)
    fout.writeData(2.7, use_ts=True)
    fout.writeData(2.8, use_ts=True)
    fout.writeData(2.9, use_ts=True)
    fout.writeData(3.0, use_ts=True)

    fout.closeOutput()

    fin.openInput("./","futest.dat")

    print "Read Records"
    print "%d %s" % fin.readDataRecord(),
    print "%d %s" % fin.readDataRecord(),
    print "%d %s" % fin.readDataRecord(),
    print "%d %s" % fin.readDataRecord(),
    print "%d %s" % fin.readDataRecord(),
    print "%d %s" % fin.readDataRecord(),

    fin.closeInput()

    fin.openInput("./","futest.dat")

    print "Read Fields"
    print "%d %s" % fin.readDataFields()
    print "%d %s" % fin.readDataFields()
    print "%d %s" % fin.readDataFields()
    print "%d %s" % fin.readDataFields()
    print "%d %s" % fin.readDataFields()
    print "%d %s" % fin.readDataFields()

    fin.closeInput()