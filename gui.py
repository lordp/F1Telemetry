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
        self.labels = dict()
        for field in fields:
            self.labels[field[0]] = make_label(parent, field[1])

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
            elements.append((make_label(parent, key), 0, label_alignment))
            elements.append((self.labels[key], 0, value_alignment))
        self.AddMany(elements)

    def __getattr__(self, value):
        return self.labels[value]

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
    def __init__(self, parent, id_no):
        wx.Frame.__init__(self, parent, id_no)
        #todo, move send message into the session and out of the sock handler

        sizer = wx.BoxSizer(wx.VERTICAL)
        #test_label = make_label(self, "+0.534352")
        #test_label.SetLabel("test")

        #todo make this an ordered dict
        session_summary = [
            ('delta','0.0'),
            ('2:','0'),
            ('3:','10'),
            ]
        self.fg = FieldGrid(self, 2, 3, session_summary)
        self.SetSizer(self.fg)
        self.Show()

    def on_new_packet(self, packet):
        self.fg.delta.SetLabel(str(packet.lap_time))

    def on_fastest_lap(self, lap):
        print "New fastest lap"

class MainApp(wx.App):
    def OnInit(self):
        self.frame = ExampleFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        s = Session()
        thread = SocketThread(s, self.frame)
        return True 

if __name__ == '__main__':
    app = MainApp(False)
    app.MainLoop()
