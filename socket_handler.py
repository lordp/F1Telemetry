#!/usr/bin/env python

from socket import *
from structures import *
import threading


class SocketThread(threading.Thread):
    def __init__(self, session, port, status_bar, config):
        threading.Thread.__init__(self)
        self.session = session
        self.status_bar = status_bar
        self.running = True
        self.has_received_packets = False

        self.session_type = None
        self.track_length = None
        self.forwarding_socket = None

        #open socket
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind(('', int(port)))

        if config['forwarding_enabled'] and config['forwarding_host'] and config['forwarding_port']:
            self.forwarding_socket = socket(AF_INET, SOCK_DGRAM)
            self.forwarding_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.forwarding_socket.connect((forwarding_host, int(forwarding_port)))

        self.daemon = True
        self.start()

    def close(self):
        self.session.logger.add_log_entry("Closing socket.")
        self.status_bar.SetStatusText("Ready.")
        self.socket.close()
        if self.forwarding_socket is not None:
            self.forwarding_socket.close()
        self.running = False

    def run(self):
        self.session.logger.add_log_entry("Waiting for data...")
        self.status_bar.SetStatusText("Waiting for data...")
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
                self.session.logger.add_log_entry("Data received.")
                self.status_bar.SetStatusText("Data received.")

            if self.session_type is None:
                self.session_type = packet.session_type

            if self.track_length is None:
                self.track_length = packet.track_length

            # if the session type or track length changes, request a new session
            if self.session_type != packet.session_type or self.track_length != packet.track_length:
                self.session_type = packet.session_type
                self.track_length = packet.track_length
                self.session.logger.request_session(packet)

            #add this packet object to the current session
            self.session.current_lap.add_packet(packet)

            # forward the packet onto another app
            if self.forwarding_socket is not None:
                self.forwarding_socket.send(raw_packet)

        #we've signalled for the recv thread to stop, so do cleanup
        self.socket.close()
        if self.forwarding_socket is not None:
            self.forwarding_socket.close()
