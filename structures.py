#!/usr/bin/env python

import struct
import wx

class Packet(object):
    keys = ['time', 'lap_time', 'lap_distance',
            'distance', 'x', 'y', 'z',
            'speed', 'world_speed_x', 'world_speed_y', 'world_speed_z',
            'xr', 'roll', 'zr', 'xd', 'pitch', 'zd',
            'suspension_position_rear_left',
            'suspension_position_rear_right',
            'suspension_position_front_left',
            'suspension_position_front_right',
            'suspension_velocity_rear_left',
            'suspension_velocity_rear_right',
            'suspension_velocity_front_left',
            'suspension_velocity_front_right',
            'wheel_speed_back_left', 'wheel_speed_back_right',
            'wheel_speed_front_left', 'wheel_speed_front_right',
            'throttle', 'steer', 'brake', 'clutch', 'gear',
            'lateral_acceleration', 'longitudinal_acceleration',
            'lap_no', 'engine_revs', 'new_field1',
            'race_position', 'kers_remaining', 'kers_recharge', 'drs_status',
            'difficulty', 'assists', 'fuel_remaining',
            'session_type', 'new_field10', 'sector', 'time_sector1', 'time_sector2',
            'brake_temperature_rear_left', 'brake_temperature_rear_right',
            'brake_temperature_front_left', 'brake_temperature_front_right',
            'new_field18', 'new_field19', 'new_field20', 'new_field21',
            'completed_laps_in_race', 'total_laps_in_race', 'track_length', 'previous_lap_time',
            'new_field_1301', 'new_field_1302', 'new_field_1303']

    def __init__(self, data):
        self.data = dict()
        self.decode_raw_packet(data)

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError

    def __len__(self):
        return struct.calcsize('f' * len(self.keys))

    def decode_raw_packet(self, raw_packet):
        data = list(struct.unpack('f' * len(self.keys), raw_packet))
        self.data = dict(zip(self.keys, data))

class Lap(object):
    def __init__(self, session):
        self.session = session
        self.packets = list()
        self.lap_time = 0
        self.lap_number = 0
        self.sector_1 = None
        self.sector_2 = None

    def get_closest_packet(self, reference_packet):
        def packet_seperation(packet):
            return abs(reference_packet.lap_distance - packet.lap_distance)
        return sorted(self.packets, key=packet_seperation)[0]

    def add_packet(self, packet):
        if packet.time_sector1 > 0 and self.sector_1 == None:
            self.sector_1 = packet.time_sector1

        if packet.time_sector2 > 0 and self.sector_2 == None:
            self.sector_2 = packet.time_sector2

        #check if lap has finished, if it hasn't store this packet
        if len(self.packets) > 1 and \
                packet.lap_time < self.packets[-1].lap_time:
            self.finish_lap(packet)
            return False
        self.packets.append(packet)
        return True

    def finish_lap(self, packet):
        self.lap_time = packet.previous_lap_time#self.packets[-1].lap_time
        self.lap_number = self.packets[-1].lap_no
        del self.packets[:]
        self.session.new_lap() #this updates current lap to a new lap

class Session(object):
    def __init__(self, logger):
        self.logger = logger
        self.last_lap = None
        self.current_lap = None
        self.fastest_lap = None
        self.laps = list()
        self.laps.append(Lap(self))
        self.current_lap = self.laps[0]

    def new_lap(self):
        #record a fastest lap if we don't already have one
        if not self.fastest_lap:
            self.fastest_lap = self.current_lap

        #update fastest lap if required
        if self.fastest_lap.lap_time > self.current_lap.lap_time:
            self.fastest_lap = self.current_lap

        #create a new lap
        self.logger.lap(self.current_lap) #todo new thread?
        new_lap = Lap(self)
        self.current_lap = new_lap
        self.laps.append(new_lap)

class PromptingComboBox(wx.ComboBox):
    def __init__(self, parent, value, choices=[], style=0, **par):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, value, style=style|wx.CB_DROPDOWN, choices=choices, **par)
        self.choices = choices
        self.Bind(wx.EVT_TEXT, self.EvtText)
        self.Bind(wx.EVT_CHAR, self.EvtChar)
        self.Bind(wx.EVT_COMBOBOX, self.EvtCombobox)
        self.ignoreEvtText = False

    def EvtCombobox(self, event):
        self.ignoreEvtText = True
        event.Skip()

    def EvtChar(self, event):
        if event.GetKeyCode() == 8:
            self.ignoreEvtText = True
        event.Skip()

    def EvtText(self, event):
        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return
        currentText = event.GetString()
        found = False
        for choice in self.choices:
            if choice.lower().startswith(currentText.lower()):
                self.ignoreEvtText = True
                self.SetValue(choice)
                self.SetInsertionPoint(len(currentText))
                self.SetMark(len(currentText), len(choice))
                found = True
                break
        if not found:
            event.Skip()

class ShowLogDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(ShowLogDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetTitle('Session log')

    def InitUI(self):
        self.logctrl = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        hbox.Add(okButton)

        vbox.Add(self.logctrl, proportion = 1, flag = wx.ALL | wx.EXPAND, border = 5)
        vbox.Add(hbox, flag = wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border = 10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, e):
        self.Destroy()

    def SetContent(self, log):
        self.logctrl.SetValue('\n'.join(log))
