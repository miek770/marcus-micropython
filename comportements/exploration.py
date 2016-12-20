#-*- coding:utf-8 -*-

# Librairies spéciales
#======================
from base import Comportement

# Vecteur moteur
#================
"""Le comportement doit retourner un vecteur (une liste) décrivant les
actions à prendre par le moteur. La liste est une série de tuples avec
la vitesse du moteur droit, la vitesse du moteur gauche et la durée de
l'événement.

Le module de moteurs doit ensuite interpréter cette commande et la
traduire en consigne de moteurs.

Une nouvelle commande doit interrompre une manoeuvre en cours.

[(vitesse_gauche, vitesse_droite, duree), ...]
"""

# Constantes
#============
duree_rotation_min = 0.5 # en secondes

class Exploration(Comportement):

    def decision(self):
        return [(100, 100, 0)]

