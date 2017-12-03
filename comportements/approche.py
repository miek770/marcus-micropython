# -*- coding: utf-8 -*-

import logging

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

class Approche(Comportement):
    """Comportement qui se rapproche de la cible lorsqu'elle est
    repérée par la caméra. Le résultat du tracking est mis à jour dans
    la variable globale config.track via une sous-routine parallèle au
    programme général.

    Pour l'instant le comportement peut aussi éloigner le robot s'il
    trouve qu'il est trop prêt de sa cible. À tester et revalider.
    
    Le dictionnaire config.track contient les éléments suivants :
    mx my x1 y1 x2 y2 pixels confidence timestamp
    """

    def variables(self):

        self.seuil_conf = 10 # Seuil de détection (10 est peut-être trop sensible)
        self.cible_pixels = 50 # Nombre de pixels désirés (à ajuster, pas testé)
        self.ecart_pixels = 10 # Écart acceptable, à ajuster
        self.derniere_lecture = None

    def decision(self):

        try:
            if int(config.track["confidence"]) < self.seuil_conf:
                return None

            elif (self.derniere_lecture is None or self.derniere_lecture != config.track["timestamp"]):

                # Mise à jour du dernier timestamp reçu
                self.derniere_lecture = config.track["timestamp"]

                if int(config.track["pixels"]) < (self.cible_pixels - self.ecart_pixels):
                    logging.info("Cible trop loin, on s'approche")
                    return [(50, 50, 0)]

                elif int(config.track["pixels"]) > (self.cible_pixels + self.ecart_pixels):
                    logging.info("Cible trop proche, on s'éloigne")
                    return [(-50, -50, 0)]

            return None

        except KeyError:
            logging.debug("Comportement {} : config.track est vide".format(self.nom))
            return None
