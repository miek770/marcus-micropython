#-*- coding: utf-8 -*-

import logging
import sys
from time import sleep
from multiprocessing import Process, Pipe

import config
from machine import Pin
from comportements import memoire, collision, evasionbrusque
from comportements import evasiondouce, viser, approche, statisme
from comportements import exploration, agressif, paisible
if not config.NO_CAM:
    from peripheriques import cmucam
from arbitres import moteurs, modes

class Marcus:
    """Classe d'application générale. Comprend l'activation des sous-
    routines et des arbitres, ainsi que la boucle principale du robot.
    """

    def __init__(self):

        # Initialisation du journal d'événements
        if config.VERBOSE:
            log_lvl = logging.DEBUG
        else:
            log_lvl = logging.INFO
        logging.basicConfig(level=log_lvl)
        logging.info("Logger initié")

        # Initialisation des pare-chocs
        self.bmpr_avant_droite = Pin(
                25,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)
        self.bmpr_avant_gauche = Pin(
                26,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)
        self.bmpr_arrie_droite = Pin(
                27,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)
        self.bmpr_arrie_gauche = Pin(
                14,
                mode=Pin.IN,
                pull=Pin.PULL_DOWN)

        # Initialisation de la CMUCam2+
        if not config.NO_CAM:
            self.cmucam_parent_conn, self.cmucam_child_conn = Pipe()
            self.cmucam_sub = Process(
                    target=cmucam.cam,
                    args=(self.cmucam_child_conn)
                    )
            self.cmucam_sub.start()
            message = self.cmucam_parent_conn.recv()

            if message:
                logging.info("Sous-routine lancée : cmucam_sub")

        # Initialisation des arbitres
        self.arbitres = dict()

        # Arbitre moteurs
        m = moteurs.Moteurs()
        self.arbitres[m.nom] = m

        self.arbitres[m.nom].active([
            (memoire.Memoire(nom="memoire"), 1),
            (collision.Collision(nom="collision"), 2),
            (evasiondouce.EvasionDouce(nom="evasion douce"), 5),
            (evasionbrusque.EvasionBrusque(nom="evasion brusque"), 6),
            (statisme.Statisme(nom="statisme"), 8),
            (exploration.Exploration(nom="exploration", priorite=9), 9)
            ])
        if not config.NO_CAM:
            self.arbitres[m.nom].active([
                (viser.Viser(nom="viser"), 3),
                (approche.Approche(nom="approche"), 4)
                ])

        # Arbitre modes
        if not config.NO_MODE:
            m = modes.Modes()
            self.arbitres[m.nom] = m
            self.arbitres[m.nom].active([
                (agressif.Agressif(nom="agressif"), 1),
                (paisible.Paisible(nom="paisible"), 9)
                ])

    def quit(self):
        """Arrêt du programme complet."""

        logging.info("Arrêt du programme.")
        for key in self.arbitres.keys():
            self.arbitres[key].arret()
        if not config.NO_CAM:
            self.cmucam_sub.terminate()
        sys.exit()

    def loop(self):
        """Boucle principale."""

        while True:
            sleep(config.periode)

            # Mise à jour de config.track
            if not config.NO_CAM and self.cmucam_parent_conn.poll():
                try:
                    t = self.cmucam_parent_conn.recv()
                    if t is None:
                        self.quit()
                    config.track = t
                except EOFError:
                    logging.error("main > La sous-routine cmucam ne répond plus")
                    self.quit()

            # Arrêt du programme principal
            if config.STOP:
                if (self.bmpr_avant_droite.value()
                    or self.bmpr_avant_gauche.value()
                    or self.bmpr_arrie_droite.value()
                    or self.bmpr_arrie_gauche.value()
                    ):

                    self.quit()

            # Interrogation des arbitres
            for key in self.arbitres.keys():
                self.arbitres[key].evalue()

            # Mise à jour de la période
            if not config.NO_MODE:
                if not config.NO_CAM and config.periode_change:
                    config.periode_change = False
                    msg = "periode={}".format(config.periode)
                    self.cmucam_parent_conn.send(msg)

def main():
    marcus = Marcus()
    try:
        marcus.loop()

    # Lorsque CTRL-C est reçu...
    except KeyboardInterrupt:
        marcus.quit()

if __name__ == '__main__':
    main()
