#!/usr/bin/env python2
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
pins['P9_11'] = (None, None)
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

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def set_low(pin):
    if pins[pin][0] == 'out':
        GPIO.output(pin, GPIO.LOW)
    elif pins[pin][0] == 'in':
        print 'Erreur:', pin, 'est configurée en entrée.'
    else:
        print 'Erreur:', pin, 'n\'est pas configurée correctement.'

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def set_high(pin):
    if pins[pin][0] == 'out':
        GPIO.output(pin, GPIO.HIGH)
    elif pins[pin][0] == 'in':
        print 'Erreur:', pin, 'est configurée en entrée.'
    else:
        print 'Erreur:', pin, 'n\'est pas configurée correctement.'

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def set_output(pin):
    pins[pin] = ('out', 1)
    GPIO.setup(pin, GPIO.OUT)
    # Met la pin à 3.3V (high) par défaut
    set_high(pin)

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def set_input(pin):
    pins[pin] = ('in', None)
    GPIO.setup(pin, GPIO.IN)

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def blink(pin, conn, verbose, delay=1.0):
    set_output(pin)
    while(True):
        set_low(pin)
        conn.send('On')
        sleep(delay)
        set_high(pin)
        conn.send('Off')
        sleep(delay)

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def message(msg, args, lvl=logging.INFO):
    if args.verbose:
        print msg
    if args.logfile:
        logging.log(lvl, msg)

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
        message('Logger initié : ' + args.logfile, args)

    message('Programme lancé.', args)

    # Lancement des sous-routines (subprocesses)
    blink_parent_conn, blink_child_conn = Pipe()
    blink_sub = Process(target=blink,
                        args=('P9_11',
                              blink_child_conn,
                              args.verbose))
    blink_sub.start()
    message('Sous-routines lancées : sub_blink', args)

    # Boucle principale
    while(True):
        sleep(0.1)
        if blink_parent_conn.poll():
            message(blink_parent_conn.recv(), args)

    return 0

if __name__ == '__main__':
    main()

