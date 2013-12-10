#!/usr/bin/env python

import struct

class Packet(object):
    keys = ['time', 'lap_time', 'lap_distance', 'distance', 'speed',
            'lap_no', 'x', 'y', 'z', 'xv', 'yv', 'zv', 'xr', 'yr', 'zr', 'xd',
            'yd', 'zd', 'suspensionpositionrearleft',
            'suspensionpositionrearright', 'suspensionpositionfrontleft',
            'suspensionpositionfrontright', 'suspensionvelocityrearleft',
            'suspensionvelocityrearright', 'suspensionvelocityfrontleft',
            'suspensionvelocityfrontright', 'wheelspeedrearleft',
            'wheelspeedrearright', 'wheelspeedfrontleft',
            'wheelspeedfrontright', 'throttle', 'steer', 'brake', 'clutch',
            'gear', 'lateralg', 'longitudinalg', 'revs']

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
        return True

    def finish_lap(self):
        self.lap_time = self.packets[-1].lap_time
        self.lap_number = self.packets[-1].lap_no
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
