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

# Dictionnaire de pins digitales
#================================
pins = dict()
pins['P8_7'] = (None, None)
pins['P8_8'] = (None, None)
pins['P8_9'] = (None, None)
pins['P8_10'] = (None, None)
pins['P8_11'] = (None, None)
pins['P8_12'] = (None, None)
pins['P8_13'] = (None, None) # Peut être utilisée en PWM
pins['P8_14'] = (None, None)
pins['P8_15'] = (None, None)
pins['P8_16'] = (None, None)
pins['P8_17'] = (None, None)
pins['P8_18'] = (None, None)
pins['P8_19'] = (None, None) # Peut être utilisée en PWM
pins['P8_26'] = (None, None) # Non-testée
pins['P8_27'] = (None, None) # Non-testée
pins['P8_28'] = (None, None) # Non-testée
pins['P8_29'] = (None, None) # Non-testée
pins['P8_30'] = (None, None) # Non-testée
pins['P8_31'] = (None, None) # Non-testée
pins['P8_32'] = (None, None) # Non-testée
pins['P8_33'] = (None, None) # Non-testée
pins['P8_34'] = (None, None) # Non-testée
pins['P8_35'] = (None, None) # Non-testée
pins['P8_36'] = (None, None) # Non-testée
pins['P8_37'] = (None, None) # Non-testée
pins['P8_38'] = (None, None) # Non-testée
pins['P8_39'] = (None, None) # Non-testée
pins['P8_40'] = (None, None) # Non-testée
pins['P8_41'] = (None, None) # Non-testée
pins['P8_42'] = (None, None) # Non-testée
pins['P8_43'] = (None, None) # Non-testée
pins['P8_44'] = (None, None) # Non-testée
pins['P8_45'] = (None, None) # Non-testée
pins['P8_46'] = (None, None) # Non-testée
pins['P9_11'] = (None, None) # Utilisée par blink_sub
pins['P9_12'] = (None, None)
pins['P9_13'] = (None, None)
pins['P9_14'] = (None, None) # Peut être utilisée en PWM
pins['P9_15'] = (None, None)
pins['P9_16'] = (None, None) # Peut être utilisée en PWM
pins['P9_21'] = (None, None)
pins['P9_22'] = (None, None)
pins['P9_23'] = (None, None)
pins['P9_24'] = (None, None)
pins['P9_25'] = (None, None)
pins['P9_26'] = (None, None)
pins['P9_27'] = (None, None)
pins['P9_28'] = (None, None)
pins['P9_29'] = (None, None)
pins['P9_30'] = (None, None)
pins['P9_31'] = (None, None)
pins['P9_42'] = (None, None)

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
# Fonction :    set_low(pin)
# Description : Regle la pin digitale a 0V.
#===============================================================================
def set_low(pin):
    if pins[pin][0] == 'out':
        GPIO.output(pin, GPIO.LOW)
    elif pins[pin][0] == 'in':
        print 'Erreur:', pin, 'est configurée en entrée.'
    else:
        print 'Erreur:', pin, 'n\'est pas configurée correctement.'

#===============================================================================
# Fonction :    set_high(pin)
# Description : Regle la pin digitale a 3.3V.
#===============================================================================
def set_high(pin):
    if pins[pin][0] == 'out':
        GPIO.output(pin, GPIO.HIGH)
    elif pins[pin][0] == 'in':
        print 'Erreur:', pin, 'est configurée en entrée.'
    else:
        print 'Erreur:', pin, 'n\'est pas configurée correctement.'

#===============================================================================
# Fonction :    set_output(pin)
# Description : Configure la pin en mode sortie.
#===============================================================================
def set_output(pin):
    pins[pin] = ('out', 1)
    GPIO.setup(pin, GPIO.OUT)
    # Met la pin à 3.3V (high) par défaut
    set_high(pin)

#===============================================================================
# Fonction :    set_input(pin)
# Description : Configure la pin en mode entree.
#===============================================================================
def set_input(pin):
    pins[pin] = ('in', None)
    GPIO.setup(pin, GPIO.IN)

#===============================================================================
# Fonction :    blink(pin, conn, delay)
# Description : Fait alterner une pin digitale 0-3.3V (pour tester).
#===============================================================================
def blink(pin, conn, delay=0.1):
    set_output(pin)
    while(True):
        set_low(pin)
        conn.send('On')
        sleep(delay)
        set_high(pin)
        conn.send('Off')
        sleep(delay)

#===============================================================================
# Fonction :    pulse(pin)
# Description : Genere une impulsion sur une pine digitale 0-3.3V (pour tester).
#===============================================================================
def pulse(pin):
    set_output(pin)
    set_low(pin)
    sleep(0.002)
    set_high(pin)
    sleep(0.002)
    set_low(pin)
    sleep(0.001)
    set_high(pin)

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

    # Blink
    blink_parent_conn, blink_child_conn = Pipe()
    blink_sub = Process(target=blink, args=('P9_11', blink_child_conn))
    blink_sub.start()
    msg('Sous-routine lancée : blink_sub', args)

    # Bumpers
    bumpers_parent_conn, bumpers_child_conn = Pipe()
    bumpers_sub = Process(target=bumpers.scan, args=(bumpers_child_conn, ))
    bumpers_sub.start()
    msg('Sous-routine lancée : bumpers_sub', args)

    # CMUCam2+
    cmucam_parent_conn, cmucam_child_conn = Pipe()
    cmucam_sub = Process(target=cmucam.cam, args=(cmucam_child_conn, ))
    cmucam_sub.start()
    msg('Sous-routine lancée : cmucam_sub', args)

#    sleep(3.0) # Attend avant de lire la couleur à tracker
    cmucam_parent_conn.send('track_mean')
    sleep(0.5)
    cmucam_parent_conn.send('track_on')

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

