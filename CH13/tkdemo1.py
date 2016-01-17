#! /usr/bin/python
#-------------------------------------------------------------------------------
# tkdemo1.py
# Demostration of Tkinter and the grid placement method
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

from Tkinter import *

class demoGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        # get top level frame reference
        top=self.winfo_toplevel()
        # set the start location in the window manager
        top.wm_geometry('+50+100')

        # set the window title
        self.master.title("Demo 1")

        # configure the global grid behavior
        self.master.rowconfigure( 0, weight = 1 )
        self.master.columnconfigure( 0, weight = 1 )
        self.grid(sticky = W+E+N+S)

        # create string objects for use with label widgets
        self.var1 = StringVar()
        self.var1.set("")
        self.var2 = StringVar()
        self.var2.set("")

        # output state toggle flags
        self.toggle1 = 0
        self.toggle2 = 0

        # create three buttons and three label widgets, one of which
        # is dummy placeholder (for now).

        # bind buttons 1 and 2 to event handlers.

        # the two active label widgets will display green text on a
        # black background.

        self.button1 = Button(self, text="Button 1", width=10)
        self.button1.grid(row=0, column=0)
        self.button1.bind("<Button-1>", self.button1_Click)

        self.text1 = Label(self, text="", width=10, relief=SUNKEN,
                               bg="black", fg="green",
                               textvariable=self.var1)
        self.text1.grid(row=0, column=10)

        self.button2 = Button(self, text="Button 2", width=10)
        self.button2.grid(row=1, column=0)
        self.button2.bind("<Button-1>", self.button2_Click)

        self.text2 = Label(self, text="", width=10, relief=SUNKEN,
                               bg="black", fg="green",
                               textvariable=self.var2)
        self.text2.grid(row=1, column=10)

        self.button3 = Button(self, text="Quit", width=10,
                                  command=self.quit)
        self.button3.grid(row=2, column=0)

        # dummy space filler
        # you could modify this to display something
        self.text3 = Label(self, text="", width=10)
        self.text3.grid(row=2, column=10)

    def button1_Click(self, event):
        if self.toggle1 == 0:
            self.var1.set("0000")
            self.toggle1 = 1
        else:
            self.var1.set("1111")
            self.toggle1 = 0

        print "Button 1"

    def button2_Click(self, event):
        if self.toggle2 == 0:
            self.var2.set("0000")
            self.toggle2 = 1
        else:
            self.var2.set("1111")
            self.toggle2 = 0

        print "Button 2"

app = demoGUI()
app.mainloop()
