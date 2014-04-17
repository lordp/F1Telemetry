#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import ConfigParser
import wmi
from socket_handler import *
import loggers
from structures import *
from wx.lib.embeddedimage import PyEmbeddedImage

rlc_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABK1J"
    "REFUWIXNl01vE1cUhh87M4wT27Ed2wHTaWInkRLh0EW8wKgKXbCoUKKKUhZIILHgJ/A7WLBA"
    "YhGWsGKRbZFYNFKQJWIordEkBEFT20kUW9jjr/HHeNzFuC4udkha2vCu5tw559xnZs69544F"
    "aHGEsh7l5J8FgPC+EYlEiEajSJLU5bS+vk4sFuPdu3cABINBzp49i67rxGIxkslkz+TDw8NE"
    "o1FmZ2cBqNVqxGIx4vF4b4BoNMrNmzdxuVxdiR4+fMjr1687AFNTU1y/fp1qtcrOzk5fAJfL"
    "xcLCAteuXQNAVVVu3brVH8Bms+F2u0kmk6ytrVGpVDqBCwsLTExMsLa2hiiKOJ1ORFFEFMUP"
    "JvZ4PEQiEcLhMIVCgQcPHgCgaRqKonT5Ch9EA/F4nNu3b7O3twfAhQsXuHHjBoqikEqlej7t"
    "+/L5fFy8eJEzZ86wtLTEnTt3ADAMg3K5/HGA8fFxzp8/j6qqnYTPnj1DURQKhcJHAQRBwO12"
    "4/V6aTQa7O7u9vftNRiJRJicnKTZbALw+PFj7t+/j6Io5PN5wuHwRyEOqp4Au7u7JBIJNE0D"
    "IJfLMT09jWEYJBKJTzZ5X4B4PM7du3fJZDIAzM/Pc/nyZRRFIZvN/vcAuVyOzc3Nzrebm5tD"
    "lmWKxSI2m63j5/P5mJ+fx+PxAJDP51lfX6dQKPD06VN0XWdkZIRLly4BUK/X2djYYHNzc3+A"
    "gyoYDHL16lWKxSIAGxsb3Lt3j9XVVZaXl3n58iWLi4tcuXIFgFKpxNLSUn+AN2/e8OjRIxKJ"
    "BLVarTOeTqdZWVkhmUyiqipWq5UnT56Qy+W6gLLZLNVqlVqtxtbWFpqmcerUKaampjoAf1+G"
    "Ft7rhoFAAFmWyWazpFIpGo0GYL5qWZapVCqk02lEUUSWZZxOZ1eycrlMKpXq7JiSJCHLMqOj"
    "owDouk4qlWJnZ6c3wGFlt9vx+/04HA7A3OkymcyB9oo/9a9qwO/3c+7cOYLBIGAu35WVlX8O"
    "YBs8zqD9JBbLAAC1ahatvI1h1HsGOxwOQqEQp0+f7tgvXrw41EN0AYz45/gy9D0DwiAAe9s/"
    "kXy7TK36add+XwC7c5zjJ7/hmGS245qWYTv5Y+e+02LBJwjYLBYAxgSBofZ1Tw1YEIYlrPZ2"
    "x2y10NU6RumvN3qoGgiJIt/a7ciCGSY5HDiE/imsgyJDs34Gp70AGPUm5ee7VH7NHAxAGLIz"
    "dCKAtWra4xb42mplxmqe5Eo2G3sDA1T6AUgDSGMuHHMnAGhWGtTTReCAAK7QBKHwIrrVrOpA"
    "OoW0sQ4Fdb+wQ2lfAHsggDQTxWI3NyTvz885tp3uC3BsAEadEPS2BzxgkXq6HgzgsDoxDD/M"
    "wXcB01YlWP0Cfvm/ALwOmJkBedK0ky3IGPsDfF7/Bc1mjXpdpdUy24OhFWiWi2CYNVDVNIq6"
    "jqrrAJQbDUqaRrndjq1NDVXTGTLdUWlRNZrorXo7n06r0ewC6GpGbu9XeP0RrFazclrDGsZI"
    "CUQDAF9mj/Gt33C0J2y43VTGxmi0DySSoTKiv8LRNA8yJQSet1y8wuyaLd2g+jZP/fdCb4Cj"
    "0JHXwJED/AHCo/cJTXmxVAAAAABJRU5ErkJggg==")

