# Projet Marcus 3

## Prochaines tâches

- Assembler un circuit de communication avec la CMUCam2+ pour M-A;
- Migrer le BBB de M-A sur Debian (je crois que c'est déjà fait, à vérifier);
- Remplacer certaines boucles par pyinotify pour réduire le temps de réaction ainsi que la charge sur le CPU;
- Créer un module "mémoire" avec SQLite3;
- Créer un module de supervision de batterie. Je pourrais m'en servir dans le journal et peut-être même adapter le comportement du robot.

## Notes

Avec la batterie actuelle rechargée le robot se promène sans problème pendant plus de 10 minutes. J'ai fait un test et après 14 minutes il s'est mis à hésiter énormément à cause des GP2D12 qui détectaient constamment des obstacles là où il n'y en avait pas. C'est probablement dû à une baisse de tension.

J'ai arrêté le test après environ 17 minutes. Ça fait maintenant une vingtaine de minutes au moins que la batterie alimente le BBB avec une connexion active sur eth0. L'autonomie semble donc suffisante pour les premiers combats.

## Installation

- Flasher le BBB avec l'image Debian;
- Désinstaller les programmes inutiles (Apache2, Xorg, lightdm, etc.);
- Configurer :

  - Fuseau horaire;
  - Samba;

            apt-get install samba
            mv /etc/samba/smb.conf /etc/samba/smb.conf.old
            cp /root/marcus/ressources/smb.conf /etc/samba/smb.conf
            testparm /etc/samba/smb.conf
            systemctl start samba
            systemctl enable samba

  - Locales;
  - Hostname;
  - hosts;
  - vim;
  - bash;
  - marcus.service;
  - uEnv.txt.

