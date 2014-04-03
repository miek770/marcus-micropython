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
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
from modules import bumpers
from modules import cmucam
from modules.moteurs import Moteurs

# Dictionnaire de pins digitales
#================================

# pins[index] = (in/out, 0/1, réservée?)

pins = dict()
pins['P8_7'] = (None, None, None)
pins['P8_8'] = (None, None, None)
pins['P8_9'] = (None, None, None)
pins['P8_10'] = (None, None, None)
pins['P8_11'] = (None, None, None)
pins['P8_12'] = (None, None, None)
pins['P8_13'] = (None, None, None) # Peut être utilisée en PWM
pins['P8_14'] = (None, None, None)
pins['P8_15'] = (None, None, None)
pins['P8_16'] = (None, None, None)
pins['P8_17'] = (None, None, None)
pins['P8_18'] = (None, None, None)
pins['P8_19'] = (None, None, None) # Peut être utilisée en PWM
pins['P8_26'] = (None, None, None) # Non-testée
pins['P8_27'] = (None, None, None) # Non-testée
pins['P8_28'] = (None, None, None) # Non-testée
pins['P8_29'] = (None, None, None) # Non-testée
pins['P8_30'] = (None, None, None) # Non-testée
pins['P8_31'] = (None, None, None) # Non-testée
pins['P8_32'] = (None, None, None) # Non-testée
pins['P8_33'] = (None, None, None) # Non-testée
pins['P8_34'] = (None, None, None) # Non-testée
pins['P8_35'] = (None, None, None) # Non-testée
pins['P8_36'] = (None, None, None) # Non-testée
pins['P8_37'] = (None, None, None) # Non-testée
pins['P8_38'] = (None, None, None) # Non-testée
pins['P8_39'] = (None, None, None) # Non-testée
pins['P8_40'] = (None, None, None) # Non-testée
pins['P8_41'] = (None, None, None) # Non-testée
pins['P8_42'] = (None, None, None) # Non-testée
pins['P8_43'] = (None, None, None) # Non-testée
pins['P8_44'] = (None, None, None) # Non-testée
pins['P8_45'] = (None, None, None) # Non-testée
pins['P8_46'] = (None, None, None) # Non-testée
pins['P9_11'] = (None, None, None)
pins['P9_12'] = (None, None, True) # Direction moteur droit
pins['P9_13'] = (None, None, True) # Direction moteur droit
pins['P9_14'] = (None, None, True) # Enable moteur droit (PWM)
pins['P9_15'] = (None, None, True) # Direction moteur gauche
pins['P9_16'] = (None, None, True) # Enable moteur gauche (PWM)
pins['P9_21'] = (None, None, True) # Direction moteur gauche
pins['P9_22'] = (None, None, None)
pins['P9_23'] = (None, None, None)
pins['P9_24'] = (None, None, None)
pins['P9_25'] = (None, None, None)
pins['P9_26'] = (None, None, None)
pins['P9_27'] = (None, None, None)
pins['P9_28'] = (None, None, None)
pins['P9_29'] = (None, None, None)
pins['P9_30'] = (None, None, None)
pins['P9_31'] = (None, None, None)
pins['P9_42'] = (None, None, None)

# Pins analogiques
#==================
# P9_39 - AIN0
# P9_40 - AIN1
# P9_37 - AIN2
# P9_38 - AIN3
# P9_33 - AIN4
# P9_36 - AIN5
# P9_35 - AIN6

#===============================================================================
# Fonction :    set_low(pin, args)
# Description : Regle la pin digitale a 0V.
#===============================================================================
def set_low(pin, args):
    # Vérifie si la pin est réservée par une sous-routine
    if pins[pin][2] != True:

        # Vérifie si la pin est configurée en sortie
        if pins[pin][0] == 'out':
            GPIO.output(pin, GPIO.LOW)
            pins[pin][1] = 0

        elif pins[pin][0] == 'in':
            msg('Erreur : ' + pin + ' est configurée en entrée.', args)

        else:
            msg('Erreur : ' + pin + ' n\'est pas configurée correctement.', args)

    else:
        msg('Erreur : ' + pin + ' est réservée par une sous-routine.', args)

#===============================================================================
# Fonction :    set_high(pin, args)
# Description : Regle la pin digitale a 3.3V.
#===============================================================================
def set_high(pin, args):
    # Vérifie si la pin est réservée par une sous-routine
    if pins[pin][2] != True:

        # Vérifie si la pin est configurée en sortie
        if pins[pin][0] == 'out':
            GPIO.output(pin, GPIO.HIGH)
            pins[pin][1] = 1

        elif pins[pin][0] == 'in':
            msg('Erreur : ' + pin + ' est configurée en entrée.', args)

        else:
            msg('Erreur : ' + pin + ' n\'est pas configurée correctement.', args)

    else:
        msg('Erreur : ' + pin + ' est réservée par une sous-routine.', args)

#===============================================================================
# Fonction :    set_output(pin)
# Description : Configure la pin en mode sortie.
#===============================================================================
def set_output(pin, args):
    # Vérifie si la pin est réservée par une sous-routine
    if pins[pin][2] != True:

        GPIO.setup(pin, GPIO.OUT)
        pins[pin][0] = 'out'

        # Met la pin à 3.3V (high) par défaut
        set_high(pin, args)

    else:
        msg('Erreur : ' + pin + ' est réservée par une sous-routine.', args)

#===============================================================================
# Fonction :    set_input(pin)
# Description : Configure la pin en mode entrée.
#===============================================================================
def set_input(pin, args):
    # Vérifie si la pin est réservée par une sous-routine
    if pins[pin][2] != True:

        GPIO.setup(pin, GPIO.IN)
        pins[pin][0] = 'in'

    else:
        msg('Erreur : ' + pin + ' est réservée par une sous-routine.', args)

#===============================================================================
# Fonction :    msg(msg, args, lvl)
# Description : Cette fonction permet d'utiliser une seule fonction pour toute
#               impression (print ou log) dependamment des arguments en ligne
#               de commande. On ne devrait jamais utiliser directement 'print'
#               et 'logging.log' dans le reste du programme, toujours 'msg'.
#===============================================================================
def msg(msg, args, lvl=logging.INFO):
    if args.verbose:
        print str(msg)
    if args.logfile:
        logging.log(lvl, str(msg))

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
    bumpers_sub = Process(target=bumpers.scan, args=(bumpers_child_conn, ))
    bumpers_sub.start()
    msg('Sous-routine lancée : bumpers_sub', args)

    # CMUCam2+
#    cmucam_parent_conn, cmucam_child_conn = Pipe()
#    cmucam_sub = Process(target=cmucam.cam, args=(cmucam_child_conn, ))
#    cmucam_sub.start()
#    msg('Sous-routine lancée : cmucam_sub', args)

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

#            if cmucam_parent_conn.poll():
#                detection = cmucam_parent_conn.recv()
#                msg(detection, args)

            pass

        # S'exécute toutes les 100ms
        if count_100ms == 100:
            count_100ms = 0

            if blink_parent_conn.poll():
                msg(blink_parent_conn.recv(), args)

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
