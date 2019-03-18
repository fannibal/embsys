TL;DR:

1. Installation du projet : méthode rapide

2. Installation du projet : méthode manuelle avec Buildroot

3. Paramètres par défaut pour se connecter à la raspberry

4. Utilisation du projet

5. Si ce qui précède échoue

-------------------

# Installation du projet : méthode rapide

Pour installer le projet facilement, voici les étapes à suivre :
1. Télécharger l'image de la partition linux du projet
2. Décompresser l'image linux
3. Insérer une carte SD et identifier le nom du disque associé à la carte SD
4. Formater la carte SD
5. Flasher la carte SD avec l'image du projet

## Télecharger l'image de la partition linux :

Une image flashable du projet est disponible à l'adresse suivante : `https://drive.google.com/file/d/12JaVFQaoY7nQFcYRRTSxN2b99ry7Ld6k/view?usp=sharing`. Cette image est une version de linux épurée et possédant l'ensemble des fichiers du projet nécessitant de se trouver sur la raspberry. il faut donc télécharger cette image sur la machine hôte.

## Décompresser l'image linux

L'image peut être décompressée à l'aide de la commande suivante :

```` $ unzip image.zip -d [destination]
````
Un fichier au format .img est créé.

## Insérer une carte SD et identifier le nom du disque associé à la carte SD

On insère la carte SD dans l'ordinateur hôte à l'aide d'un adapteur USB-micro SD (ou SD-micro SD).
Pour récupérer le nom de disque associé à la carte SD, on se positionne dans le répertoire /dev et on branche-débranche l'adaptateur USB-SD. Le nom *sdX* (où *X* est une lettre) qui apparait et disparait est le disque qui nous intéresse. Pour se faire, il peut être intéressant d'utiliser l'utilitaire nautilus pour afficher l'état du dossier /dev rafraîchi régulièrement :

```` $ sudo apt-get install nautilus
$ nautilus /dev
````

## Formater la carte SD

On utilise l'utilitaire `dd` de la manière suivante :

```` $ sudo dd if=/dev/zero of=/dev/sdx obs=2048
````

## Flasher la carte SD avec l'image du projet.

On utilise à nouveau `dd` :

```` $ sudo dd if=<chemin vers l'image du projet>/image_projet.img of=/dev/sdx
````



# Installation du projet : méthode manuelle avec Buildroot

Cette méthode implique l'utilisation de docker et se découpe en les étapes suivantes :

1. Télécharger le docker de l'image linux vierge
2. Paramétrer Buildroot
3. Insérer une carte SD et identifier le nom du disque associé à la carte SD
4. Formater la carte SD
5. Flasher la carte SD avec l'image du projet
6. Modifier les fichiers de la partition du boot
7. Modifier les fichiers du Root File System de la carte SD
8. Copier les fichiers du projet sur la carte SD

## Télécharger le docker de l'image linux vierge

Le projet se base sur l'image linux proposée par pblottiere téléchargeable sur les serveurs distants de dépôt docker :

```` $ docker pull pblottiere/embsys-rpi3-buildroot-video
````

Pour créer un conteneur:

```` $ docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash
docker# cd /root
docker# ls
buildroot-precompiled-2017.08.tar.gz
docker# tar zxvf buildroot-precompiled-2017.08.tar.gz
````

## Paramétrer Buildroot

L'installation de docker est décrite sur le site de docker :
`https://docs.docker.com/install/linux/docker-ce/ubuntu/`

Pour avoir le support de la caméra sur la RPI3, un firmware spécifique
doit être compilé avec Buildroot. Pour cela, il faut activer l'option
`BR2_PACKAGE_RPI_FIRMWARE_X` dans le fichier de configuration de Buildroot.

