# -*- coding: utf-8 -*-

from peripheriques import cmucam
from mock import patch
import argparse, logging, sys

def main():
    testargs = ["verbose"]
    with patch.object(sys, 'argv', testargs):

        parser = argparse.ArgumentParser()
        parser.add_argument('--scan',
                            action='store_true',
                            help="""Scanne la couleur devant la caméra au
                            démarrage. Sinon la dernière couleur sauvegardée
                            est chargée.""")
        parser.add_argument('-v',
                            '--verbose',
                            action='store_true',
                            help="Augmente la verbosité du programme.")
        parser.add_argument('-l',
                            '--logfile',
                            action='store',
                            default=None,
                            help="Spécifie le chemin du journal d'événement.")
        args = parser.parse_args()

    # Initialisation du journal d'événements
    log_frmt = "%(asctime)s[%(levelname)s] %(message)s"
    date_frmt = "%Y-%m-%d %H:%M:%S "
    if args.verbose:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.INFO

    logging.basicConfig(filename=args.logfile,
                        format=log_frmt,
                        datefmt=date_frmt,
                        level=log_lvl)

    logging.info("Logger initié : {}".format(args.logfile))

    c = cmucam.Cmucam(args)
    c.test("mx")

if __name__ == '__main__':
    main()
