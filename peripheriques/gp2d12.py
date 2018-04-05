# -*- coding: utf-8 -*-

from time import sleep
from machine import ADC, Pin

class GP2D12:
    def __init__(self, pin):
        self.pin = Pin(pin)
        self.adc = ADC(self.pin)
        self.adc.atten(self.adc.ATTN_6DB)

    def get_dist(self):
        """Retourne la distance en centimètres. La formule a été
        calculée a partir de mesures manuelles et d'interpolation
        polynomiale avec numpy.
        """

        x = self.adc.read()
        d = -1.525*10**-8*x**3+8.809*10**-5*x**2-0.1596*x+112.6
        if d > 90:
            return 100
        elif d < 25:
            return 0
        return d

