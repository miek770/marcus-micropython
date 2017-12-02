#-*- coding: utf-8 -*-

import logging

from comportements.base import Comportement

class Arbitre:

    def __init__(self, nom):

        self.nom = nom
        self.comportements = list()
        self.precedent = None
        logging.info("Arbitre {} initialisé".format(self.nom))

    def arret(self):
        pass

    def active(self, comportements):

        for comportement, priorite in comportements:

            if not isinstance(comportement, Comportement):
                raise TypeError

            if not isinstance(priorite, int):
                raise TypeError

            if any(priorite in c for c in self.comportements):
                logging.error("""Priorité {} déjà réservée, comportement {}
                              ignoré""".format(priorite, comportement.nom))
            else:
                logging.info("""Activation du comportement {}""".format(comportement.nom))
                self.comportements.append((comportement, priorite))
                self.comportements = sorted(self.comportements,
                                            key=lambda x: x[1])

    def evalue(self):

        for i in range(len(self.comportements)):

            action = self.comportements[i][0].evalue()

            if action is not None:

                logging.debug("Comportement {} : {}".format(self.comportements[i][0].nom, action))
                # On avise le comportement gagnant pour qu'il puisse en
                # tenir compte lors de la prochaine itération.
                self.comportements[i][0].precedent = True
                self.precedent = i
                eval(action)
                break

            else:
                logging.debug("Comportement {} : Aucune action".format(self.comportements[i][0].nom))

def main():
    log_frmt = '%(asctime)s[%(levelname)s] %(message)s'
    date_frmt = '%Y-%m-%d %H:%M:%S '
    log_lvl = logging.DEBUG
    logging.basicConfig(format=log_frmt, datefmt=date_frmt, level=log_lvl)

    a = Arbitre("Test")
    a.active(Comportement("Évasion"), 4)
    a.active(Comportement("Collision"), 1)
    a.active(Comportement("Exploration"), 99)
    a.active(Comportement("Didelidou"), 4)
    a.evalue()

    class Ctest(Comportement):

        def decision(self):
            return 'logging.debug("Patate!")'

    a.active(Ctest("Test de patate"), 6)
    a.evalue()

if __name__ == '__main__':
    main()

