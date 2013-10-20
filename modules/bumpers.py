#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
from time import sleep

# Librairies spéciales
#======================
import Adafruit_BBIO.ADC as ADC

# La fonction ADC.read(pin) renvoie une valeur de 0 à 1. Les pins suivantes
# peuvent être utiliées :

# P9_33
# P9_35
# P9_36
# P9_37
# P9_38
# P9_39
# P9_40

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def get_adc(pin):
    # Selon la documentation de Adafruit_BBIO.ADC, il faut lire la valeur deux
    # fois pour avoir le bon résultat. Ils disent que c'est un bug dans le
    # pilote ADC, donc ce sera possiblement corrigé dans le futur (quoiqu'il
    # n'y a pas vraiment d'impact pour nous).
    ADC.read(pin)
    reading = ADC.read(pin)
    return reading

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def scan(conn, delay=0.01):

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

#===============================================================================
# Fonction :
# Description :
#===============================================================================
def main():
    ADC.setup()
    print ADC.read('P9_33')

if __name__ == '__main__':
    main()
