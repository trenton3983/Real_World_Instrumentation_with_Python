#-------------------------------------------------------------------------------
# Global error code definitions.
#-------------------------------------------------------------------------------
# A collection of pseudo-constants defining return code values.
#
# A value of zero (0) is always treated as a No Error return code. Negative
# values between -1 and -6, inclusive, are considered to be status codes, and
# do not indicate an error condition.
#
# The functions GetErrorDesc() and GetErrorName() are provided as convenience
# functions. These are useful for extracting information about an error code
# for display on the console or within a dialog box.
#
# IMPORTANT: If these codes a modified then the err_codes and err_defs lists
# will also need to be modified to remain in sync.
#
# The '#:' comment marker is for Epydoc.
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
NO_ERR              = 0

# Device/subsystem state codes
ACTIVE              = -1        #: Device or function is active
INACTIVE            = -2        #: Device or function is inactive
DISABLED            = -3        #: Device of function is disabled
DEV_ON              = -4        #: The device or component is on
DEV_OFF             = -5        #: The device or component is off
DEV_FAIL            = -6        #: Device is in a failed state
# File return codes
NO_PATH             = -7        #: Path could not be found
NO_NAME             = -8        #: No file name supplied
NO_FILE             = -9        #: File reference is invalid
INV_FILE            = -10       #: File reference does not exist
WRITE_ERR           = -11       #: Error writing to file
READ_ERR            = -12       #: Error reading from file
OPEN_ERR            = -13       #: Error opening file
FILE_EMPTY          = -14       #: File is empty (zero size)
DISK_ERROR          = -15       #: Error encountered while accessing disk
DISK_FULL           = -16       #: Iinsufficient space on the disk
# Data handling return codes
OVERRANGE           = -17       #: Over range error (+ or -)
MAXSCALE            = -18       #: Maximum + output value exceeded
MINSCALE            = -19       #: Maximum - output value exceeded
INV_DATA            = -20       #: invalid data type encountered
INV_FORMAT          = -21       #: invalid data format encountered
DIV_ZERO            = -22       #: Divide by zero error
# General data I/O return codes
BAD_CMD             = -23       #: Bad command detected
BAD_RESP            = -24       #: Bad response detected
NO_RESP             = -25       #: Device is non-responsive
NO_DATA             = -26       #: No data available from device
NO_INIT_POSSIBLE    = -27       #: Initialization is not possible
# Communications return codes
SIO_FAIL            = -28       #: SIO error detected
PIO_FAIL            = -29       #: Parallemt I/O error detected
GPIB_FAIL           = -30       #: GPIB error detected
USB_FAIL            = -31       #: USB error detected
NET_FAIL            = -32       #: Network error detected
NO_PORT             = -33       #: No communications port available
IO_BUSY             = -34       #: An I/O operation is currently busy
NO_IO_AVAIL         = -35       #: No I/O available, all channels in use
DISCONNECT          = -36       #: Unexpected comm channel disconnect
# HW device return codes
DEV_AIO_ERR         = -37       #: A fault was detected during an analog I/O operation
DEV_DIO_ERR         = -38       #: A fault was detected during a discrete I/O operation
DEV_FAULT           = -39       #: Generic HW API fault detected
DEV_LIMIT           = -40       #: Device is at a limit
DEV_OVERTEMP        = -41       #: Device reports an over-temperature condition
DEV_UNDERTEMP       = -42       #: Device reports an under-temperature condition
DEV_NOTRDY          = -43       #: Device is not ready
DEV_NOTINIT         = -44       #: Device or subsystem is not initialized
DEV_ALREADY_INIT    = -45       #: Channel or device already initialized
DEV_OVERLOAD        = -46       #: Device overload error
DEV_BUSY            = -47       #: Device is currently busy
# General return codes
CFG_ERROR           = -48       #: Invalid/missing configuration data detected
BAD_PARAM           = -49       #: A function or configuration parameter is out of range or invalid type
PARAMCNT            = -50       #: The number of parameters given is not the expected number
NO_SRC              = -51       #: A source for the requested data was not found
NULL_VALUE          = -52       #: Invalid data detected, null values not acceptable
BAD_VALUE           = -53       #: Value returned to caller is not valid
NO_CFG              = -54       #: Expected configuration data is not available
NO_LOG              = -55       #: Log is not active or not available
CALC_PARM           = -56       #: calculated parameter value is out of range
CFG_VAL             = -57       #: Invalid value retreived from INI file
OBJ_REF             = -58       #: Unable to obtain object reference
OP_ABORT            = -59       #: Operation or action aborted by user
TIMEOUT             = -60       #: A timeout has occurred


