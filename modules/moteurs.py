#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies spéciales
#======================
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

# Dictionnaire de pins digitales
#================================

# pins[index] = in/out

pins = dict()
pins['P9_12'] = None # Direction moteur droit
pins['P9_13'] = None # Direction moteur droit
pins['P9_14'] = None # Enable moteur droit (PWM)
pins['P9_15'] = None # Direction moteur gauche
pins['P9_16'] = None # Enable moteur gauche (PWM)
pins['P9_21'] = None # Direction moteur gauche

# Fonctions simplifiées de contrôle de pins numériques
#======================================================

def set_low(pin):
    if pins[pin] == 'out':
        GPIO.output(pin, GPIO.LOW)

def set_high(pin):
    if pins[pin] == 'out':
        GPIO.output(pin, GPIO.HIGH)

def set_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    pins[pin] = 'out'
    set_high(pin)

def set_input(pin):
    GPIO.setup(pin, GPIO.IN)
    pins[pin] = 'in'

#===============================================================================
# Classe :      Moteurs
# Description : Wrapper pour gérer le contrôle des moteurs du robot
#===============================================================================
class Moteurs:

    # Initialisation
    #================
    def __init__(self):
        set_output('P9_12')
        set_output('P9_13')
        set_output('P9_14')
        set_output('P9_15')
        set_output('P9_16')
        set_output('P9_21')

        self.stop()

    # Fonctions globales
    #====================
    def avance(self):
        self.droit_avance()
        self.gauche_avance()

    def recule(self):
        self.droit_recule()
        self.gauche_recule()

    def freine(self):
        self.droit_freine()
        self.gauche_freine()

    def stop(self):
        self.droit_stop()
        self.gauche_freine()

    def tourne_droite(self):
        self.droit_recule()
        self.gauche_avance()

    def tourne_gauche(self):
        self.droit_avance()
        self.gauche_recule()

    # Fonctions par moteur
    #======================
    def droit_stop(self):
        set_low('P9_14') # Disable

    def droit_freine(self):
        set_high('P9_12')
        set_high('P9_13')
        set_high('P9_14') # Enable

    def droit_avance(self):
        set_low('P9_12')
        set_high('P9_13')
        set_high('P9_14') # Enable

    def droit_recule(self):
        set_high('P9_12')
        set_low('P9_13')
        set_high('P9_14') # Enable

    def gauche_stop(self):
        set_low('P9_16') # Disable

    def gauche_freine(self):
        set_high('P9_15')
        set_high('P9_21')
        set_high('P9_16') # Enable

    def gauche_avance(self):
        set_high('P9_15')
        set_low('P9_21')
        set_high('P9_16') # Enable

    def gauche_recule(self):
        set_low('P9_15')
        set_high('P9_21')
        set_high('P9_16') # Enable

