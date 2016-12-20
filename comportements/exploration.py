#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, choice

# Librairies spéciales
#======================
from base import Comportement
import config

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

# Variables
#===========
duree_rotation_min = 0.5 # en secondes
compteur_max = 50 # en cycles
compteur = compteur_max

class Exploration(Comportement):

    def decision(self):

        # Pour éviter d'atteindre -infini
        if compteur > 0:
            compteur -= 1

        # Si le compteur est écoulé...
        if compteur == 0:

            # Et qu'il n'y a eu que de l'exploration pendant ce temps...
            if all(x in self.priorite for x in config.passe_moteurs):

                logging.info("Comportement {} : Trop tranquille".format(self.nom))
                compteur = compteur_max

                duree_rotation = duree_rotation_min + random()
                tourne_gauche = choice((True, False))

                if tourne_gauche:
                    return [(-100, 100, duree_rotation)]
                else:
                    return [(100, -100, duree_rotation)]

        # Sinon...
        return [(100, 100, 0)]

