#-*- coding: utf-8 -*-

import logging

class Comportement:

    def __init__(self, nom, priorite=None):

        self.nom = nom
        self.precedent = False
        self.priorite = priorite
        self.variables()
        logging.info("Comportement {} initialisé".format(self.nom))

    def evalue(self):
        action = self.decision()
        self.precedent = False
        return action

    def decision(self):
        """Processus décisionnel du comportement. À redéfinir
        absolument dans le comportement.
        """
        logging.debug("Comportement {} : Décision indéfinie".format(self.nom))
        return None

    def variables(self):
        """Par défaut ne fait rien. Redéfinir dans le comportement si
        requis.
        """
        pass
