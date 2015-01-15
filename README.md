# Projet Marcus 3

Cette branche sert à faire la migration de Arch vers Debian pour le Beaglebone Black. La raison principale est que Debian est devenu la distribution officielle du BBB et que les librairies sont développées en conséquence. J'ai laissé tomber le virtualenv qui de toute façon n'est pas très pertinent pour un appareil dédié à une seule tâche (robot). J'ai aussi retiré certaines étapes du setup ici-bas qui n'étaient plus pertinentes.

Il y avait aussi beaucoup de problèmes avec Arch pour le BBB : librairies mal placées, synchronisation qui "timeout" avec pacman, DTO qui plante si on tente de retirer un module, etc.

## Prochaines tâches

- Assembler un circuit de communication avec la CMUCam2+ pour M-A;
- Migrer le BBB de M-A sur Debian;
- Tester les seuils de détection des GP2D12 sur les côtés, et l'augmenter ou le garder tel quel en avant;
- Ajouter une option (argument) pour arrêter l'exécution si un bumper est actionné;
- Remplacer certaines boucles par pyinotify pour réduire le temps de réaction ainsi que la charge sur le CPU;
- Créer un module "mémoire" avec SQLite3;
- Ajouter une lecture de la tension de la batterie pour faire un historique (l'enregistrer dans la base de données) et soulever une alarme lorsque le niveau est critique. J'ai eu un problème dernièrement, la batterie a duré seulement quelques minutes après une recharge complète et le BBB s'est éteint. Je crois que la batterie est vieille et je vais la remplacer pour une de plus grande capacité mais si le problème se répète je devrai ajouter une batterie indépendante pour l'électronique.

## Installation

- Flasher le BBB avec l'image Debian;
- Désinstaller les programmes inutiles (Apache2, Xorg, lightdm, etc.);
- Configurer :

  - Fuseau horaire;
  - Samba;

            apt-get install samba
            mv /etc/samba/smb.conf /etc/samba/smb.conf.old
            cp /root/marcus/smb.conf /etc/samba/smb.conf
            testparm /etc/samba/smb.conf
            systemctl start smbd
            systemctl enable smbd

  - Locales;
  - Hostname;
  - hosts;
  - vim;
  - bash;
  - marcus.service;
  - uEnv.txt.
