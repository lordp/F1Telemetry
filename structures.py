#!/usr/bin/env python

import struct, wx

class Packet(object):
    def __init__(self):
        self.data = dict()
        self.keys = ['time', 'lap_time', 'lap_distance', 'distance', 'speed',
            'lap_no', 'x', 'y', 'z', 'xv', 'yv', 'zv', 'xr', 'yr', 'zr', 'xd',
            'yd', 'zd', 'suspensionpositionrearleft',
            'suspensionpositionrearright', 'suspensionpositionfrontleft',
            'suspensionpositionfrontright', 'suspensionvelocityrearleft',
            'suspensionvelocityrearright', 'suspensionvelocityfrontleft',
            'suspensionvelocityfrontright', 'wheelspeedrearleft',
            'wheelspeedrearright', 'wheelspeedfrontleft',
            'wheelspeedfrontright', 'throttle', 'steer', 'brake', 'clutch',
            'gear', 'lateralg', 'longitudinalg', 'revs']            

        #TODO: remove this? unnecessary performance hit?
        self.format = ''
        for i in range(len(self.keys)):
            self.format += 'f'

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError

    def decode_raw_packet(self, raw_packet):
        data = list(struct.unpack(self.format, raw_packet))
        self.data = dict(zip(self.keys, data))

class Lap(object):
    def __init__(self, session, callback_target = None):  
        self.session = session
        self.callback_target = callback_target
        self.packets = list()
        self.lap_time = 0
        self.lap_no = 0

    def get_closest_packet(self, reference_packet):
        def packet_seperation(packet):
            return abs(reference_packet.lap_distance - packet.lap_distance)
        return sorted(self.packets, key=packet_seperation)[0]

    def add_packet(self, packet):
        #check if lap has finished, if it hasn't store this packet
        if len(self.packets) > 1 and \
                packet.lap_time < self.packets[-1].lap_time:
            self.finish_lap()
            return False
        self.packets.append(packet)
        #callback
        if self.callback_target:
            wx.CallAfter(self.callback_target.on_new_packet, packet)
        return True

    def finish_lap(self):
        self.lap_time = self.packets[-1].lap_time
        self.lap_no = self.packets[-1].lap_no
        #callbacks
        self.session.new_lap() #this updates current lap to a new lap
        if self.callback_target:
            wx.CallAfter(self.callback_target.on_new_lap, 
                         self.current_lap, self)

class Session(object):
    def __init__(self, callback_target = None):
        self.callback_target = callback_target
        self.last_lap = None
        self.current_lap = None
        self.fastest_lap = None
        self.laps = list()
        self.laps.append(Lap(self, self.callback_target))
        self.current_lap = self.laps[0]

    def new_lap(self):
        print "new lap"
        #record a fastest lap if we don't already have one
        if not self.fastest_lap:
            print "time set"
            self.fastest_lap = self.current_lap
        #update fastest lap if required
        if self.fastest_lap.lap_time > self.current_lap.lap_time:
            #callback (current lap is faster than fastest lap at this point)
            wx.CallAfter(self.callback_target.on_fastest_lap, 
                         self.current_lap, self.fastest_lap)
            self.fastest_lap = self.current_lap
        new_lap = Lap(self, self.callback_target)
        self.current_lap = new_lap
        self.laps.append(new_lap)
