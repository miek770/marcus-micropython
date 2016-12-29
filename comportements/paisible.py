#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging

# Librairies spéciales
#======================
from base import Comportement
import config

class Paisible(Comportement):
    """Comportement paisible, pour le contrôle de la fréquence des
    boucles d'exécution dans main.py et cmucam.py.
    """

    def decision(self):
        return 0.1
