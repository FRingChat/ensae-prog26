# Projet de programmation
####### *Félix Ringuet-Chatelier & Tony Magyar*

## **Description du projet**
A partir de plusieurs informations stockées dans un fichier texte décrivant un graph orienté, ce script calcule le chemin optimal pour relier deux points.
Chaque chemin allant d'un point A à un point B contient une distance et un coefficient de fatigue. La fatigue s'accumule au fur et à mesure et fait augmenter le ressenti de distance, de sorte que 'distance_ressentie = distance *(1 + fatigue_cumulee)', où 'fatigue_cumulee' est la somme des fatigues des chemins parcourus jusque ici.

## *Structure du script*
### graph.py
Défini une classe **Graph** fondée sur un dictionnaire 'edges' accessible par la méthode 'self.edges'.
Pour chaque point d'un graph, 'edges' associe une liste de points auquels celui-ci est connecté, ainsi qu'un deuxième paramêtre associé à la longueur.
Par exemple, si **A** est relié à **B** avec une distance de 12 et à **C** avec une distance de 30, 'edges[A] = [(B, 12),(C,30)]'
Voici les méthodes définies pour une instance de classe **Graph**:
##### 'graph.neighbours(node)'
Renvoie les voisins d'un point ('node') sous forme de liste. La liste est vide si le point n'a pas de voisin.
##### 'graph.longueur(depart, arrivee)'
Renvoie une liste de forme '[ longueur entre le départ et l'arrivée , la fatigue gagnée sur ce parcours ]'. Les paramêtres 'depart' et 'arrivee' doivent être des points du graph connectés entre eux.
##### 'graph.longueur_chemin(chemin)'
Renvoie la longueur ressentie pour parcourir un chemin, ou un chemin est une liste de points voisins.
##### 'graph.shortest_path(depart,arrivee)'
Renvoie le chemin ayant la longueur ressentie la plus courte allant du départ à l'arrivée. 'depart' et 'arrivee' sont des noms de points du graph.

### network.py
Converti un document texte en un dictionnaire définissant
