#-*- coding:utf-8 -*-

# Librairies spéciales
#======================
import config
from base import Comportement
from peripheriques.pins import get_input
from peripheriques.gp2d12 import get_dist

class Memoire(Comportement):
    """Ce comportement ne sert qu'à enregistrer un historique d'état
    des divers capteurs du robot pouvant ensuite être utilisé par les
    autres comportements. Ce comportement doit avoir la priorité la
    plus faible pour être évalué à chaque cycle, et ne doit jamais
    retourner autre chose que "None" à l'arbitre.
    """

    def decision(self):

        actuel = (not get_input("P8_7"), not get_input("P8_8"), not get_input("P8_9"), not get_input("P8_10"))
        config.passe_capteurs["pare_chocs"].append(actuel)

        actuel = config.track
        config.passe_capteurs["camera"].append(actuel)

        actuel = (get_dist("AIN0"), get_dist("AIN1"), get_dist("AIN2"))
        config.passe_capteurs["gp2d12"].append(actuel)

        return None
