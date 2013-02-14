#!/usr/bin/env python

import wx

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

        if self.vertical:
            assert len(fields) == rows
            assert columns == 2
        else:
            assert len(fields) == columns
            assert rows == 2

        elements = list()
        for key, value in fields.iteritems():
            #todo horizontal alignment
            label_alignment =  wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
            value_alignment =  wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
            elements.append((make_label(parent, key), 0, label_alignment))
            elements.append((make_label(parent, value), 0, value_alignment))
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
        session_summary = {
            '1:':'0',
            '2:':'0',
            '3:':'10',
            }
        fg = FieldGrid(self, 2, 3, session_summary)
        """gs = wx.GridSizer(2, 2, 3, 3)
        gs.AddMany([(make_label(self, "Lap delta:"), 
                     0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                    (test_label,
                     0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                    (wx.StaticText(self, -1, 'Something else:'), 
                     0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL),
                    (wx.StaticText(self, -1, '12345'), 
                     0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)])
        sizer.Add(gs, 1, wx.EXPAND)"""
        self.SetSizer(fg)
        self.Show()

app = wx.App(False)
ExampleFrame(None)
app.MainLoop()
