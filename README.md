# Projet Marcus 4

Je désigne cette version comme étant la 4e à cause des changements de contrôleur. Le projet a débuté avec un Brainstem d'Acroname, qui a été remplacé brièvement par un MAKE Controller, puis par un Beaglebone Black, et finalement par un ESP-WROOM-32 sur MicroPython.

La principale différence dès la version 3, cependant, est que chaque robot utilisait le même contrôleur et une base commune. Ça facilite beaucoup l'intégration de modules essentiels, comme la CMUCam2+, pour tous les participants. Maintenant que mon robot doit changer de base, le code doit diverger pour s'adapter à MicroPython et aux nouvelles configurations d'entrées/sorties.

À part les changements évidents (ex.: entrées/sorties), il faut aussi adapter le code à MicroPython. Celui-ci est basé sur Python 3 alors que le programme précédent était en version 2 à cause de la librairie d'Adafruit-BBIO.

De plus, tous les modules standards ne sont pas intégrés à MicroPython. Ils doivent être ajoutés manuellement. Pour l'instant ils sont inclus au répertoire deploy qui est utilisé pour cloner le code sur le robot sans copier tout le reste (symlinks).

## 1. Prochaines tâches

### 1.1. Conversion à MicroPython

- J'ai actuellement de la difficulté avec deque. J'ai trouvé une version en python sur Pypy mais elle ne fonctionne pas bien. Je devrais prendre le temps de remplacer deque par une liste dans laquelle je fais une validation manuelle de taille avec une petite fonction externe par exemple. Ou bien je pourrais désactiver la mémoire, mais je n'aime pas cette option et elle ne règle pas le problème;
- Trouver comment permettre au robot de démarrer lorsque les RX0 et TX0 sont utilisés pour la CMUCAM. Pour l'instant si c'est fils sont raccordés, rien ne démarre;
- Limiter la taille du journal en suivant ces instructions : [https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python](https://stackoverflow.com/questions/24505145/how-to-limit-log-file-size-in-python). Vérifier si ça fonctionne avec la librairie de logging de Micropython.

### 1.2. Bogues

- Ajouter un trou d'accès sur la base rotative pour permettre de visser le roulement à billes aux espaceurs sur le chassis du robot.

### 1.3. Améliorations

- Faire un premier "combat" où les robots tentent de se trouver (jeu de tag);
- Tester et intégrer les boucliers, le canon et la plateforme d'armement au robot et au code;
- Créer de nouveaux tests pour le module de CMUCam2+;
- Créer un module de supervision de batterie. Je pourrais m'en servir dans le journal et peut-être même adapter le comportement du robot.

## 2. Notes

### 2.1. Alimentation

À revoir après remplacement du contrôleur (BBB remplacé par ESP-WROOM-32) et ajout d'une seconde batterie.

### 2.2. Rangefinder central

Dernièrement j'ai fait d'autres tests et le rangefinder central a tendance à faire de fausses détections à répétition. Il est peut-être trop enfoncé en dessous du robot et détecte le châssis supérieur. Je devrais peut-être le désactiver pour le moment, de toute façon je ne suis pas sûr qu'il aide réellement le robot à se déplacer.

Pas testé depuis le changement de support avant.

### 2.3. Schémas

J'utilise maintenant Eagle pour mes circuits électriques et les PCB. Ceux-ci sont commandés chez OSH Park. La tendance est aussi de faire les circuits dans des sous-projets à part, tels que :

- [marcus-boucliers](https://github.com/miek770/marcus-boucliers);
- [marcus-bbbcape](https://github.com/miek770/marcus-bbbcape).

Les circuits seront à revoir avec le remplacement du contrôleur. Les boucliers resteront identiques, mais leur intégration changera. Le bbbcape est complètement à revoir, ou peut-être simplement à abandonner.

## 3. Installation

Suivre ce tutoriel, mais en l'adaptant considérant que le ESP32 est maintenant supporté officiellement par MicroPython : [https://www.cnx-software.com/2017/10/16/esp32-micropython-tutorials/](https://www.cnx-software.com/2017/10/16/esp32-micropython-tutorials/)

## 4. Idées

- Installer un serveur web léger pour la supervision en temps réel par wifi;
- Limiter la vitesse des moteurs lorsque la batterie descend sous un certain seuil;
- Faire une petite progression rapide des moteurs lors des démarrages et changements de direction pour éviter les forts appels de courant;
- Permettre à un comportement (ex.: batterie faible) d'en désactiver un autre? Probablement pas, c'est contre la philosophie d'isolation des comportements, mais à réfléchir;
- Empêcher l'exploration en ligne droite lorsque la batterie descend sous un certain seuil.

