#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from socket_handler import *
import loggers
from structures import *

class RLCGui(wx.Frame):

    def __init__(self, parent, title):
        super(RLCGui, self).__init__(parent,
            title = title,
            size = (320, 150),
            style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX
        )

        self.InitUI()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox_details = wx.BoxSizer(wx.HORIZONTAL)
        your_name_label = wx.StaticText(panel, label = 'Your name:')
        hbox_details.Add(your_name_label, flag = wx.RIGHT|wx.TOP, border = 4)
        self.your_name = wx.TextCtrl(panel)
        hbox_details.Add(self.your_name, proportion = 1)
        vbox.Add(hbox_details, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)

        vbox.Add((-1, 20))

        hbox_messages = wx.BoxSizer(wx.HORIZONTAL)
        self.messages_text = wx.StaticText(panel, label = 'Enter your name above, and click start')
        hbox_messages.Add(self.messages_text)
        vbox.Add(hbox_messages, flag = wx.ALIGN_CENTER_HORIZONTAL)

        vbox.Add((-1, 20))

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.start_btn = wx.Button(panel, label = '&Start', size = (70,30))
        self.start_btn.Bind(wx.EVT_BUTTON, self.start_logging)
        hbox_buttons.Add(self.start_btn)

        quit_btn = wx.Button(panel, size = (70,30), id = wx.ID_EXIT)
        quit_btn.Bind(wx.EVT_BUTTON, self.quit_app)
        hbox_buttons.Add(quit_btn)
        vbox.Add(hbox_buttons, flag = wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL)

        panel.SetSizer(vbox)

    def start_logging(self, e):
        if hasattr(self, 'thread'):
          self.thread.close()
          self.start_btn.SetLabel('&Start')
        else:
            name = self.your_name.GetValue()
            if name == "":
                wx.MessageBox('You must enter a name to start the logger', 'Info', wx.OK | wx.ICON_INFORMATION)
                return False
            self.start_btn.SetLabel('&Stop')
            logger = loggers.RacingLeagueCharts(self.your_name.GetValue(), self.messages_text)
            session = Session(logger)
            self.thread = SocketThread(session);

    def quit_app(self, e):
        #dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            #wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        #ret = dial.ShowModal()

        #if ret == wx.ID_YES:
            if hasattr(self, 'thread'):
                self.thread.close()
            self.Destroy()

if __name__ == '__main__':

    app = wx.App()
    RLCGui(None, title='Racing League Charts Logger')
    app.MainLoop()
