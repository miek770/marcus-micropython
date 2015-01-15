#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2013 Michel Lavoie <lavoie.michel@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# Librairies standards
#======================
import argparse, logging, sys
from time import sleep
from multiprocessing import Process, Pipe
from random import randint

# Librairies spéciales
#======================
from modules import bumpers
from modules import cmucam
from modules import gp2d12
from modules.moteurs import Moteurs
from modules.pins import *

class Marcus:

    # Initialisation et sous-routines
    #=================================
    def __init__(self, args):
        self.args = args

        if self.args.logfile:
            logging.basicConfig(filename=self.args.logfile,
                                format='%(asctime)s[%(levelname)s] %(message)s',
                                datefmt='%Y/%m/%d %H:%M:%S ',
                                level=logging.DEBUG)

            msg('Logger initié : ' + self.args.logfile, self.args)

        msg('Programme lancé.', self.args)

        # Bumpers
        self.bumpers_parent_conn, self.bumpers_child_conn = Pipe()
        self.bumpers_sub = Process(target=bumpers.scan, args=(self.bumpers_child_conn, self.args))
        self.bumpers_sub.start()
        msg('Sous-routine lancée : bumpers_sub', self.args)

        # CMUCam2+
        self.cmucam_parent_conn, self.cmucam_child_conn = Pipe()
        self.cmucam_sub = Process(target=cmucam.cam, args=(self.cmucam_child_conn, self.args))
        self.cmucam_sub.start()
        msg('Sous-routine lancée : cmucam_sub', self.args)

