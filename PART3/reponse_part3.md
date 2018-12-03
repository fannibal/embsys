## Exercice 1 : Multiplexage

**Question 1** : Il pourrait s'agir des ports.

**Question 2** : Pas de gestion des signaux
Pas de cas par défaut pour le switch-case.
manque de lisibilité sur les arguments (plus de commentaires si possible)

**Question 3** : Les trames GPGLL renvoie le temps en avant dernière position.

**Question 4** : Le multiplexage fonctionne avec les 4 étapes:
````
int fd = open(port, O_RDWR | O_NOCTTY); #ouvrir
(...)
FD_ZERO(&fdset);
FD_SET(fd, &fdset);
select(fd+1, &fdset, NULL, NULL, NULL); #écouter

if (FD_ISSET(fd, &fdset)){
    int bytes = read (fd, buff, sizeof(buff)); #lire
(...)
close(fd); #fermer
````
**Question 4** : L
