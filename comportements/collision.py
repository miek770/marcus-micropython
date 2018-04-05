#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, randint, choice

# Librairies spéciales
#======================
from comportements.base import Comportement
from machine import Pin

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

class Collision(Comportement):
    """Comportement qui gère les collisions du robot détectés par les
    pare-chocs.
    """

    def variables(self):

        self.duree_rotation_min = 0.5 # en secondes

    def decision(self):

        impact_av_dr = self.bmpr_avant_droite.value()
        impact_av_ga = self.bmpr_avant_gauche.value() 
        impact_ar_dr = self.bmpr_arrie_droite.value()
        impact_ar_ga = self.bmpr_arrie_gauche.value()

        # Impact avant droit
        if impact_av_dr and not impact_av_ga:
            logging.info("Comportement {} : Impact avant droit, recule et tourne à gauche".format(self.nom))
            duree_rotation = self.duree_rotation_min + random()/2
            return [(0, 0, 0.2),
                    (-100, -100, 0.5),
                    (-100, 100, duree_rotation)]

        # Impact avant droit et gauche
        elif impact_av_dr and impact_av_ga:
            duree_rotation = self.duree_rotation_min + random()
            tourne_gauche = choice((True, False))
            if tourne_gauche:
                logging.info("Comportement {} : Impact avant droit et gauche, recule et tourne à gauche".format(self.nom))
                return [(0, 0, 0.2),
                        (-100, -100, 0.5),
                        (-100, 100, duree_rotation)]
            else:
                logging.info("Comportement {} : Impact avant droit et gauche, recule et tourne à droite".format(self.nom))
                return [(0, 0, 0.2),
                        (-100, -100, 0.5),
                        (100, -100, duree_rotation)]

        # Impact avant gauche
        elif not impact_av_dr and impact_av_ga:
            logging.info("Comportement {} : Impact avant gauche, recule et tourne à droite".format(self.nom))
            duree_rotation = self.duree_rotation_min + random()/2
            return [(0, 0, 0.2),
                    (-100, -100, 0.5),
                    (100, -100, duree_rotation)]

        # Impact arrière
        elif impact_ar_dr or impact_ar_ga:
            logging.info("Comportement {} : Impact arrière, arrêt".format(self.nom))
            return [(0, 0, 0)]

        return None

    def variables(self):
        self.bmpr_avant_droite = Pin(
                25,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)
        self.bmpr_avant_gauche = Pin(
                26,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)
        self.bmpr_arrie_droite = Pin(
                27,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)
        self.bmpr_arrie_gauche = Pin(
                14,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)

