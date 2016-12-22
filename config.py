from collections import deque

global track
track = dict()

global passe_moteurs
passe_moteurs = deque(maxlen=100)

global passe_capteurs
passe_capteurs = dict()
passe_capteurs["pare_chocs"] = deque(maxlen=100)
passe_capteurs["camera"] = deque(maxlen=100)
passe_capteurs["gp2d12"] = deque(maxlen=100)
