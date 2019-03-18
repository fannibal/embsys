# Client communiquant avec les deux serveurs

Ce code fonctionne avec quatres outils : l'interface graphique Tkinter, le multi-threading, la gestion des signaux et la librairie socket pour les clients. Il y aura donc trois partie :

1. La gestion des signaux
2. l'initialisation de l'interface
3. la gestion de la communication client-serveurs

## Gestion des signaux

De par la librairie signal, il est possible de facilement gérer les signaux tel que `CTRL-C`. Actuellement, cette partie est assez limité: elle ne fait qu'un `sys.exit()`, ce qui est mieux que le comportement par défaut, mais reste perfectible.
Pour utiliser la gestion d'interuptions, une fonction est appellée par le programme lorsque l'interruption associée est appelé. Ici, `SIGINT` et `SIGTERM`.

## Initialisation de l'interface

Le `main` va dans un premier temps démarrer l'interface graphique. Il s'agit d'un objet `Tk()` créé en global, puis passer aux deux clients pour qu'ils puissent intéragir plus facilement.

Elle est composée de deux onglets. Le premier est composé d'un bouton et d'une échelle réglable entre 0 et 180, correspondant aux angles que le servomoteur peut avoir.
Le deuxième onglet contient un bouton, un Canvas (objet permettant l'affichage d'image), ainsi que d'un label (objet permettant l'affichage de texte). Ce dernier n'est utile qu'en cas de mauvaise transmission de donnée entre le serveur caméra et le client correspondant.

## Gestion de la communication client-serveurs

La majeur partie du code est tournée sur cet aspect ci.
Deux threads sont lancées, chacune correspond à un serveur. Elles se départagent par une valeur définissant leur type, l'adresse et le port du serveur.
Une méthode `close_s` a été implémenté pour gérer la fin de la communication avec les serveurs.
Les boutons précédemments présentés sont associés à une méthode `Callback` qui permet la communication avec les serveurs. La méthode `run`, appelée en boucle, est vide car le programme n'effectue une action que sur demande du client, donc pendant les `Callback`.

La partie communication du `Callback` dépend de la thread étudiée.
- Le client du servomoteur récupère la valeur de l'échelle, et l'envoie au serveur.
- Le client de la caméra envoie un caractère (par exemple `i`) au serveur, ce qui déclenche la capture d'une image par la caméra, puis sont envoi au client. Celui-ci concatène les bytes reçus, les transformant ainsi en entiers. Cette liste d'entier est ensuite découpé selon les différents canaux, bien que seul le premier nous intéresse. ce premier canal est ensuite mis sous forme de matrice aux bonne dimensions, puis afficher dans le Canvas.
