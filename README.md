# Guide d'installation BBB - Marcus 3

## Installation d'Arch Linux

- Suivre les étapes données sur le site d'ARM Arch Linux pour le BBB
- Dans les étapes il manque :
    pacman -Syy dostools wget

## Préparation de l'environnement

### Général (Linux)

- Mise à jour d'Arch Linux ARM :
    pacman -Syu

- Régler le temps et le fuseau horaire :
    timedatectl set-timezone Canada/Eastern
    echo <hostname> > /etc/hostname

### Samba

- Configurer samba :
    pacman -S samba vim
    vim /etc/samba/smb.conf
        [global]
            server string = Samba %v on %L
            workgroup = HOME
            encrypt passwords = yes
            log level = 1
            max log size = 1000
            printing = bsd
            printcap name = /dev/null

        [marcus]
            path = /root
            writable = yes
            guest ok = yes
            force user = root
            force group = root
    testparm /etc/samba/smb.conf
    systemctl start smbd
    systemctl enable smbd

### Python

- Installer :
    pacman -S git python-setuptools python2-setuptools gcc

- Installer https://github.com/adafruit/adafruit-beaglebone-io-python (utiliser méthode manuelle)

### Systemctl

- Configurer /usr/lib/systemd/system/marcus.service
