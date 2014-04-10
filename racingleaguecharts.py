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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Racing League Charts Logger", pos = wx.DefaultPosition, size = wx.Size( 240,350 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

        self.logger = None
        self.game_host = '127.0.0.1'
        self.game_port = '20777'

        self.config_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents\\my games\\formulaone2013\\hardwaresettings\\hardware_settings_config.xml")
        if os.path.isfile(self.config_path):
            self.game_config_missing = False
            tree = etree.parse(self.config_path)
            self.motion = tree.xpath('motion')[0]
            self.enabled = (self.motion.get('enabled') == 'true' and self.motion.get('extradata') == '3')

            self.game_port = self.motion.get('port')
            self.game_host = self.motion.get('host')
        else:
            self.game_config_missing = True

        self.InitUI()
        self.UpdateUI()
        self.Show()

    def InitUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        sizer = wx.BoxSizer( wx.VERTICAL )

        general_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        general_sizer = wx.StaticBoxSizer( wx.StaticBox( general_panel, wx.ID_ANY, u"General" ), wx.VERTICAL )

        self.enable_general = wx.CheckBox( general_panel, wx.ID_ANY, u"Enable", wx.DefaultPosition, wx.DefaultSize, 0 )
        general_sizer.Add( self.enable_general, 0, wx.ALL, 5 )

        general_name = wx.BoxSizer( wx.HORIZONTAL )

        self.general_name_label = wx.StaticText( general_panel, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.general_name_label.Wrap( -1 )
        general_name.Add( self.general_name_label, 0, wx.ALL, 5 )

        drivers = self.get_drivers()
        self.general_name_combo = PromptingComboBox(general_panel, "", drivers, style = wx.CB_SORT)
        general_name.Add( self.general_name_combo, 0, wx.ALL, 5 )


        general_sizer.Add( general_name, 1, 0, 5 )

        #general_host = wx.BoxSizer( wx.HORIZONTAL )

        #self.general_host_label = wx.StaticText( self, wx.ID_ANY, u"Host:", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.general_host_label.Wrap( -1 )
        #general_host.Add( self.general_host_label, 0, wx.ALL, 5 )

        #self.general_host_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        #general_host.Add( self.general_host_text, 0, wx.ALL, 5 )


        #general_sizer.Add( general_host, 1, wx.EXPAND, 5 )

        general_port = wx.BoxSizer( wx.HORIZONTAL )

        self.general_port_label = wx.StaticText( general_panel, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.general_port_label.Wrap( -1 )
        general_port.Add( self.general_port_label, 0, wx.ALL, 5 )

        self.general_port_text = wx.TextCtrl( general_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        general_port.Add( self.general_port_text, 0, wx.ALL, 5 )


        general_sizer.Add( general_port, 1, wx.EXPAND, 5 )

        general_panel.SetSizer(general_sizer)
        general_panel.Layout()
        general_sizer.Fit(general_panel)

        sizer.Add( general_panel, 1, wx.ALL|wx.EXPAND, 5 )

        # Forwarding options
        forwarding_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        forwarding_sizer = wx.StaticBoxSizer( wx.StaticBox( forwarding_panel, wx.ID_ANY, u"Forwarding" ), wx.VERTICAL )

        self.enable_forwarding = wx.CheckBox( forwarding_panel, wx.ID_ANY, u"Enable", wx.DefaultPosition, wx.DefaultSize, 0 )
        forwarding_sizer.Add( self.enable_forwarding, 0, wx.ALL, 5 )

        forwarding_host = wx.BoxSizer( wx.HORIZONTAL )

        self.forwarding_host_label = wx.StaticText( forwarding_panel, wx.ID_ANY, u"Host:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.forwarding_host_label.Wrap( -1 )
        forwarding_host.Add( self.forwarding_host_label, 0, wx.ALL, 5 )

        self.forwarding_host_text = wx.TextCtrl( forwarding_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        forwarding_host.Add( self.forwarding_host_text, 0, wx.ALL, 5 )


        forwarding_sizer.Add( forwarding_host, 1, wx.EXPAND, 5 )

        forwarding_port = wx.BoxSizer( wx.HORIZONTAL )

        self.forwarding_port_label = wx.StaticText( forwarding_panel, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.forwarding_port_label.Wrap( -1 )
        forwarding_port.Add( self.forwarding_port_label, 0, wx.ALL, 5 )

        self.forwarding_port_text = wx.TextCtrl( forwarding_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        forwarding_port.Add( self.forwarding_port_text, 0, wx.ALL, 5 )


        forwarding_sizer.Add( forwarding_port, 1, wx.EXPAND, 5 )

        forwarding_panel.SetSizer(forwarding_sizer)
        forwarding_panel.Layout()
        forwarding_sizer.Fit(forwarding_panel)

        sizer.Add( forwarding_panel, 1, wx.ALL|wx.EXPAND, 5 )

        # Buttons
        buttons = wx.BoxSizer( wx.HORIZONTAL )

        self.log_button = wx.Button( self, wx.ID_ANY, u"Show &Log", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.log_button.Bind(wx.EVT_BUTTON, self.show_log)
        buttons.Add( self.log_button, 0, wx.ALL, 5 )

        self.start_button = wx.Button( self, wx.ID_ANY, u"&Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.start_button.Bind(wx.EVT_BUTTON, self.start_logging)
        buttons.Add( self.start_button, 0, wx.ALL, 5 )


        sizer.Add( buttons, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( sizer )
        self.Layout()
        self.status_bar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

    def show_log(self, e):
        log = ShowLogDialog(None)
        if self.logger:
            log.SetContent(self.logger.log)
        log.ShowModal()
        log.Destroy()

    def toggle_config(self, e):
        if self.enabled:
            self.motion.set('enabled', 'false')
            self.enabled = False
            self.update_gui()
        else:
            self.motion.set('enabled', 'true')
            self.motion.set('ip', '127.0.0.1')
            self.game_port = self.config_port.GetValue()
            if self.game_port:
                self.motion.set('port', self.game_port)
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
        self.game_port = self.config_port.GetValue()
        self.motion.set('port', self.game_port)
        self.save_config()

    def UpdateUI(self):
        if self.game_config_missing:
            self.status_bar.SetStatusText('The game config file cannot be found')
            self.enable_general.Disable()
            self.general_name_combo.Disable()
            self.general_port_text.Disable()
            self.general_name_combo.Disable()
            self.enable_forwarding.Disable()
            self.forwarding_host_text.Disable()
            self.forwarding_port_text.Disable()
            self.start_button.Disable()
        else:
            if self.enabled:
                self.status_bar.SetStatusText('Ready')
                self.enable_general.SetValue(True)
                self.general_port_text.SetValue(self.game_port)
            else:
                self.status_bar.SetStatusText('The telemetry system is not enabled')
                self.enable_general.SetValue(False)

    def start_logging(self, e):
        if hasattr(self, 'thread'):
            self.thread.close()
            self.start_button.SetLabel('&Start')
        else:
            name = self.general_name_combo.GetValue()
            if not self.enable_general.GetValue():
                wx.MessageBox('You must check the enable box to use the logger', 'Info', wx.OK | wx.ICON_INFORMATION)
                return False
            if name == "":
                wx.MessageBox('You must enter a name to start the logger', 'Info', wx.OK | wx.ICON_INFORMATION)
                return False
            self.start_button.SetLabel('&Stop')
            self.logger = loggers.RacingLeagueCharts(name, self.status_bar)
            session = Session(self.logger)
            self.thread = SocketThread(session, self.general_port_text.GetValue(), self.status_bar);

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
