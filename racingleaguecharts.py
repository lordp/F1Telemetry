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
            size = (350, 140),
            style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX
        )

        self.custom_port = '20777'
        self.config_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents\\my games\\formulaone2013\\hardwaresettings\\hardware_settings_config.xml")
        if os.path.isfile(self.config_path):
            self.config_missing = False
            tree = etree.parse(self.config_path)
            self.motion = tree.xpath('motion')[0]

            self.enabled = (self.motion.get('enabled') == 'true' and \
                self.motion.get('ip') == '127.0.0.1' and \
                self.motion.get('extradata') == '3')

            self.custom_port = self.motion.get('port')
        else:
            self.config_missing = True

        self.InitUI()
        self.update_gui()
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

        vbox.Add((-1, 10))

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
        vbox.Add(hbox_buttons, flag = wx.ALIGN_CENTER_HORIZONTAL)

        vbox.Add((-1, 10))

        hbox_config = wx.BoxSizer(wx.HORIZONTAL)
        config_port_label = wx.StaticText(panel, label = 'Custom Port:')
        hbox_config.Add(config_port_label, flag = wx.RIGHT|wx.TOP, border = 4)

        self.config_port = wx.TextCtrl(panel, 1, self.custom_port)
        self.config_port.Bind(wx.EVT_KILL_FOCUS, self.update_port)
        hbox_config.Add(self.config_port)

        vbox.Add(hbox_config, flag = wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL)

        panel.SetSizer(vbox)

        self.status_bar = self.CreateStatusBar()

    def toggle_config(self, e):
        if self.enabled:
            self.motion.set('enabled', 'false')
            self.enabled = False
            self.update_gui()
        else:
            self.motion.set('enabled', 'true')
            self.motion.set('ip', '127.0.0.1')
            self.custom_port = self.config_port.GetValue()
            if self.custom_port:
                self.motion.set('port', self.custom_port)
            else:
                self.motion.set('port', '20777')
            self.motion.set('extradata', '3')
            self.enabled = True
            self.update_gui()

        self.save_config()

    def save_config(self):
        config = open(self.config_path, 'w')
        config.write(etree.tostring(self.motion.getparent(), encoding = 'utf-8', xml_declaration = True))
        config.close()

    def update_port(self, e):
        self.custom_port = self.config_port.GetValue()
        self.motion.set('port', self.custom_port)
        self.save_config()

    def update_gui(self):
        if self.config_missing:
            self.status_bar.SetStatusText('The config file cannot be found')
            self.enable_btn.SetLabel('&Enable')
            self.enable_btn.Disable()
            self.start_btn.Disable()
        else:
            if self.enabled:
                self.status_bar.SetStatusText('Choose or enter the driver name above, and click start')
                self.enable_btn.SetLabel('&Disable')
                self.start_btn.Enable()
            else:
                self.status_bar.SetStatusText('The telemetry system is not enabled')
                self.enable_btn.SetLabel('&Enable')
                self.start_btn.Disable()

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
            logger = loggers.RacingLeagueCharts(self.your_name.GetValue(), self.status_bar)
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
