# Projet Marcus 3

## Prochaines tâches

- Assembler un circuit de communication avec la CMUCam2+ pour M-A;
- Migrer le BBB de M-A sur Debian (je crois que c'est déjà fait, à vérifier);
- Tester les seuils de détection des GP2D12 sur les côtés, et l'augmenter ou le garder tel quel en avant;
- Remplacer certaines boucles par pyinotify pour réduire le temps de réaction ainsi que la charge sur le CPU;
- Créer un module "mémoire" avec SQLite3;
- Ajouter une lecture de la tension de la batterie pour faire un historique (l'enregistrer dans la base de données) et soulever une alarme lorsque le niveau est critique. J'ai eu un problème dernièrement, la batterie a duré seulement quelques minutes après une recharge complète et le BBB s'est éteint. Je crois que la batterie est vieille et je vais la remplacer pour une de plus grande capacité mais si le problème se répète je devrai ajouter une batterie indépendante pour l'électronique. 2016-04-11 : J'ai remplacé la batterie, à tester à nouveau.

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
