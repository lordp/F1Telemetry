import struct
from socket import *
from structures import *

if __name__ == '__main__':
    session = Session()
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('localhost', 20777))
    
    running = True
    print "Running" 
    while running:
        p = Packet()
        raw_packet = s.recv(struct.calcsize(p.format))
        p.decode_raw_packet(raw_packet)
#       print p.time, p.laptime
        b = session.current_lap.add_packet(p)
        if session.fastest_lap:
            closest_packet = session.fastest_lap.get_closest_packet(p)
            lap_delta = p.lap_time - closest_packet.lap_time
            print lap_delta
        if not b:
            print "Lap finished", session.current_lap.lap_time
            session.new_lap()
