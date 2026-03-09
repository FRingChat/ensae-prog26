"""
This is the graph module. It contains the classes Graph and GraphImplicit
"""


class Graph:
    """
    A minimal class for directed weighted graph represented as adjacency list.

    Attributes:
    -----------
    edges: dict
        A dictionary that contains the list of neighbors of each node with its weight.
        Ex: edges = {v0: [(v1, 21), (v2, 12)],
                     v1: [(v0, 74), (v2, 32)],
                     ...}

    Methods:
    --------
    neighbours(self, node):
        Returns the list of all neighbors of a node
    """

    def __init__(self, edges):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def longueur(self, depart, arrivee):
        """ Renvoie une liste de forme :
        [ longueur entre le départ et l'arrivée , la fatigue gagnée sur ce parcours ]"""
        liste_route = self._edges[depart]
        for route in liste_route:
            arr, long = route
            if arr == arrivee:
                if isinstance(long, tuple):
                    # Si on a un graph étendu, on sépare la longueur de la fatigue
                    long, fatigue = long
                else:  # Sinon on fixe la fatigue à zéro sur ce segment
                    fatigue = 0
                return [int(long), fatigue]

    def longueur_chemin(self, chemin):
        """ Renvoie la longueur d'un chemin, en prennant en compte la fatigue s'il y en a """
        lon = 0
        fatigue = 1
        if len(chemin) >= 2:
            for i in range(len(chemin)-1):
                # longueur est de forme [ longueur du segement , fatigue sur ce segment]
                longueur = self.longueur(chemin[i], chemin[i+1])
                lon += longueur[0]*fatigue

                # La fatigue arrive après avoir marché, on l'incrémente donc à la fin du segment
                fatigue += longueur[1]
        return lon

    def shortest_path(self, depart, arrivee, chemin=[], chemin_trouve=[]):
        """ Renvoie une liste de tous les points traversés pour aller le
        plus rapidement possible du départ à l'arrivée. Soit une liste de forme :
        [ Départ , Etape 1 , Etape 2 , ... , Etape N , Arrivée ]"""

        if depart not in chemin:
            nouveau_chemin = chemin + [depart]

            if self.longueur_chemin(chemin) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                # On explore les voisins s'ils sont plus courts que ceux qu'on a déjà trouvé
                for point in self.neighbours(depart):
                    point, _ = point

                    if point == arrivee:  # Si on a trouvé l'arrivée
                        chemin_trouve = nouveau_chemin + [point]
                    else:  # Sinon on continue de chercher
                        exploration = self.shortest_path(point, arrivee, nouveau_chemin, chemin_trouve)
                        # On vérifie que l'exploration a donné un chemin optimal
                        if self.longueur_chemin(exploration) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                            chemin_trouve = exploration

        return chemin_trouve


class GraphImplicit(Graph):

    def __init__(self, start):
        self._edges = {start: self.neighbours(start)}

    def ajouter(self, sommet):
        self._edges[sommet] = self.neighbours(sommet)
