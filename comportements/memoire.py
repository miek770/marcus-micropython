#-*- coding:utf-8 -*-

# Librairies spéciales
#======================
import config
from comportements.base import Comportement
from peripheriques.gp2d12 import GP2D12
from machine import Pin

class Memoire(Comportement):
    """Ce comportement ne sert qu'à enregistrer un historique d'état
    des divers capteurs du robot pouvant ensuite être utilisé par les
    autres comportements. Ce comportement doit avoir la priorité la
    plus faible pour être évalué à chaque cycle, et ne doit jamais
    retourner autre chose que "None" à l'arbitre.
    """

    def variables(self):
        self.rf_avant_centre = GP2D12(32)
        self.rf_avant_gauche = GP2D12(35)
        self.rf_avant_droite = GP2D12(34)

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

    def decision(self):

        actuel = (
                self.bmpr_avant_droite.value(),
                self.bmpr_avant_gauche.value(),
                self.bmpr_arrie_droite.value(),
                self.bmpr_arrie_gauche.value()
                )
        config.passe_capteurs["pare_chocs"].append(actuel)

        actuel = config.track
        config.passe_capteurs["camera"].append(actuel)

        actuel = (
                self.rf_avant_centre.get_dist(),
                self.rf_avant_gauche.get_dist(),
                self.rf_avant_droite.get_dist()
                )
        config.passe_capteurs["gp2d12"].append(actuel)

        return None
