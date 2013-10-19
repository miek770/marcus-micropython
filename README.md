# Projet Marcus 3

Hey bro, voici quelques instructions, notes et rappel que je prévois surtout utiliser pour dupliquer mon environnement de travail sur ton BBB.

## Prochaines tâches

1. Créer un sous-répertoire modules et y déplacer "bumpers.py"
2. L'exclure du dépôt marcus-base et l'inclure dans un nouveau dépôt marcus-modules
3. Déterminer de quelle façon inclure le "raisonnement" du robot au programme de base (main.py)
4. Il y a actuellement un bug avec la librairie ADC qui créée une "Segmentation Fault". Ç'aurait dû avoir été réglé il y a longtemps selon Adafruit
5. Développer le module CMUCam2+ (sur I2C si possible)
6. Créer un module "mémoire" avec SQLite3
7. Développer les autres modules en fonction de mon programme précédent (Marcus 2)

## Guide d'installation BBB - Marcus 3

### Installation d'Arch Linux

- Suivre les étapes données sur le site d'ARM Arch Linux pour le BBB
- Dans les étapes il manque :

        pacman -Syy dostools wget

### Préparation de l'environnement

#### Général (Linux)

- Mise à jour d'Arch Linux ARM :

        pacman -Syu

- Régler le temps et le fuseau horaire :

        timedatectl set-timezone Canada/Eastern
        echo <hostname> > /etc/hostname

#### Samba

- Configurer samba :

        pacman -S samba vim
        mv /etc/samba/smb.conf /etc/samba/smb.conf.old
        cp /root/marcus/smb.conf /etc/samba/smb.conf
        testparm /etc/samba/smb.conf
        systemctl start smbd
        systemctl enable smbd

#### Python

- Installer :

        pacman -S git python2-setuptools gcc python2-virtualenv

- Créer un virtualenv et installer les pré-requis :

        virtualenv2 ~/marcus
        source ~/marcus/bin/activate
        pip install -r ~/marcus/requirements.txt

#### Systemctl

- Lier /usr/lib/systemd/system/marcus.service

        ln -s /root/marcus/marcus.service /usr/lib/systemd/system/marcus.service
        systemctl status marcus