De plus, afin d'interagir avec la caméra, l'API de
[V4L](https://linuxtv.org/downloads/v4l-dvb-apis/uapi/v4l/v4l2.html) est
conseillée. Il est donc nécessaire d'activer l'option `BR2_PACKAGE_LIBV4L`
dans le fichier de configuration Buildroot.

## Insérer une carte SD et identifier le nom du disque associé à la carte SD

On insère la carte SD dans l'ordinateur hôte à l'aide d'un adapteur USB-micro SD (ou SD-micro SD).
Pour récupérer le nom de disque associé à la carte SD, on se positionne dans le répertoire /dev et on branche-débranche l'adaptateur USB-SD. Le nom *sdX* (où *X* est une lettre) qui apparait et disparait est le disque qui nous intéresse. Pour se faire, il peut être intéressant d'utiliser l'utilitaire nautilus pour afficher l'état du dossier /dev rafraîchi régulièrement :

```` $ sudo apt-get install nautilus
$ nautilus /dev
````

## Formater la carte SD

On utilise l'utilitaire `dd` de la manière suivante :

```` $ sudo dd if=/dev/zero of=/dev/sdx obs=2048
````

## Flasher la carte SD avec l'image du projet.

On utilise à nouveau `dd` mais nous avons cette fois-ci besoin du chemin d'accès vers l'image linux contenue dans le docker. Pour récupérer l'identifiant du docker, on ouvre un nouveau terminal et exécute la commande suivante :

```` $ docker ps -a
````

On utilise cet identifiant pour copier le fichier image *sdcard.img*. Celui-ci va à son tour pouvoir être flashé sur la carte SD avec la commande `dd` et l'identifiant *sdX* récupéré précédemment..


 ```` $ docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .
 sudo dd if=sdcard.img of=/dev/<sdX> ````

```` $ sudo dd if=<chemin vers l'image du projet>/image_projet.img of=/dev/sdx
````

## Modifier les fichiers de la partition du boot

On localise et récupère les fichiers *start_x.elf* et *fixup_x.dat* à l'aide des commandes `find` et `cp`. Les fichiers sont copiés dans la première partition de la carte SD, ie `/dev/sdbX1`.

 ```` docker: $ find . -name start_x.elf
 docker: $ find . -name fixup_x.dat
 ````

 Puis depuis un nouveau terminal, on utilise les chemins trouvés précédemment pour copier les deux fichiers sur la première partition de la carte SD :
 
 ```` $ docker cp <container_id>:<chemin_start_x.elf>/start_x.elf /dev/sdX1
 $ docker cp <container_id>:<chemin_fixup_x.elf>/fixup_x.dat /dev/sdX1
 ````  

 Il faut finalement modifier le fichier `config.txt` de la première partition de la carte SD pour ajouter :  
 
 ```` start_x=1
 gpu_mem=128
 ````  

 On en profite pour rajouter la communication SSH, utile pour du débug à l'avenir, en créant un fichier vide à la racine de la première partition :
 
 ```` $ touch ssh
 ````  

## Modifier les fichiers du Root File System de la carte SD

Dans notre implémentation, il peut être intéressant de rendre l'adresse IP de la raspberry statique afin de ne pas se tromper à l'avenir. Nous nous placerons dans cet exemple dans une communication ethernet sur le réseau privé 192.168.1.X mais cet exemple est adaptable au réseau wifi à condition qu'il n'y ait pas de whitelist en vigueur sur le réseau. Pour se faire, on modifie le fichier */etc/network/interfaces* de la manière suivante :

Ouvrir le fichier :

```` $ sudo nano /etc/network/interfaces
````
remplacer

```` iface eth0 inet dhcp
````
par

```` iface eth0 inet static

address 192.168.1.x

netmask 255.255.255.0

network 192.168.1.0

gateway 192.168.1.1
````

Il est possible de faire la même chose pour un réseau wifi en remplaçant *eth0* par *wlan0*.


## Copier les fichiers du projet sur la carte SD

Les fichiers du projet sont disponibles en stand alone sur le dépôt git suivant :

```` $ git <chemin vers dossier git> DEPOT_GIT
````

Il ne reste plus qu'à les déposer sur le dossier home du RFS de la raspberry à l'aide de la commande `cp`. Le dossier contient notamment deux sous-dossiers `SER2` et `V4L2` correspondant respectivement aux codes de contrôle des servomoteurs et de la caméra. Nous copions ces deux dossiers dans le dossier `home` de la Raspberry :

```` $ cp <chemin vers dossier git>/SER2 /dev/sdX2/home/
$ cp <chemin vers dossier git>/V4L2 /dev/sdX2/home/
````

Le code de contrôle des servomoteurs étant implémenté en python, il est déjà prêt à l'emploi. Celui pour la caméra est en C et doit donc être compilé à l'aide de l'autotools `autoconf` :

````
$ cd ./V4L2
$ ./autogen.sh          # Crée les fichiers d'autotool
$ ./configure CC=~/buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc --host=arm-buildroot-linux-uclibcgnueabihf --build=linux     # Crée le makefile pour compiler
````

Le code fourni originellement par autoconf n'est pas fonctionnel, il faut pour cela modifier le fichier config.h : en remplaçant `#define HAVE_MALLOC 0` par `#define HAVE_MALLOC 1` et en commentant `#define malloc rpl_malloc`.
Il ne reste plus qu'à compiler le code :

```` make install
````

La carte SD est alors correctement configurée et peut être mise dans le port de la raspberry. On connectera alors la raspberry à l'ordinateur client par Ethernet (ou au réseau wifi selon le choix effectué à l'étape 5).

Il reste à rajouter le script de service du projet pour lancer les serveurs de gestion caméra et servomoteurs automatiquement au lancement de la raspberry. Pour cela, copier le fichier *S98v4l2grab* dans `/etc/init.d` à l'aide de la commande `cp`.



