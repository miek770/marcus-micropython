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

class Viser(Comportement):
    """Comportement qui vise la cible lorsqu'elle est repérée par la
    caméra. Le résultat du tracking est mis à jour dans la variable
    globale config.track via une sous-routine parallèle au programme
    général.
    
    Le dictionnaire config.track contient les éléments suivants :
    mx my x1 y1 x2 y2 pixels confidence timestamp
    """

    def variables(self):

        self.seuil_mx = 5 # Seuil d'alignement sur mx, en pixels
        self.seuil_conf = 10 # Seuil de détection (10 est peut-être trop sensible)
        self.centre_x = 50 # Centre de la fenêtre de détection, en pixels
        self.derniere_lecture = None

    def decision(self):

        try:
            if int(config.track["confidence"]) < self.seuil_conf:
                return None

            elif (self.derniere_lecture is not None
                    or self.derniere_lecture != config.track["timestamp"]):

                # Mise à jour du dernier timestamp reçu
                self.derniere_lecture = config.track["timestamp"]

                if config.track["mx"] < (self.centre_x - self.seuil_mx):
                    logging.debug("Cible à gauche, tourne à gauche")
                    return [(-30, 30, 0)]

                elif config.track["mx"] > (self.centre_x + self.seuil_mx):
                    logging.debug("Cibre à droite, tourne à droite")
                    return [(30, -30, 0)]

                return None

            return None

        except KeyError:
            logging.error("""Comportement {0} : config.track est vide
                          {1}""".format(self.nom, config.track))
            return None
