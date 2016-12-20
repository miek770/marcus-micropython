#!/usr/bin/python
#-*- coding: utf-8 -*-

# Librairies standard
#=====================
import time, logging

# Librairies spéciales
#======================
from pins import set_output, set_low, set_high
from base import Arbitre
import config

class Moteurs(Arbitre):
    """À la fois l'arbitre du contrôle des moteurs et le pilote
    d'opération des moteurs.

    P9_12 - Direction moteur droit
    P9_13 - Direction moteur droit
    P9_14 - Enable moteur droit (PWM)
    P9_15 - Direction moteur gauche
    P9_16 - Enable moteur gauche (PWM)
    P9_21 - Direction moteur gauche
    """

    def __init__(self, nom="moteurs"):

        self.nom = nom
        self.comportements = list()
        self.precedent = None
        logging.info("Arbitre {} initialisé".format(self.nom))

        set_output('P9_12')
        set_output('P9_13')
        set_output('P9_14')
        set_output('P9_15')
        set_output('P9_16')
        set_output('P9_21')

        self.manoeuvre = False
        self.vecteur = None
        self.arret()

    def arret(self):
        """Cette méthode est appelée à l'initialisation de cet arbitre
        spécifique ainsi que pour tous les arbitres à l'arrêt du
        programme générale dans main.py.
        """
        self.droit_arret()
        self.gauche_arret()

    def evalue(self):
        """Méthode appelée par la boucle principale dans main.py pour
        demander à l'arbitre d'interroger chacun de ses comportements
        et de rendre une décision.
        """

        for i in range(len(self.comportements)):

            # Une manoeuvre prioritaire est en cours, donc on arrête
            # l'évaluation des comportements et on autorise la
            # manoeuvre à continuer
            if self.manoeuvre and self.comportements[i][1] >= self.precedent:
                self.poursuit_manoeuvre()
                break

            # Sinon, on évalue le comportement
            action = self.comportements[i][0].evalue()

            # S'il y a une action à prendre... 
            if action is not None:

                logging.debug("Comportement {} : {}".format(self.comportements[i][0].nom, action))

                # On avise le comportement gagnant pour qu'il puisse en
                # tenir compte lors de la prochaine itération
                self.comportements[i][0].precedent = True
                self.precedent = self.comportements[i][1]

                # On met aussi l'historique à jour pour les
                # comportements que ça intéresserait (ex.: explore)
                config.passe_moteurs.append(self.precedent)

                self.traite_vecteur(action)
                break

            # S'il n'y a pas d'action à prendre...
            else:
                logging.debug("Comportement {} : Aucune action".format(self.comportements[i][0].nom))

    def traite_vecteur(self, vecteur):
        """Interprétation de vecteur de commande de moteurs.
        
        Le comportement doit retourner un vecteur (une liste)
        décrivant les actions à prendre par le moteur. La liste est
        une série de tuples avec la vitesse du moteur droit, la
        vitesse du moteur gauche et la durée de l'événement.

        Le module de moteurs doit ensuite interpréter cette commande
        et la traduire en consigne de moteurs.

        Une nouvelle commande doit interrompre une manoeuvre en cours.

        [(vitesse_gauche, vitesse_droite, duree), ...]
        """

        # Une seule action à prendre
        if len(vecteur) == 1 and vecteur[0][2] == 0:
            self.manoeuvre = False

        # Manoeuvre à exécuter
        else:
            self.manoeuvre = True
            self.vecteur = vecteur
            self.index = 0
            self.debut = self.maintenant()

        # Exécute la première étape
        self.execute(vecteur[0])

    def poursuit_manoeuvre(self):
        """Si une manoeuvre est en cours et qu'on lui permet de se
        poursuivre (voir la méthode evalue()), alors cette méthode est
        appelée.
        """

        # Aucune manoeuvre en cours
        if not self.manoeuvre:
            logging.error("Comportement {} : Aucune manoeuvre en cours".format(self.nom))
            return

        # Étape complétée
        if self.maintenant() >= self.vecteur[self.index][2]*1000 + self.debut:
            self.index += 1

            # Manoeuvre complétée
            if self.index == len(self.vecteur):
                self.manoeuvre = False

            # Sinon, on exécute la prochaine étape
            else:
                self.execute(self.vecteur[self.index])
                self.debut = self.maintenant()

    def maintenant(self):
        """Retourne l'instant actuel en millisecondes.
        """
        return int(round(time.time() * 1000))

    def execute(self, action):
        """Exécute l'action demandée (une étape de vecteur, sans
        considérer la durée) sur les 2 moteurs.
        """

            if action[0] == 0:
                self.gauche_freine()
            elif action[0] > 0:
                self.gauche_avance()
            elif action[0] < 0:
                self.gauche_recule()

            if action[1] == 0:
                self.droit_freine()
            elif action[1] > 0:
                self.droit_avance()
            elif action[1] < 0:
                self.droit_recule()

    # Fonctions par moteur
    #======================
    def gauche_arret(self):
        set_low('P9_14') # Disable

    def gauche_freine(self):
        set_high('P9_12')
        set_high('P9_13')
        set_high('P9_14') # Enable

    def gauche_recule(self):
        set_low('P9_12')
        set_high('P9_13')
        set_high('P9_14') # Enable

    def gauche_avance(self):
        set_high('P9_12')
        set_low('P9_13')
        set_high('P9_14') # Enable

    def droit_arret(self):
        set_low('P9_16') # Disable

    def droit_freine(self):
        set_high('P9_15')
        set_high('P9_21')
        set_high('P9_16') # Enable

    def droit_recule(self):
        set_high('P9_15')
        set_low('P9_21')
        set_high('P9_16') # Enable

    def droit_avance(self):
        set_low('P9_15')
        set_high('P9_21')
        set_high('P9_16') # Enable

