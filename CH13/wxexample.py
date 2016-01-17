#! /usr/bin/python
#-------------------------------------------------------------------------------
# wxexample.py
# Demostration of wxPython
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------

#Boa:Frame:Frame1
import wx
import wx.lib.buttons

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BITMAPBUTTON1, wxID_FRAME1BITMAPBUTTON2,
 wxID_FRAME1BITMAPBUTTON3, wxID_FRAME1BITMAPBUTTON4, wxID_FRAME1EXITBUTTON,
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3,
 wxID_FRAME1STATICTEXT4, wxID_FRAME1STATICTEXT5, wxID_FRAME1TEXTCTRL1,
 wxID_FRAME1TEXTCTRL2, wxID_FRAME1TEXTCTRL3, wxID_FRAME1TEXTCTRL4,
 wxID_FRAME1UPDTBUTTON,
] = [wx.NewId() for _init_ctrls in range(16)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(331, 258), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title='wxPython Demo')
        self.SetClientSize(wx.Size(392, 223))
        self.SetBackgroundColour(wx.Colour(187, 187, 187))
        self.SetToolTipString('')

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label='Channel 1', name='staticText1', parent=self,
              pos=wx.Point(24, 64), size=wx.Size(61, 14), style=0)
        self.staticText1.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='Channel 2', name='staticText2', parent=self,
              pos=wx.Point(24, 96), size=wx.Size(61, 14), style=0)
        self.staticText2.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label='Channel 3', name='staticText3', parent=self,
              pos=wx.Point(24, 128), size=wx.Size(61, 14), style=0)
        self.staticText3.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText4 = wx.StaticText(id=wxID_FRAME1STATICTEXT4,
              label='Channel 4', name='staticText4', parent=self,
              pos=wx.Point(24, 160), size=wx.Size(61, 14), style=0)
        self.staticText4.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
              parent=self, pos=wx.Point(104, 56), size=wx.Size(100, 21),
              style=0, value='')
        self.textCtrl1.SetEditable(False)
        self.textCtrl1.SetToolTipString('')

        self.textCtrl2 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL2, name='textCtrl2',
              parent=self, pos=wx.Point(104, 88), size=wx.Size(100, 21),
              style=0, value='')
        self.textCtrl2.SetEditable(False)
        self.textCtrl2.SetToolTipString('')

        self.textCtrl3 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL3, name='textCtrl3',
              parent=self, pos=wx.Point(104, 120), size=wx.Size(100, 21),
              style=0, value='')
        self.textCtrl3.SetEditable(False)
        self.textCtrl3.SetToolTipString('')

        self.textCtrl4 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL4, name='textCtrl4',
              parent=self, pos=wx.Point(104, 152), size=wx.Size(100, 21),
              style=0, value='')
        self.textCtrl4.SetEditable(False)
        self.textCtrl4.SetToolTipString('')

        self.bitmapButton1 = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_FRAME1BITMAPBUTTON1, name='bitmapButton1', parent=self,
              pos=wx.Point(224, 56), size=wx.Size(24, 24),
              style=wx.BU_AUTODRAW)
        self.bitmapButton1.SetToolTipString('')
        self.bitmapButton1.Bind(wx.EVT_BUTTON, self.OnBitmapButton1Button,
              id=wxID_FRAME1BITMAPBUTTON1)

        self.bitmapButton2 = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_FRAME1BITMAPBUTTON2, name='bitmapButton2', parent=self,
              pos=wx.Point(224, 88), size=wx.Size(24, 24),
              style=wx.BU_AUTODRAW)
        self.bitmapButton2.SetToolTipString('')
        self.bitmapButton2.Bind(wx.EVT_BUTTON, self.OnBitmapButton2Button,
              id=wxID_FRAME1BITMAPBUTTON2)

        self.bitmapButton3 = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_FRAME1BITMAPBUTTON3, name='bitmapButton3', parent=self,
              pos=wx.Point(224, 120), size=wx.Size(24, 24),
              style=wx.BU_AUTODRAW)
        self.bitmapButton3.SetToolTipString('')
        self.bitmapButton3.Bind(wx.EVT_BUTTON, self.OnBitmapButton3Button,
              id=wxID_FRAME1BITMAPBUTTON3)

        self.bitmapButton4 = wx.BitmapButton(bitmap=wx.NullBitmap,
              id=wxID_FRAME1BITMAPBUTTON4, name='bitmapButton4', parent=self,
              pos=wx.Point(224, 152), size=wx.Size(24, 24),
              style=wx.BU_AUTODRAW)
        self.bitmapButton4.SetToolTipString('')
        self.bitmapButton4.Bind(wx.EVT_BUTTON, self.OnBitmapButton4Button,
              id=wxID_FRAME1BITMAPBUTTON4)

        self.updtButton = wx.lib.buttons.GenButton(id=wxID_FRAME1UPDTBUTTON,
              label='Update', name='updtButton', parent=self, pos=wx.Point(304,
              56), size=wx.Size(76, 65), style=0)
        self.updtButton.SetToolTipString('Fetch fresh data')
        self.updtButton.Bind(wx.EVT_BUTTON, self.OnUpdtButtonButton,
              id=wxID_FRAME1UPDTBUTTON)

        self.exitButton = wx.lib.buttons.GenButton(id=wxID_FRAME1EXITBUTTON,
              label='Exit', name='exitButton', parent=self, pos=wx.Point(304,
              192), size=wx.Size(76, 25), style=0)
        self.exitButton.Bind(wx.EVT_BUTTON, self.OnExitButtonButton,
              id=wxID_FRAME1EXITBUTTON)

        self.staticText5 = wx.StaticText(id=wxID_FRAME1STATICTEXT5,
              label='Enable/Disable', name='staticText5', parent=self,
              pos=wx.Point(200, 32), size=wx.Size(70, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.initButtons()

    def initButtons(self):
        self.cnt = 1

        self.btn1State = False
        self.btn2State = False
        self.btn3State = False
        self.btn4State = False

        self.bitmapButton1.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))
        self.bitmapButton2.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))
        self.bitmapButton3.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))
        self.bitmapButton4.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))

    def OnBitmapButton1Button(self, event):
        if self.btn1State == False:
            self.btn1State = True
            self.bitmapButton1.SetBitmapLabel(bitmap=wx.Bitmap(u'green24on.bmp', wx.BITMAP_TYPE_BMP))
        else:
            self.btn1State = False
            self.bitmapButton1.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))

    def OnBitmapButton2Button(self, event):
        if self.btn2State == False:
            self.btn2State = True
            self.bitmapButton2.SetBitmapLabel(bitmap=wx.Bitmap(u'green24on.bmp', wx.BITMAP_TYPE_BMP))
        else:
            self.btn2State = False
            self.bitmapButton2.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))

    def OnBitmapButton3Button(self, event):
        if self.btn3State == False:
            self.btn3State = True
            self.bitmapButton3.SetBitmapLabel(bitmap=wx.Bitmap(u'green24on.bmp', wx.BITMAP_TYPE_BMP))
        else:
            self.btn3State = False
            self.bitmapButton3.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))

    def OnBitmapButton4Button(self, event):
        if self.btn4State == False:
            self.btn4State = True
            self.bitmapButton4.SetBitmapLabel(bitmap=wx.Bitmap(u'green24on.bmp', wx.BITMAP_TYPE_BMP))
        else:
            self.btn4State = False
            self.bitmapButton4.SetBitmapLabel(bitmap=wx.Bitmap(u'red24off.bmp', wx.BITMAP_TYPE_BMP))

    def OnUpdtButtonButton(self, event):
        self.textCtrl1.SetValue(str(self.cnt))
        self.textCtrl2.SetValue(str(self.cnt))
        self.textCtrl3.SetValue(str(self.cnt))
        self.textCtrl4.SetValue(str(self.cnt))
        self.cnt += 1

    def OnExitButtonButton(self, event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = create(None)
    frame.Show(True)
    app.MainLoop()