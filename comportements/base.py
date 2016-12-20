#-*- coding: utf-8 -*-

import logging

class Comportement:

    def __init__(self, nom, priorite=None):

        self.nom = nom
        self.precedent = False
        self.priorite = priorite
        logging.info("Comportement {} initialisé".format(self.nom))

    def evalue(self):
        action = self.decision()
        self.precedent = False
        return action

    def decision(self):
        logging.debug("Comportement {} : Décision indéfinie".format(self.nom))
        return None

