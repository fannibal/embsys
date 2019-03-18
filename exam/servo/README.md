#Manipulation du serveur

Le serveur est lancé avec la commande `python server.py` lancée depuis l'emplacement de ce fichier.
Le serveur écoute alors les clients.

#Fonctionnement du code

- On commence par importer les librairies nécessaires.

- On définit ensuite un gestionnaire de signaux; celui-ci est important car toute interruption anormale du programme va passer par lui. Le gestionnaire de signaux se compose d'une ou plusieurs fonctions (ici, une) que l'on associe à des signaux prédéfinis pour "personnaliser" ce que retourne le système.

- On configure ensuite les variables nécessaires au bon fonctionnement du code (IP, caractéristiques des buffers, etc).

- La fonction `setAngle`, comme son nom l'indique, permet de régler l'angle du servomoteur; elle est appelée lors de la réception de données depuis le client.

- A noter ligne 45 la mise en place d'un arrêt de fonctionnement du serveur au bout de deux minutes, par principe de ne pas laisser "tourner dans le vide".

- L'écoute en elle-même est réalisée de telle sorte que le buffer reçu est analysé, ses données récupérées et appelant la fonction setAngle si elles le permettent.

- En fin de programme, on s'assure de bien refermer toutes les connexions et ports ouverts.

