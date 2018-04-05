#-*- coding: utf-8 -*-

# Librairies standard
#=====================
import time, logging

# Librairies spéciales
#======================
from machine import Pin, PWM

class Moteurs:
    """Pilote d'opération des moteurs."""

    def __init__(self):

        self.en_droite = PWM(Pin(18), freq=50)
        self.en_droite.duty(0) # 0 à 1023

        self.av_droite = Pin(19, mode=Pin.OUT)
        self.av_droite.value(1)
        self.re_droite = Pin(21, mode=Pin.OUT)
        self.re_droite.value(1)

        self.en_gauche = PWM(Pin(5), freq=50)
        self.en_gauche.duty(0) # 0 à 1023

        self.av_gauche = Pin(17, mode=Pin.OUT)
        self.av_gauche.value(1)
        self.re_gauche = Pin(16, mode=Pin.OUT)
        self.re_gauche.value(1)

    def arret(self):
        """Cette méthode est appelée pour tous les arbitres à l'arrêt
        du programme générale dans main.py.
        """
        self.en_droite.duty(0) # 0 à 1023
        self.en_droite.deinit()

        self.en_gauche.duty(0) # 0 à 1023
        self.en_gauche.deinit()

    def execute(self, action):
        """Exécute l'action demandée (une étape de vecteur, sans
        considérer la durée) sur les 2 moteurs. Considère maintenant
        les PMW.
        """

        # Moteur gauche
        if action[0] < 0:
            self.av_gauche.value(0)
            self.re_gauche.value(1)
            self.en_gauche.duty(round(abs(action[1]*1023/100)))

        else:
            self.av_gauche.value(1)
            self.re_gauche.value(0)
            self.en_gauche.duty(round(action[1]*1023/100))

        # Moteur droit
        if action[1] < 0:
            self.av_droite.value(0)
            self.re_droite.value(1)
            self.en_droite.duty(round(abs(action[1]*1023/100)))

        else:
            self.av_droite.value(1)
            self.re_droite.value(0)
            self.en_droite.duty(round(action[1]*1023/100))

