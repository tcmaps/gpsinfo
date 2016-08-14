#!/usr/bin/env python

import math
import ephem
import datetime
from __builtin__ import int

class GPSinfo:
    
    def __init__(self):
        """ http://www.celestrak.com/NORAD/elements/gps-ops.txt """
        self.satlist = []
        self.ttf = datetime.time
        self.location = ephem.Observer()
        f = open('gps-ops.txt')
        l1 = f.readline()
        while l1:
            l2 = f.readline()
            l3 = f.readline()
            sat = ephem.readtle(l1,l2,l3)
            pnr = int(sat.name.split('(PRN ')[1].split(')')[0])
            self.satlist.append(Sat(pnr,sat))
            l1 = f.readline()
        f.close()
        
    def get_sats(self,lat,lon):

        self.location.lat = math.radians(lat)
        self.location.lon = math.radians(lon)
        self.location.date = datetime.datetime.now()
        sats = []
        
        for s in self.satlist:

            s.sat.compute(self.location)
            if math.degrees(s.sat.alt) >= 15:
                s.azi = int(math.degrees(s.sat.az))
                s.elv = int(math.degrees(s.sat.alt))
                s.alm, s.eph, s.fix = True, True, True
                sats.append(s)
        return sats
    
class Sat:
    
    def __init__(self, i, satobj):
        self.pnr = i
        self.sat = satobj
        self.azi = float
        self.elv = float
        self.snr = float
        self.alm = bool
        self.eph = bool
        self.fix = bool 

def main():
    g = GPSinfo() 
    sats = g.get_sats(0,0)
    print sats
#     visible = get_visble(0,0,sats)
#     for _vis in visible:     
#         print('GPS sattelite with PRN {} is visible! azimuth: {}*, elevation: {}* '.format(*_vis))



if __name__ == '__main__':
    main()