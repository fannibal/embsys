# Readme code contrôle de la caméra

Ce code est basé sur le code du driver v4l2grab développé par .. (dépôt  github : ...) basé sur la librairie V4l2 (Video for Linux 2).

Le readme se décompose de la manière suivante :

1. Fonctionnement global du code
2. Utilisation par un programme tiers
3. Fonctionnalités supplémentaires/modifications apportées au code originel
4. Exemple d'utilisation en ligne de commande
5. Limitations et perspectives

## Fonctionnement global du code

Ce programme est un serveur communiquant les informations fournies par la caméra embarquée de la Raspberry pi à un programme client par le biais d'un socket. La communication avec un programme tiers se déroule de la manière suivante :

- Initialisation de l'appareil de capture photo
- Initialisation du serveur de communication
- Attente de connexion d'un client
- Attente du message d'un client.
  - Si le client envoie 'q' : fin de transmission, fermeture du socket et fermeture du programme.
  - Sinon, envoi d'une image au client.

## Utilisation par un programme tiers

Le client peut se connecter au serveur quelque soit son adresse IP à partir du moment où les deux appartiennent au même réseau. L'adresse du serveur est celle de la Raspberry (192.168.0.10 par défaut) et le port est modifiable par l'utilisateur lors du lancement du serveur avec l'argument  -p (5000 par défaut).
Une fois la connexion établie, le serveur attribue au client un socket de communication non nommé et attends un message de celui-ci. La longueur de ce message ne doit pas excéder un caractère. Le serveur interprète n'importe quel caractère à l'exception du 'q' (pour "quitter") comme une requête du client pour lui envoyer une photo. A la fin de l'envoi d'une photo, le serveur se met en attente du prochain caractère.
L'envoi d'une photo se fait par ligne complète de pixels, soit 640 caractères stockés sur 1 octet suivis d'une fin de chaîne "\0". Les dimensions finales de l'image sont de 480*640*3 au format YUV444.
Le format YUV444 se décompose en 3 couches : la luminance Y, la chrominance bleue Cb/U et la chrominance rouge Cr/V. Ici, seule la première couche est conservée pour la transmission.
Enfin, la réception d'un caractère "q" signifie la fin de transmission. Le serveur va alors libérer le socket et sortir de la boucle.
Le serveur libère alors la mémoire allouée à la capture des images et le programme s'arrête.

## Exemple d'utilisation en ligne de commande

````
./v4l2grab -d /dev/video0 -p 5000
````

## Fonctionnalités supplémentaires/modifications apportées au code originel

- Communication avec le client par sockets.
- Envoi de l'image captée par socket au lieu de l'écrire au format jpeg dans le dossier courant.
- Gestion du port de communication par argument de la fonction main.
- Mise à jour des arguments courts et longs de la fonction main et de l'affichage de l'aide.
- Attentes consécutives de plusieurs caractères du client pour envois d'images.
- Lancement du serveur et du module *modprobe* au démarrage de la Raspberry (voir `/etc/init.d/S98v4l2grab`).
- Communication des erreurs éventuelles et des messages informatifs au system log.
- Gestion du signal SIGINT pour fermer le socket proprement lors de la réception d'un ctrl-C.
- Nettoyage des parties du code devenues inutiles.

## Limitations et perspectives

- Passer à des images couleur.
- Gérer la déconnexion client.
- Gérer le multiclients par multithreading de la fonction main.
- Passer à un flux de photos en continu.
