#!/usr/bin/env python

import wx
from structures import *
from socket_handler import *

def make_label(parent, text):
    font = wx.Font(30, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, 
                   wx.FONTWEIGHT_NORMAL)
    txt = wx.StaticText(parent, label=text)
    txt.SetFont(font)
    return txt

class FieldGrid(wx.GridSizer):
    def __init__(self, parent, columns, rows, fields):
        #todo make it do we get rows form len(Fields)
        wx.GridSizer.__init__(self, rows, columns, 3, 3)
        self.vertical = True
        self.parent = parent
        self.labels = list()

        if self.vertical:
            assert len(fields) == rows
            assert columns == 2
        else:
            assert len(fields) == columns
            assert rows == 2

        elements = list()
        for field in fields:
            #todo horizontal alignment
            key = field[0]
            value = field[1]
            label_alignment =  wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
            value_alignment =  wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
            self.labels.append(make_label(parent, value))
            elements.append((make_label(parent, key), 0, label_alignment))
            elements.append((self.labels[-1], 0, value_alignment))
        self.AddMany(elements)

class SessionSummary(wx.Panel):
    def __init__(self, parent, session):
        wx.Panel.__init__(self, parent)

        self.session = session
        self.lap_no = 0
        self.fastest_lap_no = 0
        self.fastest_lap_time = 0

    def on_lap_end(new_fastest_lap):
        self.lap_no = self.session.current_lap.lap_no
        if new_fastest_lap:
            self.fastest_lap_no = self.session.fastest_lap.lap_no
            self.fastest_lap_time = self.session.fastest_lap.lap_time

class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        #test_label = make_label(self, "+0.534352")
        #test_label.SetLabel("test")

        #todo make this an ordered dict
        session_summary = [
            ('1:','0'),
            ('2:','0'),
            ('3:','10'),
            ]
        fg = FieldGrid(self, 2, 3, session_summary)
        self.SetSizer(fg)
        self.Show()

class MainApp(wx.App):
    def OnInit(self):
        self.frame = ExampleFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        s = Session()
        thread = SocketThread(s, self.frame)
        return True 

if __name__ == '__main__':
    app = MainApp(False)
    app.MainLoop()
