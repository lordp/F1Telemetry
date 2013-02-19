#!/usr/bin/env python

import struct
import wx
from socket import *
from structures import *
import threading
from gui import *


class SocketThread(threading.Thread):
    def __init__(self, session, notify):
        threading.Thread.__init__(self)
        self.notify = notify
        self.session = session
        self.running = True

        #open socket
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', 20777))

        print "starting thread"
        self.start()

    def close(self):
        self.running = False

    def run(self):
        while self.running:
            #populate a packet object
            packet = Packet()
            raw_packet = self.socket.recv(struct.calcsize(packet.format))
            packet.decode_raw_packet(raw_packet)
            wx.CallAfter(self.notify.on_new_packet, packet)

            #add this packet object to the current session
            lap_finished = not self.session.current_lap.add_packet(packet)
            if lap_finished:
                pass

        #we've signalled for the recv thread to stop, so do cleanup
        self.socket.close()

if __name__ == '__main__':
    s = Session()
    thread = SocketThread(s);
    while True:
        pass #todo print out some stuff
