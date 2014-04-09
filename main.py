#!/root/marcus/bin/python
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

# Librairies spéciales
#======================
from modules import bumpers
from modules import cmucam
from modules.moteurs import Moteurs
from modules.pins import *

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
    
    args = parser.parse_args()

    if args.logfile:
        logging.basicConfig(filename=args.logfile,
                            format='%(asctime)s[%(levelname)s] %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S ',
                            level=logging.DEBUG)

        msg('Logger initié : ' + args.logfile, args)

    msg('Programme lancé.', args)

    # Lancement des sous-routines (subprocesses)
    #============================================

    # Bumpers
    bumpers_parent_conn, bumpers_child_conn = Pipe()
    bumpers_sub = Process(target=bumpers.scan, args=(bumpers_child_conn, args))
    bumpers_sub.start()
    msg('Sous-routine lancée : bumpers_sub', args)

    # CMUCam2+
    cmucam_parent_conn, cmucam_child_conn = Pipe()
    cmucam_sub = Process(target=cmucam.cam, args=(cmucam_child_conn, args))
    cmucam_sub.start()
    msg('Sous-routine lancée : cmucam_sub', args)

#    sleep(3.0) # Attend avant de lire la couleur à tracker
#    cmucam_parent_conn.send('track_mean')
#    sleep(0.5)
#    cmucam_parent_conn.send('track_on')

    # Boucle principale
    #===================

    # J'ai créé des compteurs indépendants pour pouvoir les redémarrer à zéro
    # sans affecter les autres (pour ne pas atteindre des chiffres inutilement
    # élevés).
    count_10ms = 0
    count_100ms = 0
    count_1000ms = 0
    while True:

        # S'exécute toutes les 10ms
        if count_10ms == 10:
            count_10ms = 0

            if bumpers_parent_conn.poll():
                impact = bumpers_parent_conn.recv()
                msg(impact, args)

            if cmucam_parent_conn.poll():
                detection = cmucam_parent_conn.recv()
                msg(detection, args)

            pass

        # S'exécute toutes les 100ms
        if count_100ms == 100:
            count_100ms = 0

            pass

        # S'exécute toutes les 1s
        if count_1000ms == 1000:
            count_1000ms = 0

            pass

        count_10ms += 1
        count_100ms += 1
        count_1000ms += 1
        sleep(0.001)

    return 0

if __name__ == '__main__':
    main()
