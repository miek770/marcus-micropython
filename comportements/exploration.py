#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from itertools import islice
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

class Exploration(Comportement):
    """Comportement d'exploration, avec rotation aléatoire lorsqu'un
    certain nombre de cycles est passé sans autre vainqueur à
    l'arbitrage des moteurs.
    """

    def variables(self):

        self.duree_rotation_min = 0.5 # en secondes
        self.compteur_max = 50 # en cycles
        self.compteur = self.compteur_max

    def decision(self):

        # Pour éviter d'atteindre -infini
        if self.compteur > 0:
            self.compteur -= 1
            #logging.debug("Comportement {} : Compteur à {}".format(self.nom, self.compteur))

        # Si le compteur est écoulé...
        if self.compteur == 0:

            # Et qu'il n'y a eu que de l'exploration pendant ce temps...
            try:
                passe_max = list(islice(config.passe_moteurs, config.passe_moteurs.__len__()-self.compteur_max, config.passe_moteurs.__len__()))
            except ValueError:
                logging.error("Comportement {} : config.passe_moteurs = {}".format(self.nom, config.passe_moteurs))
                return None

            if all(x in (self.priorite, ) for x in passe_max):

                logging.info("Comportement {} : Trop tranquille".format(self.nom))
                self.compteur = self.compteur_max

                duree_rotation = self.duree_rotation_min + random()
                tourne_gauche = choice((True, False))

                if tourne_gauche:
                    return [(-100, 100, duree_rotation)]
                else:
                    return [(100, -100, duree_rotation)]

        # Sinon...
        return [(100, 100, 0)]

