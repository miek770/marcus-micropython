# Projet Marcus 3

Je désigne cette version comme étant la 3e à cause des changements de contrôleur. Le projet a débuté avec un Brainstem d'Acroname, qui a été remplacé brièvement par un MAKE Controller, puis finalement par un Beaglebone Black.

La principale différence, cependant, est que chaque robot utilise maintenant le même contrôleur et une base commune. Ça facilite beaucoup l'intégration de modules essentiels, comme la CMUCam2+, pour tous les participants.

## Prochaines tâches

- Remplacer ma fonction msg par du simple logging;
- Utiliser les bornes 7 et 8 plutôt que 5 et 6 sur le P9 pour mon 5V. Le SYS_5V est coupé lorsque le BBB est fermé, ce qui va éviter de présenter une tension aux bornes. 250mA max, à tester;
- Créer de nouveaux tests pour le module de CMUCam2+;
- Remplacer certaines boucles par pyinotify pour réduire le temps de réaction ainsi que la charge sur le CPU;
- Créer un module "mémoire" avec SQLite3;
- Créer un module de supervision de batterie. Je pourrais m'en servir dans le journal et peut-être même adapter le comportement du robot.

## Notes

### Alimentation

Avec la batterie actuelle rechargée le robot se promène sans problème pendant plus de 10 minutes. J'ai fait un test et après 14 minutes il s'est mis à hésiter énormément à cause des GP2D12 qui détectaient constamment des obstacles là où il n'y en avait pas. C'est probablement dû à une baisse de tension.

J'ai arrêté le test après environ 17 minutes. Ça fait maintenant une vingtaine de minutes au moins que la batterie alimente le BBB avec une connexion active sur eth0. L'autonomie semble donc suffisante pour les premiers combats.

### Schémas

Les schémas électriques ont été réalisés avec gEDA sur Linux. Il faudrait que je trouve un programme équivalent sur Windows, ou que j'utilise le format DWG à la place (plus commun). Ou SVG.

2016-12-12 : J'utilise maintenant Eagle pour mes circuits électriques et les PCB. Ceux-ci sont commandés chez OSH Park. La tendance est aussi de faire les circuits dans des sous-projets à part, tels que [marcus-boucliers](https://github.com/miek770/marcus-boucliers) et [marcus-bbbcape](https://github.com/miek770/marcus-bbbcape).

### Chasse

Une fois l'autre robot détecté, le robot doit le viser et faire feu. La version préliminaire sera assez limitée puisqu'il n'y aura pas de bouclier et de canon, mais je devrais faire 2 boucles de contrôle avec feedback pour :

1. Centrer le robot sur la cible (viser);
2. Maintenir une distance désirée.

Idéalement, dans une version future du projet avec une tourelle semi-indépendante, celle-ci pour être asservie avec une boucle PID complète. Ce PID serait important pour un temps de réponse rapide, une erreur nulle en régime permanent, et un ajustement constant pour suivre les déplacements de chaque robot l'un par rapport à l'autre. Avec une simple boucle proportionnelle il reste une erreur constante, et il faut limiter le gain pour éviter l'oscillation. Quoiqu'avec un servomoteur comme actuateur la consigne est en position absolue, le servomoteur est déjà asservi à l'interne. Ce n'est donc pas pertinent.

Ça le serait pour contrôler l'orientation du robot au complet avec la cible, en agissant sur les moteurs gauche et droit. Dans ce cas je pourrais faire un PID pour améliorer le contrôle.

### Améliorations

#### Évasion infrarouge

Le contrôle actuel des moteurs lors de détection d'obstacles par infrarouge est très polarisé. S'il y a un obstacle à gauche, le moteur droit se met à reculer et le gauche à avancer à la vitesse maximale. Ensuite, les 2 se remettent à avancer. Pour chaque manoeuvre, il y a donc au moins 2 changements de directions sur l'un des moteurs. Ça provoquer un délai, un mouvement saccadé et une inutilement forte consommation électrique. Je devrais plutôt d'abord tenter d'utiliser une commande proportionnelle à la différence entre les 2 capteurs.

