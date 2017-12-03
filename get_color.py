# -*- coding: utf-8 -*-

from peripheriques import cmucam
#from mock import patch
import argparse

def main():
#    testargs = ["scan"]
#    with patch.object(sys, 'argv', testargs):

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
    if self.args.verbose:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.INFO

    logging.basicConfig(filename=self.args.logfile,
                        format=log_frmt,
                        datefmt=date_frmt,
                        level=log_lvl)

    logging.info("Logger initié : {}".format(self.args.logfile))

    c = cmucam.Cmucam(args)

if __name__ == '__main__':
    main()
