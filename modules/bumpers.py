#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep

# Librairies spéciales
#======================
from pins import set_input, get_input

#===============================================================================
# Fonction :    scan(conn, args, delay)
# Description :
#===============================================================================
def scan(conn, args, delay=0.01):

    last_impact = (False, False, False, False)

    set_input('P8_7', args) # Avant droit
    set_input('P8_8', args) # Avant gauche
    set_input('P8_9', args) # Arrière droit
    set_input('P8_10', args) # Arrière gauche

    while True:

        impact = (get_input('P8_7', args),
                  get_input('P8_8', args),
                  get_input('P8_9', args),
                  get_input('P8_10', args))

        # Renvoie le nouvel état seulement s'il y a eu un changement, pour
        # éviter le SPAM.
        if impact != last_impact:
            last_impact = impact
            conn.send(impact)

        sleep(delay)

