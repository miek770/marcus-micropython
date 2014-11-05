#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep
import re

# Librairies spéciales
#======================
import Adafruit_BBIO.UART as UART
import serial

#===============================================================================
# Classe :      Cmucam
# Description : Wrapper pour gérer la communication avec la CMUCam2+ (incluant
#               la configuration et la recherche de l'autre robot).
#===============================================================================
class Cmucam:
    # Initialisation
    #================
    def __init__(self):
        UART.setup('UART1')
        self.ser = serial.Serial('/dev/ttyO1')
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = 0.1
        self.ser.xonxoff = 0
        self.ser.rtscts = 0

        # Configuration de la CMUCam2+
        self.write('rm 2') # Raw mode (disable ACK\r et NCK\r)
        self.write('pm 1') # Poll mode
        self.write('cr 18 44') # RGB auto white balance on

        # Set Tracked
        # (Rmin Rmax Gmin Gmax Bmin Bmax)
        self.tc = None
        self.set_tracked()

    # Enregistre la couleur trackée dans un fichier texte
    #===================================================
    def save_tc(self):
        with open('tc.txt', 'w') as f:
            f.write(self.tc)

    # Récupère la couleur préalablement enregistrée
    #===============================================
    def load_tc(self):
        try:
            with open('tc.txt', 'r') as f:
                self.tc = f.readline()
            return True
        except IOError:
            return False

    # Lit la couleur moyenne vue par la caméra
    # Rmean Gmean Bmean Rdev Gdev Bdev
    #==========================================
    def get_mean(self):
        return self.write('gm')

    # Converti de GM à TC
    #=====================
    def mean_to_track(self, m, facteur=1.5):
        [Rm, Gm, Bm, Rd, Gd, Bd] = m.split()
        Rmin = int(Rm) - facteur*int(Rd)
        Rmax = int(Rm) + facteur*int(Rd)
        Gmin = int(Gm) - facteur*int(Gd)
        Gmax = int(Gm) + facteur*int(Gd)
        Bmin = int(Bm) - facteur*int(Bd)
        Bmax = int(Bm) + facteur*int(Bd)
        return '%i %i %i %i %i %i' %(Rmin, Rmax, Gmin, Gmax, Bmin, Bmax)

    # Règle la couleur a repérer
    # Rmin Rmax Gmin Gmax Bmin Bmax
    #===============================
    def set_tracked(self, color=None):
        if color is None:

            # Si aucune couleur n'est spécifiée
            if not self.load_tc():

                # Si aucune couleur n'a été enregistrée
                return False
        else:
            self.tc = color

        self.ser.write('st {0}\r'.format(self.tc))
        self.ser.readline()
        return True

    # Repère la couleur préalablement configurée
    # mx my x1 y1 x2 y2 pixels confidence
    #============================================
    def track(self):
        return self.write('tc')

    # Écrit une commande et retourne le résultat (nettoyé)
    #======================================================
    def write(self, s, raw=False):
        self.ser.write('{0}\r'.format(s))
        r = self.ser.readline()
        if not raw:
            return re.sub('[A-Z\r:]', '', r)[1:]
        else:
            return r

#===============================================================================
# Fonction :    cam
# Description : [...]
#===============================================================================
def cam(conn, args, delay=0.01):
    cmucam = Cmucam()
    track = False

    while True:

        if conn.poll():
            # Si l'application principale a envoyé une commande
            cmd = conn.recv()

            if cmd == 'track_mean':
                # Utilise la couleur moyenne comme cible
                cmucam.set_tracked(cmucam.mean_to_track(cmucam.get_mean()))

            elif cmd == 'track_on':
                # Active le tracking automatique
                track = True

            elif cmd == 'track_off':
                # Active le tracking automatique
                track = False

            elif cmd == 'save':
                # Sauvegarde la couleur recherchée
                cmucam.save_tc()

        if track:
            # Si le tracking automatique est activé
            # mx my x1 y1 x2 y2 pixels confidence
            r = cmucam.track()
            if r != '0 0 0 0 0 0 0 0':
                conn.send(r)
            # Ajouter une analyse du résultat et la communication avec le
            # programme principal (via conn).

        sleep(delay)