#        sleep(3.0) # Attend avant de lire la couleur à tracker
#        cmucam_parent_conn.send('track_mean')
#        sleep(0.5)
#        cmucam_parent_conn.send('track_on')

    # Arrêt
    #=======
    def quit(self):
        self.m.arret()
        self.bumpers_sub.terminate()
        self.cmucam_sub.terminate()
        sys.exit()

    # Boucle principale
    #===================
    def loop(self):
        # 0 = Exploration
        # 1 = Combat
        # 2 = ???
        # 3 = Profit
        self.mode = 0

        # Initialisation des moteurs. La variable manoeuvre sert à s'assurer qu'une
        # manoeuvre est maintenue pendant suffisamment de temps pour être efficace
        # (par exemple tourner). C'est un peu comme une hystérésie aléatoire. Il
        # s'agit d'incréments de 100ms (dépend de l'endroit où elle est utilisée
        # dans la boucle principale.
        self.m = Moteurs(self.args)
        self.manoeuvre = 0
        self.patience = 0

        # Seuil de détection pour les GP2D12
        self.seuil_avant = 45 # en cm
        self.seuil_cote = 20 # en cm

        # J'ai créé des compteurs indépendants pour pouvoir les redémarrer à zéro
        # sans affecter les autres (pour ne pas atteindre des chiffres inutilement
        # élevés).
        self.count_10ms = 0
        self.count_100ms = 0
        self.count_1000ms = 0

        while True:

            # S'exécute toutes les 10ms
            if self.count_10ms == 10:
                self.count_10ms = 0

                # Collision
                if self.bumpers_parent_conn.poll():
                    self.impact = self.bumpers_parent_conn.recv()

                    # Impact avant droit
                    if self.impact[0] and not self.impact[1]:
                        msg('Impact avant droit, recule et tourne à gauche', self.args)
                        self.m.freine()
                        sleep(0.2)
                        self.m.recule()
                        sleep(0.5)
                        self.m.tourne_gauche()
                        self.manoeuvre = 1 + randint(0, 1)

                    # Impact avant droit et gauche
                    elif self.impact[0] and self.impact[1]:
                        msg('Impact avant droit, recule...', self.args)
                        self.m.freine()
                        sleep(0.2)
                        self.m.recule()
                        sleep(0.5)
                        i = randint(0, 1)
                        if i == 0:
                            msg('et tourne à gauche', self.args)
                            self.m.tourne_gauche()
                        else:
                            msg('et tourne à droite', self.args)
                            self.m.tourne_droite()
                        self.manoeuvre = 1 + randint(0, 3)

                    # Impact avant gauche
                    elif not self.impact[0] and self.impact[1]:
                        msg('Impact avant gauche, recule et tourne à droite', self.args)
                        self.m.freine()
                        sleep(0.2)
                        self.m.recule()
                        sleep(0.5)
                        self.m.tourne_droite()
                        self.manoeuvre = 1 + randint(0, 1)
 
                    # Impact arrière droit
                    elif self.impact[2] and not self.impact[3]:
                        self.quit() # Temporaire

                    # Impact arrière droit et gauche
                    elif self.impact[2] and self.impact[3]:
                        self.quit() # Temporaire

                    # Impact arrière gauche
                    elif not self.impact[2] and self.impact[3]:
                        pass # À développer
 
                # Détection
                if self.cmucam_parent_conn.poll():
                    self.detection = self.cmucam_parent_conn.recv()
                    msg(self.detection, self.args)

                    # À développer
                    pass

                pass

            # S'exécute toutes les 100ms
            if self.count_100ms == 100:
                self.count_100ms = 0

                # Exploration
                if self.mode == 0:
                    self.av_mi = gp2d12.get_dist('AIN0') # Avant milieu
                    self.av_ga = gp2d12.get_dist('AIN1') # Avant gauche
                    self.av_dr = gp2d12.get_dist('AIN2') # Avant droite

                    # Manoeuvre en cours
                    if self.manoeuvre > 0:
                        self.manoeuvre -= 1

                    else:
                        # Obstacle à gauche
                        if self.av_mi > self.seuil_avant and self.av_ga < self.seuil_cote and self.av_dr > self.seuil_cote:
                            msg('Obstacle à gauche, tourne a droite', self.args)
                            self.m.tourne_droite()
                            self.manoeuvre = 1 + randint(0, 1)

                        # Obstacle devant et à gauche
                        if self.av_mi < self.seuil_avant and self.av_ga < self.seuil_cote and self.av_dr > self.seuil_cote:
                            msg('Obstacle devant et à gauche, tourne a droite', self.args)
                            self.m.tourne_droite()
                            self.manoeuvre = 1 + randint(0, 2)

                        # Obstacle à droite
                        elif self.av_mi > self.seuil_avant and self.av_dr < self.seuil_cote and self.av_ga > self.seuil_cote:
                            msg('Obstacle à droite, tourne a gauche', self.args)
                            self.m.tourne_gauche()
                            self.manoeuvre = 1 + randint(0, 1)

                        # Obstacle devant et à droite
                        elif self.av_mi < self.seuil_avant and self.av_dr < self.seuil_cote and self.av_ga > self.seuil_cote:
                            msg('Obstacle devant et à droite, tourne a gauche', self.args)
                            self.m.tourne_gauche()
                            self.manoeuvre = 1 + randint(0, 2)

                        # Obstacle devant, à droite et à gauche
                        elif self.av_mi < self.seuil_avant and self.av_dr < self.seuil_cote and self.av_ga < self.seuil_cote:
                            msg('Obstacle devant, à droite et à gauche', self.args)
                            i = randint(0, 1)
                            if i == 0:
                                msg('Tourne a gauche', self.args)
                                self.m.tourne_gauche()
                            else:
                                msg('Tourne a droite', self.args)
                                self.m.tourne_droite()
                            self.manoeuvre = 1 + randint(0, 3)

                        # Obstacle devant uniquement
                        elif self.av_mi < self.seuil_avant and self.av_dr > self.seuil_cote and self.av_ga > self.seuil_cote:
                            msg('Obstacle devant uniquement', self.args)
                            i = randint(0, 1)
                            if i == 0:
                                msg('Tourne a gauche', self.args)
                                self.m.tourne_gauche()
                            else:
                                msg('Tourne a droite', self.args)
                                self.m.tourne_droite()
                            self.manoeuvre = 1 + randint(0, 2)

                        # Aucun obstacle en avant
                        else:

                            # C'est trop tranquille
                            if self.patience < 0:
                                msg('Trop tranquille', self.args)
                                i = randint(0, 1)
                                if i == 0:
                                    msg('Tourne a gauche', self.args)
                                    self.m.tourne_gauche()
                                else:
                                    msg('Tourne a droite', self.args)
                                    self.m.tourne_droite()
                                self.manoeuvre = 3 + randint(0, 5)
                                self.patience = 200 + randint(0, 200)

                            # Rien à l'horizon
                            else:
                                msg('.', self.args)
                                self.m.avance()
                                self.patience -= 1

                pass

            # S'exécute toutes les 1s
            if self.count_1000ms == 1000:
                self.count_1000ms = 0

                pass

            self.count_10ms += 1
            self.count_100ms += 1
            self.count_1000ms += 1
            sleep(0.001)

#===============================================================================
# Fonction :    main
# Description : Routine principale
#===============================================================================
def main():
    parser = argparse.ArgumentParser(description='Robot Marcus (BBB) - Michel')

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Imprime l\'aide sur l\'exécution du script.')

    parser.add_argument('-l',
                        '--logfile',
                        action='store',
                        help='Spécifie le chemin du journal d\'événement.')

    marcus = Marcus(args=parser.parse_args())
    marcus.loop()

if __name__ == '__main__':
    main()

