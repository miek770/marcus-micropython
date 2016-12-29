#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, choice
from itertools import islice

# Librairies spéciales
#======================
import config
from base import Comportement

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

class Statisme(Comportement):
    """Ce comportement sert à détection une absence de changement dans
    les capteurs qui pourrait indiquer que le robot est coincé quelque
    part sans s'en rendre compte. Dans ce cas, l'action à prendre est
    probablement de reculer pour se déloger, puis de tourner.

    Le comportement dépend du comportement mémoire, qui enregistre
    l'état des capteurs dans le module config.
    """

    def variables(self):

        self.duree_min_recul = 1 # en seconde
        self.duree_min_rotation = 0.5 # en seconde
        self.memoire = 30 # en cycles

    def decision(self):

        statisme = True
        for key in config.passe_capteurs.keys():

            # Pas encore assez de cycles pour détecter du statisme
            if len(config.passe_capteurs[key]) < self.memoire:
                statisme = False
                break

            passe_max = list(islice(config.passe_capteurs[key], len(config.passe_capteurs[key])-self.memoire, len(config.passe_capteurs[key])))
            logging.debug("Comportement {} : passe_max[{}] = {}".format(self.nom, key, passe_max))
            if not all(x == passe_max[0] for x in passe_max):
                statisme = False
                break

        if statisme:
            logging.info("Comportement {} : Aucune variation de capteurs en {} cycles".format(self.nom, self.memoire))
            duree_recul = self.duree_min_recul + random()
            duree_rotation = self.duree_min_rotation + random()
            tourne_gauche = choice((True, False))
            
            if tourne_gauche:
                return [(-100, -100, duree_recul),
                        (-100, 100, duree_rotation)]
            else:
                return [(-100, -100, duree_recul),
                        (100, -100, duree_rotation)]

        return None
