#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies spéciales
#======================
from pins import set_output, set_low, set_high

# P9_12 - Direction moteur droit
# P9_13 - Direction moteur droit
# P9_14 - Enable moteur droit (PWM)
# P9_15 - Direction moteur gauche
# P9_16 - Enable moteur gauche (PWM)
# P9_21 - Direction moteur gauche

#===============================================================================
# Classe :      Moteurs
# Description : Wrapper pour gérer le contrôle des moteurs du robot
#===============================================================================
class Moteurs:

    # Initialisation
    #================
    def __init__(self, args):

        self.args = args

        set_output('P9_12', self.args)
        set_output('P9_13', self.args)
        set_output('P9_14', self.args)
        set_output('P9_15', self.args)
        set_output('P9_16', self.args)
        set_output('P9_21', self.args)

        self.etat = None

        self.arret()

    # Fonctions globales
    #====================
    def avance(self):
        self.droit_avance()
        self.gauche_avance()
        self.etat = 'av'

    def recule(self):
        self.droit_recule()
        self.gauche_recule()
        self.etat = 're'

    def freine(self):
        self.droit_freine()
        self.gauche_freine()
        self.etat = 'fr'

    def arret(self):
        self.droit_arret()
        self.gauche_arret()
        self.etat = 'ar'

    def tourne_droite(self):
        self.droit_recule()
        self.gauche_avance()
        self.etat = 'td'

    def tourne_gauche(self):
        self.droit_avance()
        self.gauche_recule()
        self.etat = 'tg'

    # Fonctions par moteur
    #======================
    def gauche_arret(self):
        set_low('P9_14', self.args) # Disable

    def gauche_freine(self):
        set_high('P9_12', self.args)
        set_high('P9_13', self.args)
        set_high('P9_14', self.args) # Enable

    def gauche_recule(self):
        set_low('P9_12', self.args)
        set_high('P9_13', self.args)
        set_high('P9_14', self.args) # Enable

    def gauche_avance(self):
        set_high('P9_12', self.args)
        set_low('P9_13', self.args)
        set_high('P9_14', self.args) # Enable

    def droit_arret(self):
        set_low('P9_16', self.args) # Disable

    def droit_freine(self):
        set_high('P9_15', self.args)
        set_high('P9_21', self.args)
        set_high('P9_16', self.args) # Enable

    def droit_recule(self):
        set_high('P9_15', self.args)
        set_low('P9_21', self.args)
        set_high('P9_16', self.args) # Enable

    def droit_avance(self):
        set_low('P9_15', self.args)
        set_high('P9_21', self.args)
        set_high('P9_16', self.args) # Enable

