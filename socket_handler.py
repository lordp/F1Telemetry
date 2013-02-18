#!/usr/bin/env python

import struct
import wx
from socket import *
from structures import *
import threading
import gui

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

        self.start()

    def close(self):
        self.running = False

    def run(self):
        while self.running:
            #populate a packet object
            packet = Packet()
            raw_packet = self.socket.recv(struct.calcsize(packet.format))
            packet.decode_raw_packet(raw_packet)

            #add this packet object to the current session
            lap_finished = not self.session.current_lap.add_packet(packet)
            if lap_finished:
                pass #signal an event to the GUI

        #we've signalled for the recv thread to stop, so do cleanup
        self.socket.close()

if __name__ == '__main__':
    s = Session()
    thread = SocketThread(s);
    while True:
        pass #todo print out some stuff
