# Description fonctionnelle du circuit standard des boucliers

## Caractéristiques techniques

- Tension d'alimentation
  - Minimal : 5Vcc
  - Maximal : 6Vcc
- Niveau logique
  - 0-5 Vcc (TTL)
- Temps de réaction
  - À compléter

## Borniers d'interface
- TB0 : Alimentation
  1. Masse
  2. V+
- TB1 : Contrôleur
  3. Mort
  4. Bouclier 1
  5. Bouclier 2
  6. Bouclier 3
  7. Bouclier 4
  8. Réinitialise
  9. Auxiliaire 1
  10. Auxiliaire 2
- TB2 : Boucliers
  11. Bouclier 1A
  12. Bouclier 1B
  13. Bouclier 2A
  14. Bouclier 2B
  15. Bouclier 3A
  16. Bouclier 3B
  17. Bouclier 4A
  18. Bouclier 4B

### TB0 – Alimentation

Ce bornier sert à fournir une alimentation régulée à l'externe à une tension entre 5 et 6 VCC.
Il n'y a aucun régulateur de tension ni condensateur régulateur dans le circuit standard des boucliers.
La masse doit être isolée des composants de puissance afin d'éviter de perturber le fonctionnement des composants sensibles du circuit.

### TB1 – Interface contrôleur
L'interface contrôleur sert à communiquer de l'information sur l'état des boucliers au contrôleur principal, et à recevoir des commandes de réinitialisation une fois que les données ont bien été communiquées.

#### Sorties

Les bornes 3 à 7, c'est-à-dire « Mort », « Bouclier 1 », « Bouclier 2 », « Bouclier 3 » et « Bouclier 4 » servent à communiquer l'état des boucliers, ainsi que le statut de mort (voir section 3).
La sortie « Mort » est normalement à 0 et passe à 1 (voir section 1) lorsque les points de vies ont été épuisés (voir section 3).
Après que la sortie soit passée à 1, une réinitialisation manuelle […] ou une coupure de l'alimentation V+ est requise afin de remettre le compteur de vies à sa valeur initiale et remettre la sortie de mort à 0.
Les sorties « Bouclier 1 », « Bouclier 2 », « Bouclier 3 » et « Bouclier 4 » sont normalement à 0 et passent à 1 (voir section 1) lorsqu'un impact réussi […] est détecté sur le bouclier correspondant.
La sortie en question est maintenue à 1 jusqu'à la prochaine réinitialisation logicielle (voir section 2.2.2).
Il est important de noter que la réinitialisation des sorties 4 à 7 n'a aucun effet sur le décompte des impacts, et donc le statut de mort.

#### Entrée

La borne 8 « Réinitialisation » sert à ramener l'état des sorties 4 à 7 (voir section 2.2.1) à 0, soit leur état au repos.
Elle est activée par un 1 logique et n'a aucun effet sur le décompte des impacts ni le statut de mort.
Elle est à la disposition du concepteur, pour information, dans le cas où il voudrait inclure l'état des boucliers à sa logique.

#### Auxiliaires

Les auxiliaires sont actuellement inutilisés.

### TB2 – Interface boucliers

À venir. Les capteurs se connecteront ici.

## Points de vie

Les points de vie, à l'état initial, sont définis par la configuration d'un interrupteur DIP à […] positions.
La position des interrupteurs doit se faire lorsque le circuit n'est pas alimenté […]
Chaque impact réussi […] abaisse la quantité de points de vie de 1, jusqu'à ce qu'elle atteigne 0.
La borne 3 « Mort » passe alors à 1 et le circuit doit être réinitialisé par la méthode décrite en 2.2.1.
