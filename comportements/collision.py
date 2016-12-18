#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, randint, choice

# Librairies spéciales
#======================
from arbitre import Comportement
from modules.pins import get_input

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

# Constantes
#============
duree_rotation_min = 0.5 # en secondes

class Collision(Comportement):

    def decision(self):
        impact_av_dr = not get_input("P8_7")
        impact_av_ga = not get_input("P8_8")
        impact_ar_dr = not get_input("P8_9")
        impact_ar_ga = not get_input("P8_10")

        # Impact avant droit
        if impact_av_dr and not impact_av_ga:
            logging.info("Comportement {} : Impact avant droit, recule et tourne à gauche", self.nom)
            duree_rotation = duree_rotation_min + random()
            return [(0, 0, 0.2),
                    (-100, -100, 0.5),
                    (-100, 100, duree_rotation)]

        # Impact avant droit et gauche
        elif impact_av_dr and impact_av_ga:
            duree_rotation = duree_rotation_min + 2*random()
            tourne_gauche = choice((True, False))
            if tourne_gauche:
                logging.info("Comportement {} : Impact avant droit et gauche, recule et tourne à gauche", self.nom)
                return [(0, 0, 0.2),
                        (-100, -100, 0.5),
                        (-100, 100, duree_rotation)]
            else:
                logging.info("Comportement {} : Impact avant droit et gauche, recule et tourne à droite", self.nom)
                return [(0, 0, 0.2),
                        (-100, -100, 0.5),
                        (100, -100, duree_rotation)]

        # Impact avant gauche
        elif not impact_av_dr and impact_av_ga:
            logging.info("Comportement {} : Impact avant gauche, recule et tourne à droite", self.nom)
            duree_rotation = duree_rotation_min + random()
            return [(0, 0, 0.2),
                    (-100, -100, 0.5),
                    (100, -100, duree_rotation)]

        # Impact arrière
        elif impact_ar_dr or impact_ar_ga:
            logging.info("Comportement {} : Impact arrière, arrêt", self.nom)
            return [(0, 0, 0)]

        return None