Donc plutôt que d'arrêter et de tourner sur place lorsqu'un obstacle est détecté, le robot aurait un déplacement sinueux qui éviterait doucement les obstacles.

Pour y parvenir je dois modifier le module de moteurs et y activer les PWM (sur enable). Pour le moment les pins sont à vrai ou faux.

#### Statisme

Créer une routine de statisme qui détecte une absence de variation générale des capteurs pendant une certain temps, dans le but de détecter une absence de mouvement. Idéalement il me faudrait une détection de rotor barré (haut courant), mais une détection de statisme permettrait aussi de valider que le robot est bloqué.

#### Qualification des capteurs

Une routine de qualification des capteurs pourrait être implantée pour chacun afin de détecter s'il opère normalement. Par exemple, un bumper qui reste activé alors que le robot se déplace (actions aux moteurs combinés avec une absence de statisme) indique probablement que le bumper est "collé".

Même chose pour un capteur infrarouge qui reste identique dans la même situation.

Pour la caméra, le plus simple est probablement juste de s'assurer que le lien de communication est toujours bon. Par contre c'est le capteur essentiel, non-remplaçable. Sans caméra le robot ne peut pas tirer et devrait donc tomber en faute catastrophique.

#### Approche par comportements

L'approche de programmation par comportement pourrait être une alternative intéressante à la structure actuelle du programme. Chaque comportement (ex.: évasion infrarouge, évasion impact, exploration) donne ses conclusions à un ou des arbitres, et le ou les arbitres décident quel comportement remporte le droit d'opérer l'actionneur. Des priorités statiques peuvent être données aux comportements, et des priorités dynamiques peuvent varier en cours d'exécution.

Pour l'instant mon programme est plutôt basé sur des routines de capteurs, les décisions sont prises dans une grande boucle. L'effet désiré est le même, mais la boucle peut devenir gigantesque à mesure que le programme grossit.

Il faudra aussi gérer des boucles différentes selon le mode du robot (exploration, combat, etc.). Les comportements ne changeraient pas nécessairement, mais les priorités pourraient changer, des comportements pourraient être désactivés, et d'autres activés. Ce serait une façon plus élégante de tout gérer. Haha, en poursuivant ma lecture de mon ouvrage de référence j'ai lu qu'il est tentant d'aller vers un système à priorités variables, mais que c'est très rarement requis. Un système à priorités fixes est plus simple, plus élégant et plus facile à comprendre. C'est pas fou, plutôt que de faire des changements de priorités je pourrais dupliquer certains comportements simples avec des variations et activer des versions dans certaines circonstances seulement.

Par exemple, dans le mode actuel d'exploration il y a un comportement d'ennui. Lorsqu'il ne se passe rien d'excitant pendant un certain temps, le robot tourne aléatoirement sur lui-même. En mode combat, si l'ennemi disparaît soudainement, je voudrais que le robot se mette à tourner rapidement sur lui-même pour trouver l'ennemi. Plutôt que d'augmenter la priorité de la routine d'ennui, de modifier son délai et la durée de sa rotation, je devrais la dupliquer et activer le comportement uniquement lorsque le stress est au-delà d'un certain seuil.

Le stress pourrait être une variable globale qui est augmenté par certains événements, et décroit progressivement en l'absence d'événements.

À noter que du parallelisme peut être requis quand même pour les routines qui peuvent ou doivent bloquer, comme celles impliquant une quelconque communication (ex.: caméra).

## Installation

- Flasher le BBB avec l'image Debian;
- Configurer hostname, PermitRootLogin;
- Installer git, screen;
- Désinstaller les programmes inutiles (Apache2, Xorg, lightdm, etc.);
- Configurer :

  - dpkg-reconfigure tzdata;
  - dpkg-reconfigure locales (voir la section Standard de https://wiki.debian.org/Locale pour modifier /etc/profile);
  - Samba;

            apt-get install samba
            mv /etc/samba/smb.conf /etc/samba/smb.conf.old
            cp /root/marcus/ressources/smb.conf /etc/samba/smb.conf
            testparm /etc/samba/smb.conf
            systemctl start samba
            systemctl enable samba

  - hosts;
  - vim;
  - bash;
  - marcus.service;
  - uEnv.txt.
