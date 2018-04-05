#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging

# Librairies spéciales
#======================
from comportements.base import Comportement
import config

class Agressif(Comportement):
    """Comportement agressif, pour le contrôle de la fréquence des
    boucles d'exécution dans main.py et cmucam.py.

    Le comportement devrait être influencé par les boucliers et la
    détection par la caméra. Il devrait employer un compteur
    décroissant qui conserve l'agressivité pendant un certain temps
    après la disparition d'événement.
    """

    def decision(self):
        return None
