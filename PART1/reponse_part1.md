# Partie 1: Utilisation d'un simulateur GPS

## Exercice 1 : GDB et fichier core

**Question 1** : Makefile : fichier définissant les règles de compilation. la commande make permet de lancer la compilation avec les règles définis dans le makefile.

**Question 2** : gcc est utilisé.

**Question 3** : Bibliotèque partagée : fichier compilé contenant des fonctions pouvant être utilisées par d'autres programmes.

**Question 4** : imaginons un fichier C nommé hello_world.c contenant des fonctions. la ligne de commande la plus simple à lancer dans le repertoire courant est : 
````
gcc hello_world.c -o hello_world
````
**Question 5** : Prenons par exemple le fichier nmea.c que l'on veut compiler en bibliotèque partagée. Les commandes minimales pour le faire sont : 
````
gcc -c -fPIC nmea.c -o nmea.o
gcc -shared -o libnmea.so nmea.o
````
