#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
import time, logging

# Librairies spéciales
#======================
from base import Arbitre
import config

class Modes(Arbitre):
    """Arbitre du contrôle de mode.
    """

    def __init__(self, nom="modes"):

        self.nom = nom
        self.comportements = list()
        self.precedent = None
        logging.info("Arbitre {} initialisé".format(self.nom))

    def evalue(self):
        """Méthode appelée par la boucle principale dans main.py pour
        demander à l'arbitre d'interroger chacun de ses comportements
        et de rendre une décision.
        """

        for i in range(len(self.comportements)):
            action = self.comportements[i][0].evalue()

            # S'il y a une action à prendre... 
            if action is not None:

                logging.debug("Comportement {} : {}".format(self.comportements[i][0].nom, action))

                # On avise le comportement gagnant pour qu'il puisse en
                # tenir compte lors de la prochaine itération
                self.comportements[i][0].precedent = True
                self.precedent = self.comportements[i][1]

                config.periode = action
                config.periode_change = True
                break

            # S'il n'y a pas d'action à prendre...
            else:
                #logging.debug("Comportement {} : Aucune action".format(self.comportements[i][0].nom))
                pass
