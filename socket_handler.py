#!/usr/bin/env python

import struct
from socket import *
from structures import *
import threading

import loggers

class SocketThread(threading.Thread):
    def __init__(self, session):
        threading.Thread.__init__(self)
        self.session = session
        self.running = True
        self.has_received_packets = False

        #open socket
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', 20777))

        self.daemon = True
        self.start()

    def close(self):
        print "Done"
        self.socket.close()
        self.running = False

    def run(self):
        print "Waiting"
        while self.running:
            #populate a packet object
            #todo, remove calcsize from here and do it in the pkt object
            size = struct.calcsize('f' * len(Packet.keys))
            raw_packet = self.socket.recv(size)
            packet = Packet(raw_packet)

            # request an RLC session if this is the first packet
            if not self.has_received_packets and hasattr(self.session.logger, 'request_session'):
                self.has_received_packets = True
                self.session.logger.request_session(packet)

            #add this packet object to the current session
            self.session.current_lap.add_packet(packet)
            print self.running

        #we've signalled for the recv thread to stop, so do cleanup
        print "Closing!"
        self.socket.close()

if __name__ == '__main__':
    #Threading probably not required here, but could make adding a GUI later
    #a bit easier?
    s = Session(loggers.RacingLeagueCharts())
    thread = SocketThread(s);
    while True:
        pass #todo print out some stuff
