#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep

# Librairies spéciales
#======================
import Adafruit_BBIO.ADC as ADC
from pins import get_adc

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def scan(conn, args, delay=0.01):

    ADC.setup()
    last_impact = (False, False, False, False)

    while True:

        reading = get_adc('P9_33')
        
        if reading > 767: 
            impact = (True, True, True, True)
        elif reading > 426:
            impact = (False, True, True, True)
        elif reading > 298:
            impact = (True, False, True, True)
        elif reading > 230:
            impact = (False, False, True, True)
        elif reading > 188:
            impact = (True, True, False, True)
        elif reading > 158:
            impact = (False, True, False, True)
        elif reading > 137:
            impact = (True, False, False, True)
        elif reading > 121:
            impact = (False, False, False, True)
        elif reading > 108:
            impact = (True, True, True, False)
        elif reading > 98:
            impact = (False, True, True, False)
        elif reading > 89:
            impact = (True, False, True, False)
        elif reading > 82:
            impact = (False, False, True, False)
        elif reading > 76:
            impact = (True, True, False, False)
        elif reading > 71:
            impact = (False, True, False, False)
        elif reading > 66:
            impact = (True, False, False, False)
        else:
            impact = (False, False, False, False)

        # Renvoie le nouvel état seulement s'il y a eu un changement, pour
        # éviter le SPAM.
        if impact != last_impact:
            last_impact = impact
            conn.send(impact)

        sleep(delay)

