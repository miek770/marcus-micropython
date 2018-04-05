from collections import deque

VERBOSE = True
LOGFILE = None
STOP = True
NO_CAM = True
NO_MODE = True
SCAN = False

global track
track = dict()

global passe_moteurs
passe_moteurs = deque(maxlen=100)

global passe_capteurs
passe_capteurs = dict()
passe_capteurs["pare_chocs"] = deque(maxlen=100)
passe_capteurs["camera"] = deque(maxlen=100)
passe_capteurs["gp2d12"] = deque(maxlen=100)

global periode
periode = 0.1 # en seconde

global periode_change
periode_change = False
