#!/usr/local/bin/python

import sys, struct, pygame
from socket import *

class TelemPacket(object):
    def __init__(self):
        self.keys = [
            'time',
            'laptime',
            'lapdistance',
            'distance',
            'speed',
            'lap',
            'x',
            'y',
            'z',
            'xv',
            'yv',
            'zv',
            'xr',
            'yr',
            'zr',
            'xd',
            'yd',
            'zd',
            'suspensionpositionrearleft',
            'suspensionpositionrearright',
            'suspensionpositionfrontleft',
            'suspensionpositionfrontright',
            'suspensionvelocityrearleft',
            'suspensionvelocityrearright',
            'suspensionvelocityfrontleft',
            'suspensionvelocityfrontright',
            'wheelspeedrearleft',
            'wheelspeedrearright',
            'wheelspeedfrontleft',
            'wheelspeedfrontright',
            'throttle',
            'steer',
            'brake',
            'clutch',
            'gear',
            'lateralg'
            'longitudinalg',
            'revs'
        ]           
        self.data = list()   

class Graph(object):
    def __init__(self):
        self.graph_width = 10 #seconds
        self.width = 640
        self.height = 480
        self.lines = [[]]

        size=self.width, self.height
        speed=[1,1]
        color=0,0,0 #black

        #setup pygame
        pygame.init()
        self.screen=pygame.display.set_mode(size)
        

    def add_point(self, index, value, value_range):
        #TODO make this safer
        scale_value = value / (value_range[1] - value_range[0])
        self.lines[index].append([self.width, -1 * scale_value * self.height + self.height])

    def update(self):
        #expects 60 calls per second returns boolean
        #handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        #draw the lines
        self.screen.fill((0, 0, 0))
        for points in self.lines:
            if len(points) < 2:
                continue
            pygame.draw.lines(self.screen, (255, 255, 255), False, points)
            delta_x = self.width / 60 / self.graph_width
            for point in points:
                point[0] -= delta_x #move this point to the left

            #keep the points array limited to only what's on the screen
            if len(points) > 60 * self.graph_width:
                points.pop(0)
        pygame.display.flip()
        return True

def get_gear():
    field_count = 38
    float_size = 4
    data = s.recv(float_size * field_count) #recv 1024 bytes at a time
    if data:
        offset = float_size * 33 #gear
        return struct.unpack_from('f', data, offset)[0]
    return -1

if __name__ == '__main__':
    g = Graph()
    s = socket(AF_INET, SOCK_DGRAM) #UDP socket
    s.bind(('127.0.0.1', 20777))
    running = True
    while running:
        gear = get_gear()
        g.add_point(0, gear, [0, 7])
        if not g.update():
            running = False
    s.close()
    #telem_from_file('test.dat')
    #if len(sys.argv) > 1:
    #    send_msg(' '.join(sys.argv[1:]))
    #else:
    #    recv_msg()
