# -*- coding: utf-8 -*-

# Librairies standards
#======================
import argparse, logging, sys
from time import sleep
from multiprocessing import Process, Pipe

# Librairies spéciales
#======================
from peripheriques.pins import set_input, get_input
from comportements import collision, evasion, viser, approche, statisme, exploration
from peripheriques import cmucam
from arbitres import moteurs
import config

class Marcus:
    """Classe d'application générale. Comprend l'activation des sous-
    routines et des arbitres, ainsi que la boucle principale du
    robot.
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
        set_input('P8_7') # Avant droit
        set_input('P8_8') # Avant gauche
        set_input('P8_9') # Arrière droit
        set_input('P8_10') # Arrière gauche

        # Initialisation de la CMUCam2+
        if not self.args.nocam:
            self.cmucam_parent_conn, self.cmucam_child_conn = Pipe()
            self.cmucam_sub = Process(target=cmucam.cam, args=(self.cmucam_child_conn, self.args))
            self.cmucam_sub.start()
            message = self.cmucam_parent_conn.recv()

            if message:
                logging.info("Sous-routine lancée : cmucam_sub")

        # Initialisation des arbitres
        self.arbitres = dict()

        # Arbitre moteurs
        m = moteurs.Moteurs()
        self.arbitres[m.nom] = m
        self.arbitres[m.nom].active(collision.Collision(nom="collision"), 2)
        self.arbitres[m.nom].active(evasion.Evasion(nom="evasion"), 5)
        if not self.args.nocam:
            self.arbitres[m.nom].active(viser.Viser(nom="viser"), 4)
            self.arbitres[m.nom].active(approche.Approche(nom="approche"), 6)
            #self.arbitres[m.nom].active(statisme.Statisme(nom="statisme"), 8)
        self.arbitres[m.nom].active(exploration.Exploration(nom="exploration", priorite=9), 9)
        #self.arbitres[m.nom].active(.(nom=""), )

    # Arrêt
    #=======
    def quit(self):
        logging.info("Arrêt du programme.")
        for key in self.arbitres.keys():
            self.arbitres[key].arret()
        self.cmucam_sub.terminate()
        sys.exit()

    # Boucle principale
    #===================
    def loop(self):

        while True:
            sleep(0.1)

            if self.args.stop:
                if not get_input("P8_7") or not get_input("P8_8") or not get_input("P8_9") or not get_input("P8_10"):
                    self.quit()


            for key in self.arbitres.keys():
                self.arbitres[key].evalue()

#======================================================================
# Fonction :    main
# Description : Routine principale
#======================================================================
def main():
    parser = argparse.ArgumentParser(description='Robot Marcus (BBB) - Michel')

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help="Imprime l'aide sur l'exécution du script.")
    parser.add_argument('-l',
                        '--logfile',
                        action='store',
                        default=None,
                        help="Spécifie le chemin du journal d'événement.")
    parser.add_argument('-s',
                        '--stop',
                        action='store_true',
                        help="Arrête l'exécution lorsqu'un impact est détecté.")
    parser.add_argument('-n',
                        '--nocam',
                        action='store_true',
                        help="Lance le programme sans la caméra et les comportements qui en dépendent.")
    parser.add_argument('--scan',
                        action='store_true',
                        help="Scanne la couleur devant la caméra au démarrage. Sinon la dernière couleur sauvegardée est chargée.")

    marcus = Marcus(args=parser.parse_args())
    marcus.loop()

if __name__ == '__main__':
    main()

