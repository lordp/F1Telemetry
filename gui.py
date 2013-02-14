#!/usr/bin/env python

import wx
class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = wx.Panel(self)
        font = wx.Font(30, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, 
                       wx.FONTWEIGHT_NORMAL)
        self.quote = wx.StaticText(panel, label="Lap delta: ", 
                                   pos=(20, 30), size=(20,20))
        self.quote.SetFont(font)
        self.Show()

app = wx.App(False)
ExampleFrame(None)
app.MainLoop()
