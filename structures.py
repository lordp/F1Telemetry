#!/usr/bin/env python

import struct   

class Packet(object):
    def __init__(self):
        self.data = {'time': 0, 'laptime': 0, 'lapdistance': 0, 'distance': 0, 
                     'speed': 0, 'lap': 0, 'x': 0, 'y': 0, 'z': 0, 'xv': 0, 
                     'yv': 0, 'zv': 0, 'xr': 0, 'yr': 0, 'zr': 0, 'xd': 0,
                     'yd': 0, 'zd', 'suspensionpositionrearleft': 0,
                     'suspensionpositionrearright': 0, 
                     'suspensionpositionfrontleft': 0,
                     'suspensionpositionfrontright': 0, 
                     'suspensionvelocityrearleft': 0,
                     'suspensionvelocityrearright': 0, 
                     'suspensionvelocityfrontleft': 0,
                     'suspensionvelocityfrontright': 0, 'wheelspeedrearleft': 0,
                     'wheelspeedrearright': 0, 'wheelspeedfrontleft': 0, 
                     'wheelspeedfrontright': 0, 'throttle': 0, 'steer': 0, 
                     'brake': 0, 'clutch': 0, 'gear': 0, 'lateralg': 0,
                     'longitudinalg': 0, 'revs': 0 }

        #build a format string based on the fact that all of the above fields
        #are floats
        #TODO: remove this?
        self.format = ''
        for key in self.data.keys():
            self.format += 'f'
        print self.format

    def __getattr__(self, name):
        #a handy wrapper to allow us to access the data like any other attribute
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError

    def decode_raw_packet(raw_packet):
        #use struct to parse and store raw data
        pass

class Lap(object):
    def __init__(self):  
        self.packets = list()
        pass

    def get_closest_packet(reference_packet):
        def packet_seperation(packet):
            return abs(reference_packet.lap_distance - packet.lap_distance)

        return sorted(self.packets, key=packet_seperation)[0]

    def add_packet(packet):
        self.packets.append(packet)

    def end_lap():
        #return a new lap object, and save the current lap
        pass

if __name__ == '__main__':
    p = Packet()
