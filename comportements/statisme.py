#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, choice
from collections import deque

# Librairies spéciales
#======================
import config
from base import Comportement
from peripheriques.pins import get_input
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

class Statisme(Comportement):
    """Ce comportement sert à détection une absence de changement dans
    les capteurs qui pourrait indiquer que le robot est coincé quelque
    part sans s'en rendre compte. Dans ce cas, l'action à prendre est
    probablement de reculer pour se déloger, puis de tourner.
    """

    def variables(self):

        self.duree_min_recul = 1 # en seconde
        self.duree_min_rotation = 0.5 # en seconde

        self.passe = dict()
        self.memoire = 30 # en cycles
        self.passe["pare_chocs"] = (None, deque(maxlen=memoire))
        self.passe["camera"] = (None, deque(maxlen=memoire))
        self.passe["gp2d12"] = (None, deque(maxlen=memoire))
        #self.passe["boucliers"] = deque(maxlen=memoire)

    def decision(self):

        actuel = (not get_input("P8_7"), not get_input("P8_8"), not get_input("P8_9"), not get_input("P8_10"))
        self.passe["pare_chocs"][0] = actuel
        self.passe["pare_chocs"][1].append(actuel)

        actuel = config.track
        self.passe["camera"][0] = actuel
        self.passe["camera"][1].append(actuel)

        actuel = (get_dist("AIN0"), get_dist("AIN1"), get_dist("AIN2"))
        self.passe["gp2d12"][0] = actuel
        self.passe["gp2d12"][1].append(actuel)

        statisme = True
        for key in self.passe.keys():
            if not all(x == self.passe[key][0] for x in self.passe[key][1]):
                statisme = False
                break

        if statisme:
            logging.info("Comportement {} : Aucune variation de capteurs en {} cycles".format(self.nom, self.memoire))
            duree_recul = self.duree_min_recul + random()
            duree_rotation = self.duree_min_rotation + random()
            tourne_gauche = choice(True, False)
            
            if tourne_gauche:
                return [(-100, -100, duree_recul),
                        (-100, 100, duree_rotation)]
            else:
                return [(-100, -100, duree_recul),
                        (100, -100, duree_rotation)]

        return None
