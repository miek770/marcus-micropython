# Projet Marcus 3

Je désigne cette version comme étant la 3e à cause des changements de contrôleur. Le projet a débuté avec un Brainstem d'Acroname, qui a été remplacé brièvement par un MAKE Controller, puis finalement par un Beaglebone Black.

La principale différence, cependant, est que chaque robot utilise maintenant le même contrôleur et une base commune. Ça facilite beaucoup l'intégration de modules essentiels, comme la CMUCam2+, pour tous les participants.

Tant que le code est en développement, il est recommandé de lancer l'application manuellement dans une session "screen" ou "tmux" et de désactiver les fonctions non-désirées. La session screen permet de fermet la connexion SSH (PuTTY ou autre) pendant que le programme roule, sans le faire planter. Par exemple, pour lancer le programme sans la caméra et les modes (agressif et paisible, en développement), avec arrêt automatique dès qu'un pare-choc est actionné :

    python main.py --verbose --logfile=marcus.log --nocam --nomode --stop

Pour lancer le programme dans screen et le détacher immédiatement (donc pas besoin de faire CTRL-A D) :

    screen -d -m python main.py --verbose --logfile=marcus.log --nocam --nomode --stop

Encore plus simple, utiliser mosh plutôt que SSH et laisser faire screen. À tester mais ça marche bien avec un autre BBB.
  
Pour consulter l'aide :

    python main.py --help

## 1. Prochaines tâches

### 1.1. Bogues

- Tester le code davantage, surtout les portions utilisant la caméra. Je ne l'ai presque pas testé et MA a relevé des comportements bizarres pendant ses tests, par exemple la détection qui se fait toujours du même côté. Je crois que c'était causé par l'autre bogue qui a déjà été réglé, mais je dois le vérifier davantage.

### 1.2. Améliorations

- Faire un premier "combat" où les robots tentent de se trouver (jeu de tag);
- Tester et intégrer les boucliers, le canon et la plateforme d'armement au robot et au code;
- Ajouter comportement de "wall following" aléatoire pour aider à passer les cadres de porte. Voir exemple dans mon livre de référence;
- Utiliser les bornes 7 et 8 plutôt que 5 et 6 sur le P9 pour mon 5V. Le SYS_5V est coupé lorsque le BBB est fermé, ce qui va éviter de présenter une tension aux bornes. 250mA max, à tester;
- Créer de nouveaux tests pour le module de CMUCam2+;
- Créer un module de supervision de batterie. Je pourrais m'en servir dans le journal et peut-être même adapter le comportement du robot.

## 2. Notes

### 2.1. Alimentation

Avec la batterie actuelle rechargée le robot se promène sans problème pendant plus de 10 minutes. J'ai fait un test et après 14 minutes il s'est mis à hésiter énormément à cause des GP2D12 qui détectaient constamment des obstacles là où il n'y en avait pas. C'est probablement dû à une baisse de tension.

J'ai arrêté le test après environ 17 minutes. Ça fait maintenant une vingtaine de minutes au moins que la batterie alimente le BBB avec une connexion active sur eth0. L'autonomie semble donc suffisante pour les premiers combats.

### 2.2. Rangefinder central

Dernièrement j'ai fait d'autres tests et le rangefinder central a tendance à faire de fausses détections à répétition. Il est peut-être trop enfoncé en dessous du robot et détecte le châssis supérieur. Je devrais peut-être le désactiver pour le moment, de toute façon je ne suis pas sûr qu'il aide réellement le robot à se déplacer.

### 2.3. Schémas

J'utilise maintenant Eagle pour mes circuits électriques et les PCB. Ceux-ci sont commandés chez OSH Park. La tendance est aussi de faire les circuits dans des sous-projets à part, tels que :

- [marcus-boucliers](https://github.com/miek770/marcus-boucliers);
- [marcus-bbbcape](https://github.com/miek770/marcus-bbbcape).

## 3. Installation

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

## 4. Idées

- Limiter la vitesse des moteurs lorsque la batterie descend sous un certain seuil;
- Faire une petite progression rapide des moteurs lors des démarrages et changements de direction pour éviter les forts appels de courant;
- Permettre à un comportement (ex.: batterie faible) d'en désactiver un autre? Probablement pas, c'est contre la philosophie d'isolation des comportements, mais à réfléchir;
- Empêcher l'exploration en ligne droite lorsque la batterie descend sous un certain seuil.
