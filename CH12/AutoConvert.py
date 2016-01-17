#! /usr/bin/python
#-------------------------------------------------------------------------------
# AutoConvert.py
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
def AutoConvert(input):
    """ Attempts to identify and convert any type of input to a standard
        Python type.

        Useful for dealing with values stored in a configuration data
        file (i.e. an 'ini' file) where the values read from the KV pairs
        are always in string format.

        Returns the converted value (or just the input value, if no
        conversion took place) along with the data type as a 2-tuple.
        Always returns valid data, even if it's just a copy of the
        original input. Never returns None.

        Note that Boolean value characters ('t', 'T', 'TRUE', etc.) are
        converted to 0 or 1. They are not returned as Boolean values using
        Python's True or False values. This can be changed easily enough
        if you really want Boolean values as the output.
    """
    if type(input) == str:
        if input.isalpha():
            # convert T and F characters to 1 and 0
            if len(input) == 1 and input.upper() == 'T':
                ret_val = 1
            elif len(input) == 1 and input.upper() == 'F':
                ret_val = 0
            else:
                if input.upper() == "TRUE":
                    ret_val = 1
                elif input.upper() == "FALSE":
                    ret_val = 0
                else:
                    ret_val = input
                #endif
            #endif
        elif input.isdigit():
            # integer in string form, convert it
            ret_val = int(input)
        elif input.isalnum():
            # mixed character string, just pass it on
            ret_val = input
        else:
            # see if string is a float value, or something else
            try:
                ret_val = float(input)
            except:
                # no, see if it's a tuple, list or dictionary. The code
                # below will exclude most attempts to invoke internal
                # functions or built-in methods masquerading as parameter
                # values.
                try:
                    ret_val = eval(input, {"__builtins__":{}}, {})
                except:
                    # eval choked, so just pass it on
                    ret_val = input
        #endif
    else:
        # We'll assume that input is a valid type not captured in a string
        # This might be problematic, since a value from a conventional
        # *.ini file should be a string.
        ret_val = input
    #endif

    ret_type = type(ret_val)

    return ret_val, ret_type


if __name__ == "__main__":
    print "%s  %s" % AutoConvert("T")
    print "%s  %s" % AutoConvert("F")
    print "%s  %s" % AutoConvert("t")
    print "%s  %s" % AutoConvert("f")
    print "%s  %s" % AutoConvert("[0, 4, 1, 8]")
    print "%s  %s" % AutoConvert("5.5")
    print "%s  %s" % AutoConvert("-2")
    print "%s  %s" % AutoConvert("42")
    print "%s  %s" % AutoConvert("Spam, spam, spam")
    print "%s  %s" % AutoConvert("(1, 2, 3)")
    print "%s  %s" % AutoConvert("{1: 'fee', 2: 'fie', 3: 'foe'}")
    print "%s  %s" % AutoConvert(1)
    print "%s  %s" % AutoConvert(99.98)
    print "%s  %s" % AutoConvert([1, 2,])
    print "%s  %s" % AutoConvert((9, 8, 7))