# Paramètres par défaut pour se connecter à la raspberry

- Username : user - Password : user1* - IP address : 192.168.1.10

Au besoin, on peut changer l'adresse statique PC client avec la commande suivante, où *x* est compris entre 2 et 254, 10 exclu dans le cas où vous avez effectuée l'installation rapide puisqu'il s'agit de l'adresse de la raspberry) :  

```` ifconfig eth0 192.168.1.x
````



# Utilisation du projet  

Pour utiliser le projet une fois l'installation faite, il faut tout d'abord se connecter par câble ethernet à la Raspberry. Ensuite, il faut attribuer à son hôte (ordinateur) une adresse IP dans la même classe que celle de la Raspberry en utilisant ifconfig. Par exemple: 

```` $ sudo ifconfig [nom interface réseau] 192.168.1.11
````

Il convient de se connecter en ssh (mot de passe: `user1*` ) pour lancer le serveur du servomoteur:

```` $ ssh user@192.168.1.10
````

Il faudra passer en super utilisateur avec la commande su (mot de passe: `root1*` ), nécessaire pour utiliser les GPIO.
Enfin, il faut lancerle serveur avec la commande suivante:

```` $ python /home/user/SER2/server_servo.py
````

Le serveur de la caméra se lançant au démarrage, il n'y a rien a faire de ce côté!

Dans un nouveau terminal, il suffira de lancer le client python pour voir apparaitre une interface graphique sous Tkinter.
Celle-ci a deux onglets, le premier gère les commandes pour le servomoteur. Il faut fixer une valeur d'angle, puis cliquer sur le bouton pour l'envoyer au serveur.
L'autre onglet s'occupe de la caméra. En appuyant sur le bouton, on récupère dans le cadre en dessous une image de la caméra.

Il est toutefois important de noter que les serveurs ne supporte pas la perte de leur client. Dans le cas échéant, ils n'accepteront aucun autre client. Il faudra soit redémarrer la Raspberry et reprendre les étapes du début (Recommandé), soit éteindre les deux serveurs et les relancer à la main.

# Si ce qui précède échoue

## Erreur d'identification sur la raspberry

On peut récupérer les identifiants par défaut de la Raspberry en explorant le fichier *users.tables* à l'aide de la commande `cat`. A priori, le couple est `user/user1*`.

```` ~/buildroot-precompiled-2017.08# cat users.tables user -1 users_group -1 =user1* /home/user /bin/sh -
````

## Erreur de communication entre le client et le serveur caméra

Ouvrir un nouveau terminal pour se connecter à la raspberry en SSH depuis le PC client :

```` $ sudo ssh user@192.168.1.10
````

Ouvrir le fichier de log `syslog`

Relancer le code client depuis un autre

## Erreur de connexion Ethernet
On va alors se connecter à la raspberry via le port série.
Pour cela, insérer la carte SD dans la Raspberry et connecter le port série au PC client. Depuis le PC client, se positionner dans le répertoire /dev avec Nautilus :  

```` $ nautilus /dev
````

On allume la Raspberry et on récupère l'identifiant *ttyUSBX* qui apparait.
On va ensuite configurer ce port série avec GTKTerm. Si besoin, on l'installe et le lance avec les commandes suivantes :

 ```` $ sudo apt-get install gtkterm
 $ sudo gtkterm
 ````

Dans la page de configuration on sélectionne comme paramètres de GTKTerm :

- Baud rate: 115200-8N1
- Port : /dev/<ttyUSBX>

Une fois les paramètres rentrés, on peut redémarrer la raspberry. La raspberry va alors envoyer pendant son démarrage les informations relatives au lancement des scripts de services. Si les deux serveurs se lancent correctement au démarrage, les lignes suivantes doivent apparaître sur le terminal GTKTerm :

```` Starting video capture            # Lancement du service
Starting /dev/video0              # Lancement de la caméra
Starting v4l2grab server          # Lancement du serveur caméra
Starting servo handling server    # Lancement du serveur servomoteurs #non implémentée
OK                                # Etat du lancement du service
````
Toute variation de cette chaîne de caractères dans le terminal GTKTerm signifie une erreur du lancement du service.

Il est par la suite possible de se connecter à distance au terminal de la Raspberry. Le système nous demande pour cela un nom d'utilisateur et un mot de passe. On lui fournit le couple récupéré à l'étape précédente. Une fois connectés, on récupère l'adresse IP de la Raspberry avec la commande `ifconfig`.
On vérifie l'adresse IP de l'interface *eth0* (192.168.1.10 à priori).

Si l'adresse fournie est erronée, on peut la changer en IP statique à distance en modifiant le fichier de configuration réseau */etc/network/interfaces* comme décrit plus haut.
