#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import requests
from lxml import etree
import os
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

        self.config_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents\\my games\\formulaone2013\\hardwaresettings\\hardware_settings_config.xml")

        self.check_config()
        self.InitUI()
        self.update_gui(self.enabled)
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox_details = wx.BoxSizer(wx.HORIZONTAL)
        your_name_label = wx.StaticText(panel, label = 'Your name:')
        hbox_details.Add(your_name_label, flag = wx.RIGHT|wx.TOP, border = 4)

        drivers = self.get_drivers()
        self.your_name = PromptingComboBox(panel, "", drivers, style = wx.CB_SORT)
        hbox_details.Add(self.your_name, proportion = 1)
        vbox.Add(hbox_details, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border = 10)

        vbox.Add((-1, 20))

        hbox_messages = wx.BoxSizer(wx.HORIZONTAL)
        self.messages_text = wx.StaticText(panel)
        hbox_messages.Add(self.messages_text)
        vbox.Add(hbox_messages)

        vbox.Add((-1, 20))

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)

        self.enable_btn = wx.Button(panel, size = (70, 30))
        self.enable_btn.Bind(wx.EVT_BUTTON, self.toggle_config)
        hbox_buttons.Add(self.enable_btn)

        self.start_btn = wx.Button(panel, label = '&Start', size = (70,30))
        self.start_btn.Bind(wx.EVT_BUTTON, self.start_logging)
        hbox_buttons.Add(self.start_btn)

        quit_btn = wx.Button(panel, size = (70,30), id = wx.ID_EXIT)
        quit_btn.Bind(wx.EVT_BUTTON, self.quit_app)
        hbox_buttons.Add(quit_btn)
        vbox.Add(hbox_buttons, flag = wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL)

        panel.SetSizer(vbox)

    def load_config(self):
        tree = etree.parse(self.config_path)
        return tree.xpath('motion')[0]

    def check_config(self):
        self.motion = self.load_config()
        self.enabled = (self.motion.get('enabled') == 'true' and \
            self.motion.get('ip') == '127.0.0.1' and \
            self.motion.get('port') == '20777' and \
            self.motion.get('extradata') == '3')

    def toggle_config(self, e):
        if self.enabled:
            self.motion.set('enabled', 'false')
            self.update_gui(False)
        else:
            self.motion.set('enabled', 'true')
            self.motion.set('ip', '127.0.0.1')
            self.motion.set('port', '20777')
            self.motion.set('extradata', '3')
            self.update_gui(True)

        config = open(self.config_path, 'w')
        config.write(etree.tostring(self.motion.getparent(), encoding = 'utf-8', xml_declaration = True))
        config.close()

    def update_gui(self, enabled):
        if enabled:
            msg = 'Choose or enter the driver name above, and click start'
            self.messages_text.SetLabel(msg)
            self.enable_btn.SetLabel('&Disable')
            self.start_btn.Enable()
            self.enabled = True
        else:
            msg = 'The telemetry system is not enabled'
            self.messages_text.SetLabel(msg)
            self.enable_btn.SetLabel('&Enable')
            self.start_btn.Disable()
            self.enabled = False


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

    def get_drivers(self):
        try:
            req = requests.get('https://racingleaguecharts.com/drivers.json', verify = False)
            if req.status_code == 200:
                return req.json()
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            return []

if __name__ == '__main__':

    app = wx.App()
    RLCGui(None, title='Racing League Charts Logger')
    app.MainLoop()
