#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep

# Librairies spéciales
#=====================
import serial

#===============================================================================
# Classe :
# Description :
#===============================================================================
class Cmucam:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyO0')
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = 1
        self.ser.xonxoff = 0
        self.ser.rtscts = 0

        # Raw Mode (disable ACK\r et NCK\r)
        self.ser.write('rm 2\r')

        # Packets Skipped (à confirmer)
        # Pour ralentir le débit de données
        self.ser.write('ps 1\r')

        # Set Tracked
        # (Rmin Rmax Gmin Gmax Bmin Bmax)
        self.tc = None
        self.set_tracked()

        # Poll Mode
        self.poll_mode(False)

    def save_tc(self):
        with open('tc.txt', 'w') as f:
            f.write(self.tc)

    def load_tc(self):
        try:
            with open('tc.txt', 'r') as f:
                self.tc = f.readline(eol='\r')
        except IOError:
            self.tc = self.get_mean()
            self.save_tc()

    def get_mean(self):
        self.ser.write('gm\r')
        self.tc = self.ser.readline(eol='\r')[2:]

    def poll_mode(self, state):
        if state:
            self.pm = True
            self.ser.write('pm 1\r')
        else:
            self.pm = False
            self.ser.write('pm 0\r')

    def set_tracked(self):
        if self.tc is None:
            self.load_tc()
        self.ser.write('st {0}\r'.format(self.tc))

    def track(self):
        self.ser.write('tc\r')

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def track(cam, conn, delay=0.01):
    cam.poll_mode(False)
    cam.track()
    while True:
        print cam.ser.readline()
        sleep(delay)

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def main():
    cam = Cmucam()
    track(cam)

if __name__ == '__main__':
    main()
