#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep
import re

# Librairies spéciales
#======================
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
        self.ser = serial.Serial('/dev/ttyO0')
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.timeout = 0.1
        self.ser.xonxoff = 0
        self.ser.rtscts = 0

        # Raw Mode (disable ACK\r et NCK\r)
        self.ser.write('rm 2\r')
        self.ser.readline()

        # Poll Mode
        self.poll_mode(True)
        self.ser.readline()

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
    #==========================================
    def get_mean(self):
        self.ser.write('gm\r')
        s = self.ser.readline()
        return re.sub('[A-Z\r:]', '', s)[1:]

    # Configure le poll_mode
    #========================
    def poll_mode(self, state):
        if state:
            self.pm = True
            self.ser.write('pm 1\r')
            self.ser.readline()
        else:
            self.pm = False
            self.ser.write('pm 0\r')
            self.ser.readline()

    # Règle la couleur a repérer
    #============================
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
    #============================================
    def track(self):
        self.ser.write('tc\r')
        s = self.ser.readline()
        return re.sub('[A-Z\r:]', '', s)[1:]

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
def cam(conn, delay=0.01):
    cmucam = Cmucam()
    track = False

    while True:

        if conn.poll():
            # Si l'application principale a envoyé une commande
            cmd = conn.recv()

            if cmd == 'track_mean':
                # Utilise la couleur moyenne comme cible
                cmucam.set_tracked(cmucam.get_mean())

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
            result = cmucam.track()
            # Ajouter une analyse du résultat et la communication avec le
            # programme principal (via conn).

        sleep(delay)

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def main():
    pass

if __name__ == '__main__':
    main()
