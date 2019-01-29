TO DO : DESCRIPTION ETAPES BUILDROOT

# Installation buildroot + flashage raspberry :

## RPI

### Buildroot

Pour avoir le support de la caméra sur la RPI3, un firmware spécifique
doit être compilé avec Buildroot. Pour cela, il faut activer l'option
`BR2_PACKAGE_RPI_FIRMWARE_X` dans le fichier de configuration de Buildroot.

De plus, afin d'intéragir avec la caméra, l'API de
[V4L](https://linuxtv.org/downloads/v4l-dvb-apis/uapi/v4l/v4l2.html) est
conseillée. Il est donc nécessaire d'activer l'option `BR2_PACKAGE_LIBV4L`
dans le fichier de configuration Buildroot.

Votre système d'exploitation précompilé grâce à Buildroot est disponible
via une image Docker (comme lors des TPs):

````
$ docker pull pblottiere/embsys-rpi3-buildroot-video
````

Pour créer un conteneur:

````
$ docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash
docker# cd /root
docker# ls
buildroot-precompiled-2017.08.tar.gz
docker# tar zxvf buildroot-precompiled-2017.08.tar.gz
````

Le nécessaire pour flasher la carte RPI3 avec le support de la caméra est
alors disponible:

get sdX
````
sudo apt-get install nautilus
nautilus /dev
````
brancher débrancher adaptateur usb-SD -> get *sdX*

- `sdcard.img` à flasher sur la carte SD avec la commande `dd`
get .img from docker :
````
docker ps -a
````
-> get container_id
````
docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .
sudo dd if=sdcard.img of=/dev/<sdX>
````

- `start_x.elf` et `fixup_x.dat` à copier avec la commande `cp` sur la 1ère
  partition de la carte SD
in docker :
- start_x.elf
````
find . -name start_x.elf
````
-> get *position_start_x.elf*
````
docker cp <container_id>:<position_start_x.elf>/start_x.elf .
````
- fixup_x.dat
````
find . -name fixup_x.dat
````
-> get *fixup_x.dat*
````
docker cp <container_id>:<position_start_x.elf>/fixup_x.dat .
````
copy these two files unto the first partition of sd card

Il faut finalement modifier le fichier `config.txt` de la 1ère partition
de la carte SD pour ajouter:

````
start_x=1
gpu_mem=128
````

Se connecter à la rasp :
Paramètres par défaut :
Username : user
Password : user1*
IP adress : 192.168.1.10

changer adresse statique PC client :

````
ifconfig eth0 192.168.1.x			# x!=10
````












# (OPTIONNAL, IN CASE OF EMERGENCY)

````
~/buildroot-precompiled-2017.08# cat users.tables
user -1 users_group -1 =user1* /home/user /bin/sh -
````
-> get raspberry *username* and *password* (user/user1*)

put SD card in rasp and plug serial port :
PC client :
````
nautilus /dev
````
allumer rasp
-> get *ttyUSBX*

configuration port série (avec gtkterm)
````
sudo apt-get install gtkterm
sudo gtkterm
````
params : 115200-8N1, port : <ttyUSBX>
input <username> and <password>

````
ifconfig
````
-> check ip adress *eth0*, (192.168.1.10)

Ip statique rasp :
````
sudo nano /etc/network/interfaces
````
modifier (connexion ethernet)
````
iface eth0 inet dhcp 
````
par
````
iface eth0 inet static
 
address 192.168.1.x
 
netmask 255.255.255.0
 
network 192.168.1.0
 
gateway 192.168.1.1
````

Activer SSH:
ajouter fichier vierge "ssh" sur la racine de la première partition

Connexion SSH depuis pc client :
````
sudo ssh user@192.168.1.10
````








 






