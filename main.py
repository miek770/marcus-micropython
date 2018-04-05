#-*- coding: utf-8 -*-

import argparse
import logging
import sys
from time import sleep
from multiprocessing import Process, Pipe

from machine import Pin
from comportements import memoire, collision, evasionbrusque
from comportements import evasiondouce, viser, approche, statisme
from comportements import exploration, agressif, paisible
from peripheriques import cmucam
from arbitres import moteurs, modes
import config

class Marcus:
    """Classe d'application générale. Comprend l'activation des sous-
    routines et des arbitres, ainsi que la boucle principale du robot.
    """

    def __init__(self, args):

        self.args = args

        # Initialisation du journal d'événements
        log_frmt = "%(asctime)s[%(levelname)s] %(message)s"
        date_frmt = "%Y-%m-%d %H:%M:%S "
        if self.args.verbose:
            log_lvl = logging.DEBUG
        else:
            log_lvl = logging.INFO

        logging.basicConfig(filename=self.args.logfile,
                            format=log_frmt,
                            datefmt=date_frmt,
                            level=log_lvl)

        logging.info("Logger initié : {}".format(self.args.logfile))
        logging.info("Programme lancé")

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
        if not self.args.nocam:
            self.cmucam_parent_conn, self.cmucam_child_conn = Pipe()
            self.cmucam_sub = Process(
                    target=cmucam.cam,
                    args=(self.cmucam_child_conn, self.args)
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
        if not self.args.nocam:
            self.arbitres[m.nom].active([
                (viser.Viser(nom="viser"), 3),
                (approche.Approche(nom="approche"), 4)
                ])

        # Arbitre modes
        if not self.args.nomode:
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
        if not self.args.nocam:
            self.cmucam_sub.terminate()
        sys.exit()

    def loop(self):
        """Boucle principale."""

        while True:
            sleep(config.periode)

            # Mise à jour de config.track
            if not self.args.nocam and self.cmucam_parent_conn.poll():
                try:
                    t = self.cmucam_parent_conn.recv()
                    if t is None:
                        self.quit()
                    config.track = t
                except EOFError:
                    logging.error("main > La sous-routine cmucam ne répond plus")
                    self.quit()

            # Arrêt du programme principal
            if self.args.stop:
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
            if not self.args.nomode:
                if not self.args.nocam and config.periode_change:
                    config.periode_change = False
                    msg = "periode={}".format(config.periode)
                    self.cmucam_parent_conn.send(msg)

def main():
    """Routine principale. Traitement des arguments et création de
    l'objet d'application général Marcus.
    """

    parser = argparse.ArgumentParser(description='Robot Marcus (BBB) - Michel')

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help="Augmente la verbosité du programme.")
    parser.add_argument('-l',
                        '--logfile',
                        action='store',
                        default=None,
                        help="Spécifie le chemin du journal d'événement.")
    parser.add_argument('-s',
                        '--stop',
                        action='store_true',
                        help="""Arrête l'exécution lorsqu'un impact est
                            détecté.""")
    parser.add_argument('--nocam',
                        action='store_true',
                        help="""Lance le programme sans la caméra et les
                            comportements qui en dépendent.""")
    parser.add_argument('--nomode',
                        action='store_true',
                        help="""Lance le programme sans l'arbitre de modes et
                            ses comportements.""")
    parser.add_argument('--scan',
                        action='store_true',
                        help="""Scanne la couleur devant la caméra au
                            démarrage. Sinon la dernière couleur sauvegardée
                            est chargée.""")

    marcus = Marcus(args=parser.parse_args())

    try:
        marcus.loop()

    # Lorsque CTRL-C est reçu...
    except KeyboardInterrupt:
        marcus.quit()

if __name__ == '__main__':
    main()
