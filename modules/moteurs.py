#!/root/marcus/bin/python
#-*- coding: utf-8 -*-

# Librairies spéciales
#======================
#from pins import *

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
    def __init__(self):
        set_output('P9_12')
        set_output('P9_13')
        set_output('P9_14')
        set_output('P9_15')
        set_output('P9_16')
        set_output('P9_21')

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
    def droit_arret(self):
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

    def gauche_arret(self):
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

