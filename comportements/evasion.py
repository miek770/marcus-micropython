#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, randint, choice

# Librairies spéciales
#======================
from arbitre import Comportement
from modules import gp2d12

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
seuil_avant = 45 # Seuil de détection, en cm
seuil_cote = 20 # Seuil de détection, en cm
duree_rotation_min = 1 # en s

class Evasion(Comportement):

    def decision(self):
        av_mi = gp2d12.get_dist('AIN0') # Avant milieu
        av_ga = gp2d12.get_dist('AIN1') # Avant gauche
        av_dr = gp2d12.get_dist('AIN2') # Avant droit

        # Obstacle à gauche (pas à droite)
        if av_ga <= seuil_cote and av_dr > seuil_cote:

            # Obstacle devant aussi (tourne plus longtemps)
            if av_mi <= seuil_avant:
                logging.info("Comportement {} : Obstacle devant et à gauche, tourne à droite".format(self.nom))
                duree_rotation = duree_rotation_min + 2*random()

            # Sinon (gauche seulement)
            else:
                logging.info("Comportement {} : Obstacle à gauche, tourne à droite".format(self.nom))
                duree_rotation = duree_rotation_min + random()

            return [(100, -100, duree_rotation)]

        # Obstacle à droite (pas à gauche)
        elif av_dr <= seuil_cote and av_ga > seuil_cote:

            # Obstacle devant aussi (tourne plus longtemps)
            if av_mi <= seuil_avant:
                logging.info("Comportement {} : Obstacle devant et à droite, tourne à gauche".format(self.nom))
                duree_rotation = duree_rotation_min + 2*random()

            # Sinon (droite seulement)
            else:
                logging.info("Comportement {} : Obstacle à droite, tourne à gauche".format(self.nom))
                duree_rotation = duree_rotation_min + random()

            return [(100, -100, duree_rotation)]

        # Obstacle à gauche et à droite
        elif av_ga <= seuil_cote and av_dr <= seuil_cote:

            duree_rotation = duree_rotation_min + 2*random()
            tourne_gauche = choice((True, False))

            if tourne_gauche:
                logging.info("Comportement {} : Obstacle à gauche et à droite, tourne à gauche".format(self.nom))
                return [(-100, 100, duree_rotation)]
            else:
                logging.info("Comportement {} : Obstacle à gauche et à droite, tourne à droite".format(self.nom))
                return [(100, -100, duree_rotation)]

        # Obstacle devant seulement
        elif av_mi <= seuil_avant:
            duree_rotation = duree_rotation_min + random()
            tourne_gauche = choice((True, False))

            if tourne_gauche:
                logging.info("Comportement {} : Obstacle devant, tourne à gauche".format(self.nom))
                return [(-100, 100, duree_rotation)]
            else:
                logging.info("Comportement {} : Obstacle devant, tourne à droite".format(self.nom))
                return [(100, -100, duree_rotation)]

        return None
