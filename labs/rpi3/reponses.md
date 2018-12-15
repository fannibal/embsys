# Construction d'OS avec Buildroot et chaîne de cross-compilation

**Question 1**: 
`embsys_defconfig` : fichier de configuration du kernel pour la compilation.
- `busybox.config` : fichier de configuration du busybox, qui est un logiciel permettant de rajouter des commandes standard sous Unix. Souvent utilisé pour l'embarqué pour sa compacité et sa transparence sur les utilitaires ajoutés.
- `users.table` : la table répertoriant les utilisateurs. Il contient la ligne suivante:

````
user -1 users_group -1 =user1* /home/user /bin/sh -
````

**Question 2**: 

il faudrait utiliser `raspberrypi3_defconfig`. 

**Question 3**: 

Il contient toutes les librairies installées. Chaque librairie contient possiblement des patchs, un fichier de config `.in` créé par buildroot, une table de `hash`, et un fichier `mk`.

**Question 4**: 

La commande permet,dans cette ordre, de:
- faire un fichier `lxdialog` le temps de la compilation
- compiler ce fichier par gcc en se servant de la configuration de buildroot(la compilation regarde dans `/root/buildroot-precompiled-2017.08/support/kconfig` et `/root/buildroot-precompiled-2017.08/output/build/buildroot-config`)

**Question 5**: 

- Architecture matérielle cible: ARM (little Endian)
- CPU cible: cortex A-53
- ABI: EABIhf (supporte le modèle `hard floating point`)
- librairie C utilisé: uClibc-ng
- version cross-compilateur: gcc 6.X
- version kernel: Custom git repository kernel

**Question 6**: 

L'option est activé dans `target packages/Networking applications`. Openssh sera compilé. Dans embsys_defconfig: `BR2_PACKAGE_OPENSSH=y`.

**Question 7**: 

Comme dit précédement, busybox est un logiciel permettant de rajouter des commandes standard sous Unix. La commande permet, à l'instar de buildroot, de créer une interface utilisateur. Cela permet de paramétrer plus finement le fonctionnement des utilitaires fournies par busybox.

**Question 8**: 

Le contenu de `output/host` est:
````
drwxr-xr-x  6 root root  4096 Nov 25 12:13 arm-buildroot-linux-uclibcgnueabihf
drwxr-xr-x  2 root root 12288 Dec 15 20:07 bin
drwxr-xr-x  3 root root  4096 Nov 25 12:22 doc
drwxr-xr-x  3 root root  4096 Nov 25 12:34 etc
drwxr-xr-x 16 root root  4096 Nov 25 13:03 include
drwxr-xr-x  7 root root  4096 Nov 25 13:04 lib
drwxr-xr-x  3 root root  4096 Nov 25 11:24 libexec
drwxr-xr-x  3 root root  4096 Nov 25 12:34 man
drwxr-xr-x  2 root root  4096 Nov 25 12:45 sbin
drwxr-xr-x 18 root root  4096 Nov 25 12:34 share
lrwxrwxrwx  1 root root     1 Nov 25 11:14 usr -> .
````
Ce qui correspond aux binaires, à la documentation, etc (fichiers de configuration), les headers, les librairies, le manuel et un pointeur sur ce même répertoire. Cela correspond à ce que l'on peut trouver dans un OS.

arm-linux-gcc est le binaire exécutable du compilateur gcc résultant de la cross-compilation.

**Question 9**: 

file détermine le type de fichier et ces paramètres. Ici, cela donne l'architecture définit pendant la compilation.
Faire `./hw` lance l'exécutable, et affiche `Hello World!`.

**Question 10**: 

Avec le gcc compilé, la commande `file` donne:
````
hw: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-uClibc.so.0, not stripped
````
le fichier n'est plus défini de la même façon (32bit vs 64, executable vs shared object, ARM, interpréteur différent).
Tenter d'exécuter le fichier donne:
````
bash: ./hw: cannot execute binary file: Exec format error
````
Cela vient des différences énoncés plus tôt: l'interpréteur ne sait pas lire le fichier compilé par cross-compilation.

**Question 11**: 

Le contenu de `output/images` est:
````
-rw-r--r-- 1 root root     17624 Nov 25 13:03 bcm2710-rpi-3-b.dtb
-rw-r--r-- 1 root root     16380 Nov 25 13:03 bcm2710-rpi-cm3.dtb
-rw-r--r-- 1 root root  33554432 Nov 25 13:04 boot.vfat
-rw-r--r-- 1 root root 209715200 Nov 25 13:04 rootfs.ext2
lrwxrwxrwx 1 root root        11 Nov 25 13:04 rootfs.ext4 -> rootfs.ext2
-rw-r--r-- 1 root root  95907840 Nov 25 13:04 rootfs.tar
drwxr-xr-x 3 root root      4096 Nov 25 12:45 rpi-firmware
-rw-r--r-- 1 root root 243270144 Nov 25 13:04 sdcard.img
-rw-r--r-- 1 root root   4566832 Nov 25 13:03 zImage
````
- rootfs.tar: `root file system` compressé.
- zImage: image compressée du noyau Linux.
- sdcard.img: image de la carte SD
L'avantage de ces fichiers est d'être compressés, donc facile à copier ou récupérer en cas de problèmes potentiels (ex:corruption de la carte).

**Question 12**: 

Pour zImage:
````
zImage: Linux kernel ARM boot executable zImage (little-endian)
````
Pour sdcard.img:
````
sdcard.img: DOS/MBR boot sector; partition 1 : ID=0xc, active, start-CHS (0x0,0,2), end-CHS (0x4,20,17), startsector 1, 65536 sectors; partition 2 : ID=0x83, start-CHS (0x4,20,18), end-CHS (0x1d,146,54), startsector 65537, 409600 sectors
````

**Question 13**: 

Il contient le `root file system` décompressé.


# QEMU


**Question 1**: 

`--cap-add` permet dans le mode privilège d'ajouter des permissions supplémentaires à l'utilisateur.

**Question 2**: 

`chroot` permet de changer la racine d'execution d'un processus, ce qui l'empêche d'avoir accès à autre chose que son nouveau RFS. Cela permet à la fois de sécuriser l'exécution du processus en limitant ses accès, et permet de faire tourner plusieurs instances d'un même processus.

**Question 3**: 
Le programme s'est bien exécuter. L'environnement de la raspberry a été émulé, ce qui a permit d'executer le programme avec la bonne architecture.








