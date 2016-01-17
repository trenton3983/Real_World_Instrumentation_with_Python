# somewhere in the module's global namespace we define some control
# variables and assign initial values (these could also be object
# variables):

msglock   = False
errcnt    = 0
errcntmax = 9   # this will result in 10 counts before lockout

# And here is the function/method that does the actual data acquire and error
# message lock-out:

def grabData():
    global msglock, errcnt

    rc = Acquire()

    if rc != OK:
        if msglock == False:
            errcnt += 1
            if errcnt > errcntmax:
                print "ERROR: Data acquisition failed %d times" % (errcntmax + 1)
                msglock = True
    else:
        msglock = False
        errcnt  = 0

    return rc
