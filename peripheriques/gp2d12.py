# -*- coding: utf-8 -*-

from time import sleep

import Adafruit_BBIO.ADC as ADC

from pins import get_adc

ADC.setup()

def get_dist(pin):
    """Retourne la distance en centimetres. La formule a ete calculee
       a partir de la fiche technique du manufacturier et de calculs
       manuels pour trouver une courbe qui se rapproche des donnees.

       L'ecart moyen est de -0,3% dans mes calculs, soit certainement
       inferieur a la precision du GP2D12.

       L'equation calculee est : y = 8,2/x + 0,04
       Ou x = distance en centimetres
          y = lecture analogique (de 0,00 a 1,00)
       """

    d = abs(8.20/(get_adc(pin) - 0.04))
    if d > 80:
        return 100
    elif d < 10:
        return 0
    return d
