#!/usr/bin/env python

import math
import ephem
import urllib
import random
import datetime
from __builtin__ import int

class GPSinfo:
    
    def __init__(self):
        
        urllib.urlretrieve ("http://www.celestrak.com/NORAD/elements/gps-ops.txt", "gps-ops.txt")
        f = open('gps-ops.txt')
        self.satlist = []
        self.ttf = datetime.time
        self.location = ephem.Observer()
        
        l1 = f.readline()
        random.seed()
        while l1:
            l2 = f.readline()
            l3 = f.readline()
            sat = ephem.readtle(l1,l2,l3)
            prn = int(sat.name.split('(PRN ')[1].split(')')[0])
            self.satlist.append(Sat(prn,sat))
            l1 = f.readline()
        f.close()
        
    def get_sats(self,lat,lon):

        self.location.lat = math.radians(lat)
        self.location.lon = math.radians(lon)
        self.location.date = datetime.datetime.now()
        sats = []
        
        for s in self.satlist:

            s.tle.compute(self.location)
            if math.degrees(s.tle.alt) >= 15:
                s.azi = int(math.degrees(s.tle.az))
                s.elv = int(math.degrees(s.tle.alt))
                s.snr = s.elv * random.random() * 0.5               
                s.alm, s.eph, s.fix = True, True, True
                sats.append(s)
        return sats
    
class Sat:
    
    def __init__(self, prn, satobj):
        self.prn = prn
        self.tle = satobj
        self.azi = float
        self.elv = float
        self.snr = float
        self.alm = bool
        self.eph = bool
        self.fix = bool 


if __name__ == '__main__':
    g = GPSinfo() 
    sats = g.get_sats(0,0)
    for sat in sats:     
        print('GPS sattelite with PRN {} is visible! azimuth {}*, elevation {}*, SNR {} '.format(sat.prn,sat.azi,sat.elv,sat.snr))
