# Projet de programmation
###### *Félix Ringuet-Chatelier & Tony Magyar*

## **Description du projet**
A partir de plusieurs informations stockées dans un fichier texte décrivant un graph orienté, ce script calcule le chemin optimal pour relier deux points.
Chaque chemin allant d'un point A à un point B contient une distance et un coefficient de fatigue. La fatigue s'accumule au fur et à mesure et fait augmenter le ressenti de distance, de sorte que `distance_ressentie = distance *(1 + fatigue_cumulee)`, où `fatigue_cumulee` est la somme des fatigues des chemins parcourus jusque ici.

## *Structure du script*
### graph.py
Défini une classe **Graph** fondée sur un dictionnaire 'edges' accessible par la méthode `self.edges`.
Pour chaque point d'un graph, 'edges' associe une liste de points auquels celui-ci est connecté, ainsi qu'un deuxième paramêtre associé à la longueur.
Par exemple, si **A** est relié à **B** avec une distance de 12 et à **C** avec une distance de 30, `edges[A] = [(B, 12),(C,30)]`. 
Voici les méthodes définies pour une instance de classe **Graph**:
##### `graph.neighbours(node)`
Renvoie les voisins d'un point ('node') sous forme de liste. La liste est vide si le point n'a pas de voisin.
##### `graph.longueur(depart, arrivee)`
Renvoie une liste de forme `[longueur, fatigue]` où `longueur` est la longueur entre le départ et l'arrivée, et `fatigue` est la fatigue gagnée sur ce parcours. Les paramêtres 'depart' et 'arrivee' doivent être des points du graph connectés entre eux.
##### `graph.longueur_chemin(chemin)`
Renvoie la longueur ressentie pour parcourir un chemin, ou un chemin est une liste de points voisins.
##### `graph.shortest_path(depart, arrivee)`
Renvoie le chemin ayant la longueur ressentie la plus courte allant du départ à l'arrivée. `depart` et `arrivee` sont des noms de points du graph.

### network.py
Défini un graph ayant de la fatigue sur ses arrètes. Chaque arrète, que nous appellons chemin, sont associé à un sommet qui sert de départ, et est de forme `(arrivée, longueur, fatigue)`. La fatigue est fixée à 1 au départ, et influence le ressenti d'une distance en servant de coefficient à la longueur d'un chemin. Ainsi `longeur_ressentie = longueur * fatigue`. La fatigue s'accumule à la fin de chaque chemin parcouru.
Voici les différentes méthodes définies pour une instance de classe **Network**:
##### `network.from_file(file)`
Converti un document texte en un dictionnaire définissant un graph avec de la fatigue sur ses arrètes.
##### `network.build_simple_graph()`
Transforme un network en graph, lui donnant l'accès aux methode de l'instance **Graph**. Cependant, ce passage fait perdre les information de fatigue.
##### `network.build_extended_graph()`
Transforme lui aussi un network en graph, mais en stockant le paramêtre de fatigue avec celui de longueur sous forme de tuple. Une arrète est donc de forme `(arrivée, (longueur, fatigue))`. Cela permet à la methode `shortest_path` de prendre en compte la fatigue dans le calcul d'un chemin optimal.
##### `network.neighbours(node)`
Renvoie les voisins d'un point ('node') sous forme de liste. La liste est vide si le point n'a pas de voisin.
##### `network.longueur_chemin(chemin)`
Calcule la distance ressentie d'un chemin, en prennant en compte la fatigue s'il y en a.
##### `network.shortest_path_network(depart, arrivee)`
Equivalent de la methode `shortest_path` de la classe **Graph**. L'objectif est de gagner du temps par rapport à cette autre methode en ne transformant pas le network en graph, et en l'utilisant sous sa forme brute. Cependant, cette méthode reste assez lente.
##### `network.A_etoile(depart, arrivee)`
Exactement le même objectif que la methode `shortest_path` mais en fonctionnant de manière itérative plutôt que récursive. Cette méthode est beaucoup plus rapide, et renvoie un tuple de forme `(chemin, longueur_totale, fatigue_finale)`.
#### *Extensions*
##### `network.missions_multiples(liste_missions)`
Cette première extension gère plusieurs missions à la suite pour un seul agent. Par mission nous entendons un chemin entre un point de départ et d'arrivée.
##### `network.point_de_reposV1()`
Cette extension est une première approche du problème du point de repos. L'idée est de placer sur le graph un point de repos qui réinitialise la fatigue lorsqu'on y passe. Dans cette première version, on évalue quel point de repos est optimal pour chaque chemin possible du graph, et on lui ajoute un vote. A la fin, on garde le point de repos ayant le plus de vote. Cette methode est très longue à executer, car il y a `n!` chemins à évaluer, et `n` points de repos à tester.
##### `network.point_de_repos()`
Cette deuxième version à le même objectif, mais utilise une methodologie différente pour être plus rapide. En effet, précedement nous devions lancer la fonction `A_etoile` `n * n!` fois car chaque point de repos modifiait un peu le graph. Ici, on évalue le temps cumulé de tous les chemins du graph pour chaque point de repos. Cela fait gagner du temps car on commence par fixer le point de repos, ce qui permet de créer un dictionnaire de prunning global sur le graph de ce point. Ce dictionnaire est donné à la fonction `A_etoile` ce qui lui épargne des branches de calcul. Cepndant, il reste toujours autant de points et de chemins, donc cette extension reste aussi assez lente.

## *Tests*
Pour chaque methode définie ci-dessus, il existe un test, rangé dans le dossier **Tests**, qui vérifie le bon fonctionnement de la methode.

## *Exemples*
C'est dans ce fichier que sont stockés tous les network/graph sous forme de fichiers texts. 
