#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random

# Librairies spéciales
#======================
from comportements.base import Comportement
from peripheriques.gp2d12 import get_dist

# Vecteur moteur
#================
"""Le comportement doit retourner un vecteur (une liste) décrivant les
actions à prendre par le moteur. La liste est une série de tuples avec
la vitesse du moteur droit, la vitesse du moteur gauche et la durée de
l'événement.

Le module de moteurs doit ensuite interpréter cette commande et la
traduire en consigne de moteurs.

Une nouvelle commande doit interrompre une manoeuvre en cours.

[(vitesse_gauche, vitesse_droite, duree), ...]
"""

class EvasionDouce(Comportement):

    def variables(self):
        self.rf_avant_centre = GP2D12(32)
        self.rf_avant_gauche = GP2D12(35)
        self.rf_avant_droite = GP2D12(34)

        self.seuil = 80 # En cm

    def decision(self):
        av_ga = self.rf_avant_gauche.get_dist()
        av_dr = self.rf_avant_droite.get_dist()

        # Obstacle à gauche mais pas à droite
        if av_ga < self.seuil and av_dr > self.seuil:

            logging.info("Comportement {} : Obstacle à gauche, évite à droite".format(self.nom))
            return [(100, av_ga, 0)]

        # Obstacle à droite mais pas à gauche
        if av_dr < self.seuil and av_ga > self.seuil:

            logging.info("Comportement {} : Obstacle à droite, évite à droite".format(self.nom))
            return [(av_dr, 100, 0)]

        return None