# Convenience data
err_codes = ["NO_ERR", "ACTIVE", "INACTIVE", "DISABLED", "DEV_ON", "DEV_OFF",
             "DEV_FAIL", "NO_PATH", "NO_NAME", "NO_FILE", "INV_FILE",
             "WRITE_ERR", "READ_ERR", "OPEN_ERR", "FILE_EMPTY", "DISK_ERROR",
             "DISK_FULL", "OVERRANGE", "MAXSCALE", "MINSCALE", "INV_DATA",
             "INV_FORMAT", "DIV_ZERO", "BAD_CMD", "BAD_RESP", "NO_RESP",
             "NO_DATA", "NO_INIT_POSSIBLE", "SIO_FAIL", "PIO_FAIL", "GPIB_FAIL",
             "USB_FAIL", "NET_FAIL", "NO_PORT", "IO_BUSY", "NO_IO_AVAIL",
             "DISCONNECT", "DEV_AIO_ERR", "DEV_DIO_ERR", "DEV_FAULT",
             "DEV_LIMIT","DEV_OVERTEMP", "DEV_UNDERTEMP", "DEV_NOTRDY",
             "DEV_NOTINIT", "DEV_ALREADY_INIT", "DEV_OVERLOAD", "DEV_BUSY",
             "CFG_ERROR", "BAD_PARAM", "PARAMCNT", "NO_SRC", "NULL_VALUE",
             "BAD_VALUE", "NO_CFG", "NO_LOG", "CALC_PARM", "CFG_VAL",
             "OBJ_REF", "OP_ABORT", "TIMEOUT"]

err_defs =  {"NO_ERR"            : "No error",
             "ACTIVE"            : "Device or function is active",
             "INACTIVE"          : "Device or function is inactive",
             "DISABLED"          : "Device of function is disabled",
             "DEV_ON"            : "The device or component is on",
             "DEV_OFF"           : "The device or component is off",
             "DEV_FAIL"          : "Device is in a failed state",
             "NO_PATH"           : "Path could not be found",
             "NO_NAME"           : "No file name supplied",
             "NO_FILE"           : "File reference is invalid",
             "INV_FILE"          : "File reference does not exist",
             "WRITE_ERR"         : "Error writing to file",
             "READ_ERR"          : "Error reading from file",
             "OPEN_ERR"          : "Error opening file",
             "FILE_EMPTY"        : "File is empty (zero size)",
             "DISK_ERROR"        : "Error encountered while accessing disk",
             "DISK_FULL"         : "Iinsufficient space on the disk",
             "OVERRANGE"         : "Over range error (+ or -)",
             "MAXSCALE"          : "Maximum + output value exceeded",
             "MINSCALE"          : "Maximum - output value exceeded",
             "INV_DATA"          : "invalid data type encountered",
             "INV_FORMAT"        : "invalid data format encountered",
             "DIV_ZERO"          : "Divide by zero error",
             "BAD_CMD"           : "Bad command detected",
             "BAD_RESP"          : "Bad response detected",
             "NO_RESP"           : "Device is non-responsive",
             "NO_DATA"           : "No data available from device",
             "NO_INIT_POSSIBLE"  : "Initialization is not possible",
             "SIO_FAIL"          : "SIO error detected",
             "PIO_FAIL"          : "Parallemt I/O error detected",
             "GPIB_FAIL"         : "GPIB error detected",
             "USB_FAIL"          : "USB error detected",
             "NET_FAIL"          : "Network error detected",
             "NO_PORT"           : "No communications port available",
             "IO_BUSY"           : "An I/O operation is currently busy",
             "NO_IO_AVAIL"       : "No I/O available, all channels in use",
             "DISCONNECT"        : "Unexpected comm channel disconnect",
             "DEV_AIO_ERR"       : "A fault was detected during an analog I/O operation",
             "DEV_DIO_ERR"       : "A fault was detected during a discrete I/O operation",
             "DEV_FAULT"         : "Generic HW API fault detected",
             "DEV_LIMIT"         : "Device is at a limit",
             "DEV_OVERTEMP"      : "Device reports an over-temperature condition",
             "DEV_UNDERTEMP"     : "Device reports an under-temperature condition",
             "DEV_NOTRDY"        : "Device is not ready",
             "DEV_NOTINIT"       : "Device or subsystem is not initialized",
             "DEV_ALREADY_INIT"  : "Channel or device already initialized",
             "DEV_OVERLOAD"      : "Device overload error",
             "DEV_BUSY"          : "Device is currently busy",
             "CFG_ERROR"         : "Invalid/missing configuration data detected",
             "BAD_PARAM"         : "A function or configuration parameter is out of range or invalid type",
             "PARAMCNT"          : "The number of parameters given is not the expected number",
             "NO_SRC"            : "A source for the requested data was not found",
             "NULL_VALUE"        : "Invalid data detected, null values not acceptable",
             "BAD_VALUE"         : "Value returned to caller is not valid",
             "NO_CFG"            : "Expected configuration data is not available",
             "NO_LOG"            : "Log is not active or not available",
             "CALC_PARM"         : "calculated parameter value is out of range",
             "CFG_VAL"           : "Invalid value retreived from INI file",
             "OBJ_REF"           : "Unable to obtain object reference",
             "OP_ABORT"          : "Operation or action aborted by user",
             "TIMEOUT"           : "A timeout has occurred" }


def GetErrorDesc(error_code):
    """ Returns a brief one-line description of an error code value.
    """
    errdesc = "Not an error"
    if error_code <= 0:
        try:
            errdesc = err_defs[err_codes[abs(error_code)]]
        except:
            errdesc = "Invalid error code value"

    return errdesc


def GetErrorName(error_code):
    """ Returns the pseduo-constant name of an error code value.
    """
    errname = "NOT_ERR"

    if error_code <= 0:
        try:
            errname = err_codes[abs(error_code)]
        except:
            errname = "INV_CODE"
    return errname
