# Partie 2: Compilation, debug et gestionnaire de signaux


## Exercice 1 : GDB et fichier core

**Question 1** : Le processus a fait un Segmentation fault (core dumped). Il y a des problèmes

**Question 2** : Avec les commandes suivantes, on obtient l'erreur SEGV.
````
$ echo $?
139
$ kill -l 11
SEGV
````

**Question 3** : Voici les lignes obtenues
````
#0  strlen () at ../sysdeps/x86_64/strlen.S:106
#1  0x00007f34ad27f69c in _IO_puts (str=0x0) at ioputs.c:35

#2  0x00007f34ad5dab41 in knot_to_kmh_str (not=5.51000023, size=6,
    format=0x7f34ad5db00f "%05.1f", kmh_str=0x7ffe0bee8f70 "010.2")
    at nmea.c:23
#3  0x00007f34ad5daf98 in nmea_vtg (vtg=0x7ffe0bee8fb0) at nmea.c:178
#4  0x0000000000400bc4 in write_vtg (fd=3) at gps.c:40
#5  0x0000000000400e3c in main () at gps.c:109
````
Le problème se trouve dans les lignes de #2 à #5. En effet, les 2 premières lignes utilisent des librairies standards, donc sûre.

**Question 4** : Voici le message obtenu:
````
/home/fabrice/Bureau/UV5.2/embsys/labs/sysprog/gps/bin/gps: error while loading shared libraries: libptmx.so: cannot open shared object file: No such file or directory
````
Il manque donc un import d'une librairies.

**Question 5** : D'après le man, ldd donne les librairies nécessaires au programme. Cela permet de savoir quelles librairies manquent à l'import.
````
	linux-vdso.so.1 =>  (0x00007fffedbe1000)
	libptmx.so => not found
	libnmea.so => not found
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1a273f3000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f1a277bd000)
````

**Question 6** : La ligne dessous permet d'acceder aux librairies nécessaires. Pour pouvoir faire de même en lancant le fichier compilé directement, il faut soit revoir les paramètres de compilation pour rajouter l'importation des librairies, soit le sourcer dans le terminal (ou rajouter l'export dans le bashrc).
````
export LD_LIBRARY_PATH=$ROOT_DIR/lib
````

**Question 7** : "s" fait passer le parcours des instructions à l'instruction suivante, tandis que "n" ne rentre pas dans les fonctions et continue après l'appel fonction.

**Question 8** : Cela peut servir quand il n'est pas possible d'avoir accès directement aux fichiers (sur un serveur, chez un client lointain).

## Exercice 2 : LD_PRELOAD et sigaction

**Question 1** :











d
