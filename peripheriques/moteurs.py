#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
import time, logging

# Librairies spéciales
#======================
from pins import set_pwm, reset_pwm, set_duty_cycle, set_output, set_low, set_high

class Moteurs:
    """Pilote d'opération des moteurs.

    P9_12 - Direction moteur droit
    P9_13 - Direction moteur droit
    P9_14 - Enable moteur droit (PWM)
    P9_15 - Direction moteur gauche
    P9_16 - Enable moteur gauche (PWM)
    P9_21 - Direction moteur gauche
    """

    def __init__(self):

        set_output('P9_12')
        set_output('P9_13')
        set_pwm('P9_14')
        set_output('P9_15')
        set_pwm('P9_16')
        set_output('P9_21')

        self.droit_arret()
        self.gauche_arret()

    def arret(self):
        """Cette méthode est appelée pour tous les arbitres à l'arrêt du
        programme générale dans main.py.
        """
        self.droit_arret()
        self.gauche_arret()
        reset_pwm("P9_14")
        reset_pwm("P9_16")

    def execute(self, action):
        """Exécute l'action demandée (une étape de vecteur, sans
        considérer la durée) sur les 2 moteurs. Considère maintenant
        les PMW.
        """

        # Moteur gauche
        if action[0] < 0:
            set_low('P9_12')
            set_high('P9_13')
            set_duty_cycle('P9_14', abs(action[0]))
        else:
            # Si le duty cycle est égal à 0 le moteur arrête
            set_high('P9_12')
            set_low('P9_13')
            set_duty_cycle('P9_14', action[0])

        # Moteur droit
        if action[1] < 0:
            set_low('P9_21')
            set_high('P9_15')
            set_duty_cycle("P9_16", abs(action[1]))
        else:
            # Si le duty cycle est égal à 0 le moteur arrête
            set_high('P9_21')
            set_low('P9_15')
            set_duty_cycle("P9_16", action[1])

    # Fonctions par moteur
    #======================

    def gauche_arret(self):
        set_duty_cycle('P9_14', 0) # Disable

    def gauche_freine(self):
        set_high('P9_12')
        set_high('P9_13')
        set_duty_cycle("P9_14", 100) # Enable

    def gauche_recule(self):
        set_low('P9_12')
        set_high('P9_13')
        set_duty_cycle("P9_14", 100) # Enable

    def gauche_avance(self):
        set_high('P9_12')
        set_low('P9_13')
        set_duty_cycle("P9_14", 100) # Enable

    def droit_arret(self):
        set_duty_cycle("P9_16", 0) # Disable

    def droit_freine(self):
        set_high('P9_15')
        set_high('P9_21')
        set_duty_cycle("P9_16", 100) # Enable

    def droit_recule(self):
        set_high('P9_15')
        set_low('P9_21')
        set_duty_cycle("P9_16", 100) # Enable

    def droit_avance(self):
        set_low('P9_15')
        set_high('P9_21')
        set_duty_cycle("P9_16", 100) # Enable