class RLCGui(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Racing League Charts Logger", pos = wx.DefaultPosition, size = wx.Size( 240,350 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

        self.version = "0.9.3"
        self.SetIcon(rlc_icon.GetIcon())

        self.logger = None
        self.thread = None

        self.local_mode = False

        self.game_host = '127.0.0.1'
        self.game_port = '20777'


        # Start Menu bar
        menu_bar = wx.MenuBar()

        # Start File
        menu_file = wx.Menu()
        
        file_exit = wx.MenuItem(menu_file, 1, "&Exit")
        menu_file.AppendItem(file_exit)
        self.Bind(wx.EVT_MENU, self.quit_app, id=1)

        menu_bar.Append(menu_file, "&File")
        # End File

        # Start Help
        menu_help = wx.Menu()
        
        help_instructions = wx.MenuItem(menu_help, 2, "&Instructions")
        menu_help.AppendItem(help_instructions)
        self.Bind(wx.EVT_MENU, self.menu_instructions, id=2)

        menu_help.AppendSeparator()
        
        help_about = wx.MenuItem(menu_help, 3, "&About")
        menu_help.AppendItem(help_about)
        self.Bind(wx.EVT_MENU, self.menu_about, id=3)
        
        menu_bar.Append(menu_help, "&Help")
        # End Help

        self.SetMenuBar(menu_bar)
        # End Menu bar


        self.game_config_path = os.path.join(os.path.expandvars("%userprofile%"),"Documents\\my games\\formulaone2013\\hardwaresettings\\hardware_settings_config.xml")
        if os.path.isfile(self.game_config_path):
            self.game_config_missing = False
            tree = etree.parse(self.game_config_path)
            self.motion = tree.xpath('motion')[0]
            self.enabled = (self.motion.get('enabled') == 'true' and self.motion.get('extradata') == '3')

            self.game_port = self.motion.get('port')
            self.game_host = self.motion.get('ip')
        else:
            self.game_config_missing = True

        self.game_running = False
        processes = wmi.WMI().Win32_Process(name = 'F1_2013.exe')
        self.game_running = (len(processes) != 0)

        self.app_config_path = 'config.ini'
        self.app_config = ConfigParser.SafeConfigParser()
        self.app_config.read(self.app_config_path)

        self.InitUI()
        self.UpdateUI()
        self.Show()

    def InitUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        sizer = wx.BoxSizer( wx.VERTICAL )

        general_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        general_sizer = wx.StaticBoxSizer( wx.StaticBox( general_panel, wx.ID_ANY, u"General" ), wx.VERTICAL )

        general_boxes = wx.BoxSizer(wx.HORIZONTAL)
        self.enable_general = wx.CheckBox( general_panel, wx.ID_ANY, u"Enable", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.enable_general.Bind(wx.EVT_CHECKBOX, self.save_game_config)
        general_boxes.Add(self.enable_general, 0, wx.ALL, 0)
        general_boxes.Add((100,0))
        self.enable_local = wx.CheckBox( general_panel, wx.ID_ANY, u"Local", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.enable_local.Bind(wx.EVT_CHECKBOX, self.toggle_local)
        general_boxes.Add(self.enable_local, 0, wx.ALL, 0)

        general_sizer.Add( general_boxes, 0, wx.ALL, 5 )

        general_name = wx.BoxSizer( wx.HORIZONTAL )

        self.general_name_label = wx.StaticText( general_panel, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.general_name_label.Wrap( -1 )
        general_name.Add( self.general_name_label, 0, wx.ALL, 5 )

        drivers = self.get_drivers()
        self.general_name_combo = PromptingComboBox(general_panel, "", drivers, style = wx.CB_SORT)
        self.general_name_combo.Bind(wx.EVT_KILL_FOCUS, self.save_app_config)
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
        self.enable_forwarding.Bind(wx.EVT_CHECKBOX, self.save_app_config)
        forwarding_sizer.Add( self.enable_forwarding, 0, wx.ALL, 5 )

        forwarding_host = wx.BoxSizer( wx.HORIZONTAL )

        self.forwarding_host_label = wx.StaticText( forwarding_panel, wx.ID_ANY, u"Host:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.forwarding_host_label.Wrap( -1 )
        forwarding_host.Add( self.forwarding_host_label, 0, wx.ALL, 5 )

        self.forwarding_host_text = wx.TextCtrl( forwarding_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.forwarding_host_text.Bind(wx.EVT_KILL_FOCUS, self.save_app_config)
        forwarding_host.Add( self.forwarding_host_text, 0, wx.ALL, 5 )


        forwarding_sizer.Add( forwarding_host, 1, wx.EXPAND, 5 )

        forwarding_port = wx.BoxSizer( wx.HORIZONTAL )

        self.forwarding_port_label = wx.StaticText( forwarding_panel, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.forwarding_port_label.Wrap( -1 )
        forwarding_port.Add( self.forwarding_port_label, 0, wx.ALL, 5 )

        self.forwarding_port_text = wx.TextCtrl( forwarding_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.forwarding_port_text.Bind(wx.EVT_KILL_FOCUS, self.save_app_config)
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

    def toggle_local(self, e):
        self.local_mode = e.IsChecked()
        self.save_app_config(e)

    def show_log(self, e):
        log = ShowLogDialog(None)
        if self.logger:
            log.SetContent(self.logger.log)
        log.ShowModal()
        log.Destroy()

    def save_game_config(self, e):
        if e.IsChecked():
            self.motion.set('enabled', 'true')
            self.motion.set('ip', '127.0.0.1')
            self.game_port = self.general_port_text.GetValue()
            if self.game_port:
                self.motion.set('port', self.game_port)
            else:
                self.motion.set('port', '20777')
            self.motion.set('extradata', '3')
            self.enabled = True
            self.UpdateUI()
        else:
            self.motion.set('enabled', 'false')
            self.enabled = False
            self.UpdateUI()

        config = open(self.game_config_path, 'w')
        config.write(etree.tostring(self.motion.getparent(), encoding = 'utf-8', xml_declaration = True))
        config.close()

    def save_app_config(self, e):
        self.app_config.set('general', 'name', self.general_name_combo.GetValue())
        self.app_config.set('general', 'local', str(self.local_mode).lower())
        self.app_config.set('forwarding', 'forwarding_enabled', str(self.enable_forwarding.GetValue()).lower())
        self.app_config.set('forwarding', 'forwarding_host', self.forwarding_host_text.GetValue())
        self.app_config.set('forwarding', 'forwarding_port', self.forwarding_port_text.GetValue())
        with open(self.app_config_path, 'w') as config:
            self.app_config.write(config)
        return True

    def UpdateUI(self):
        if self.game_config_missing:
            wx.MessageBox('The game config file cannot be found in the expected place.\n\n{0}'.format(self.game_config_path), 'Info', wx.OK | wx.ICON_INFORMATION)
            self.status_bar.SetStatusText('The game config file cannot be found')
            self.enable_general.Disable()
            self.enable_local.Disable()
            self.general_name_combo.Disable()
            self.general_port_text.Disable()
            self.general_name_combo.Disable()
            self.enable_forwarding.Disable()
            self.forwarding_host_text.Disable()
            self.forwarding_port_text.Disable()
            self.start_button.Disable()
        elif self.game_running and not self.enabled:
            self.status_bar.SetStatusText('The game is already running')
            wx.MessageBox('The game is already running but the telemetry system is not enabled. Please tick the enable box and restart the game.', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            self.general_port_text.SetValue(self.game_port)
            if self.enabled:
                self.status_bar.SetStatusText('Ready')
                self.enable_general.SetValue(True)
            else:
                self.status_bar.SetStatusText('The telemetry system is not enabled')
                self.enable_general.SetValue(False)

            if self.app_config.get('general', 'local') == 'true':
                self.enable_local.SetValue(True)

            if self.app_config.get('general', 'name'):
                self.general_name_combo.SetValue(self.app_config.get('general', 'name'))

            if self.app_config.get('forwarding', 'forwarding_enabled') == 'true':
                self.enable_forwarding.SetValue(True)

            if self.app_config.get('forwarding', 'forwarding_host'):
                self.forwarding_host_text.SetValue(self.app_config.get('forwarding', 'forwarding_host'))

            if self.app_config.get('forwarding', 'forwarding_port'):
                self.forwarding_port_text.SetValue(self.app_config.get('forwarding', 'forwarding_port'))

    def start_logging(self, e):
        if self.thread is not None:
            self.thread.close()
            self.start_button.SetLabel('&Start')
            self.thread = None
        else:
            name = self.general_name_combo.GetValue()
            if not self.enable_general.GetValue():
                wx.MessageBox('You must check the enable box to use the logger', 'Info', wx.OK | wx.ICON_INFORMATION)
                return False
            if name == "":
                wx.MessageBox('You must enter a name to start the logger', 'Info', wx.OK | wx.ICON_INFORMATION)
                return False
            self.start_button.SetLabel('&Stop')
            self.logger = loggers.RacingLeagueCharts(name, self.status_bar, self.local_mode)
            session = Session(self.logger)
            self.thread = SocketThread(session, self.general_port_text.GetValue(), self.status_bar, self.forwarding_host_text.GetValue(), self.forwarding_port_text.GetValue());

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


    # Menu items
    def menu_about(self, e):
        description = "An F1 telemetry logging application."

        info = wx.AboutDialogInfo()
        info.SetName('Racing League Charts Logger')
        info.SetVersion(self.version)
        info.SetWebSite('https://racingleaguecharts.com')
        info.SetDescription(description)
        
        #info.SetIcon(wx.Icon('logo', wx.BITMAP_TYPE_PNG))
        #info.SetCopyright('')
        #info.SetLicence(licence)
        #info.AddDeveloper('Lordp')
        
        wx.AboutBox(info)

    def menu_instructions(self, e):
        frame = Instructions(None, -1, 'Instructions')
        frame.Show(True)

class Instructions(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, ((600,200)), wx.Size(450, 170))

        panel = wx.Panel(self, -1)

        headertext = "Instructions"

        header = wx.StaticText(panel, -1, headertext, (10,15), style=wx.ALIGN_CENTRE)
        header.SetFont( wx.Font( 14, 70, 90, 92, False, wx.EmptyString ) )

        text = ("1. Choose your name from the dropdown list\n"
                "2. (Optional) Change the port this app runs on. (Only do this if another app already uses this port)\n"
                "3. Press start and run the game\n"
                "4. Keep note of the session ID for the race and forward it to Lordp")

        instructionstext = wx.StaticText(panel, -1, text, (10,50), style=wx.ALIGN_LEFT)
        instructionstext.SetMinSize( wx.Size( 430,100 ) )
        instructionstext.SetMaxSize( wx.Size( 430,200 ) )
        instructionstext.Wrap( -1 )

if __name__ == '__main__':

    app = wx.App()
    RLCGui(None, title='Racing League Charts Logger')
    app.MainLoop()