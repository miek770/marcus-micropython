# Projet Marcus 3

Je désigne cette version comme étant la 3e à cause des changements de contrôleur. Le projet a débuté avec un Brainstem d'Acroname, qui a été remplacé brièvement par un MAKE Controller, puis finalement par un Beaglebone Black.

La principale différence, cependant, est que chaque robot utilise maintenant le même contrôleur et une base commune. Ça facilite beaucoup l'intégration de modules essentiels, comme la CMUCam2+, pour tous les participants.

## 1. Prochaines tâches

- Utiliser les bornes 7 et 8 plutôt que 5 et 6 sur le P9 pour mon 5V. Le SYS_5V est coupé lorsque le BBB est fermé, ce qui va éviter de présenter une tension aux bornes. 250mA max, à tester;
- Créer de nouveaux tests pour le module de CMUCam2+;
- Créer un module de supervision de batterie. Je pourrais m'en servir dans le journal et peut-être même adapter le comportement du robot.

## 2. Notes

### 2.1 Alimentation

Avec la batterie actuelle rechargée le robot se promène sans problème pendant plus de 10 minutes. J'ai fait un test et après 14 minutes il s'est mis à hésiter énormément à cause des GP2D12 qui détectaient constamment des obstacles là où il n'y en avait pas. C'est probablement dû à une baisse de tension.

J'ai arrêté le test après environ 17 minutes. Ça fait maintenant une vingtaine de minutes au moins que la batterie alimente le BBB avec une connexion active sur eth0. L'autonomie semble donc suffisante pour les premiers combats.

### 2.2. Schémas

Les schémas électriques ont été réalisés avec gEDA sur Linux. Il faudrait que je trouve un programme équivalent sur Windows, ou que j'utilise le format DWG à la place (plus commun). Ou SVG.

2016-12-12 : J'utilise maintenant Eagle pour mes circuits électriques et les PCB. Ceux-ci sont commandés chez OSH Park. La tendance est aussi de faire les circuits dans des sous-projets à part, tels que [marcus-boucliers](https://github.com/miek770/marcus-boucliers) et [marcus-bbbcape](https://github.com/miek770/marcus-bbbcape).

### 2.3. Amélioration de l'évasion infrarouge

Le contrôle actuel des moteurs lors de détection d'obstacles par infrarouge est très polarisé. S'il y a un obstacle à gauche, le moteur droit se met à reculer et le gauche à avancer à la vitesse maximale. Ensuite, les 2 se remettent à avancer. Pour chaque manoeuvre, il y a donc au moins 2 changements de directions sur l'un des moteurs. Ça provoquer un délai, un mouvement saccadé et une inutilement forte consommation électrique. Je devrais plutôt d'abord tenter d'utiliser une commande proportionnelle à la différence entre les 2 capteurs.

Donc plutôt que d'arrêter et de tourner sur place lorsqu'un obstacle est détecté, le robot aurait un déplacement sinueux qui éviterait doucement les obstacles.

Pour y parvenir je dois modifier le module de moteurs et y activer les PWM (sur enable). Pour le moment les pins sont à vrai ou faux.

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
