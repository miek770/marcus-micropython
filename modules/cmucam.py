#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep
import re, sys

# Librairies spéciales
#======================
import Adafruit_BBIO.UART as UART
import serial

# GM # Get Mean
# GT # Get Tracked
# L0 1 # LED0 ON
# PM 0 # Poll Mode (Ã  confirmer)
# PS 1 # Packets Skipped (Ã  confirmer)
# RM 2 # Raw Mode - Disable ACK\r and NCK\r
# ST Rmin Rmax Gmin Gmax Bmin Bmax # Set Tracking
# TC # Track Color

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
        self.blink()

        self.write('pm 1') # Poll mode
        self.blink()
        self.write('cr 18 44') # RGB auto white balance on
        self.blink()
        self.write('cr 19 33') # Auto gain on
        self.leds_on()

        sleep(3.0)

        self.track_window()
        self.write('cr 18 40') # RGB auto white balance off
        self.write('cr 19 32') # Auto gain off
        self.leds_off()

    # Contrôle des LEDs
    #===================
    def leds_on(self):
        self.write('l0 1')
        self.write('l1 1')

    def leds_off(self):
        self.write('l0 0')
        self.write('l1 0')
 
    def blink(self):
        self.leds_on()
        sleep(0.1)
        self.leds_off()
        sleep(0.1)

    # Obtiens la version du firmware, pratique pour tester la connexion
    #===================================================================
    def get_version(self):
        return self.write('gv')

    # Enregistre la couleur trackée dans un fichier texte
    #=====================================================
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
    # Avant mes tests le facteur était à 1.5
    # Je devrais plutôt mettre un absolu, par exemple +/- 30 autour de la moyenne
    #=============================================================================
    def mean_to_track(self, m, facteur=5):
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

    # En cours, voir manuel
    #=======================
    def track_window(self):
        self.write('tw')
        self.tc = self.write('gt')

    # Écrit une commande et retourne le résultat (nettoyé)
    #======================================================
    def write(self, s, raw=False):
        self.ser.write('{0}\r'.format(s))
        r = self.ser.readline()
        if not raw:
            return re.sub('[A-Z\r:]', '', r)[1:]
        else:
            return r

    # Repère la couleur préalablement configurée
    # mx my x1 y1 x2 y2 pixels confidence
    #============================================
    def track(self):
        return self.write('tc')

    # Converti de "T packet" à un dictionnaire
    #==========================================
    def t_packet_to_dict(self, t_packet):
        t_dict = dict()
        l = t_packet.split()
        t_dict['mx'] = l.pop(0) # The middle of mass x value
        t_dict['my'] = l.pop(0) # The middle of mass y value
        t_dict['x1'] = l.pop(0) # The left most corner's x value
        t_dict['y1'] = l.pop(0) # The left most corner's y value
        t_dict['x2'] = l.pop(0) # The right most corner's x value
        t_dict['y2'] = l.pop(0) # The right most corner's y value
        t_dict['pixels'] = l.pop(0) # Number of Pixels in the tracked region, scaled and capped at 255: (pixels+4)/8
        t_dict['confidence'] = l.pop(0) # The (# of pixels / area)*256 of the bounded rectangle and capped at 255
        return t_dict

#===============================================================================
# Fonction :    cam
# Description : [...]
#===============================================================================
def cam(conn, args, delay=0.01):
    cmucam = Cmucam()
    track = True

    v = cmucam.get_version()
    if v:
        conn.send(v)
    else:
        conn.send('Erreur : La CMUCam2+ ne répond pas.')
        sys.exit()

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
                conn.send(cmucam.t_packet_to_dict(r))

        sleep(delay)

