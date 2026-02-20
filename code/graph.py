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
        # Longueur entre deux points
        liste_route = self._edges[depart]
        for route in liste_route:
            arr, long = route
            if arr == arrivee:
                return int(long)
    
    def longueur_chemin(self, chemin):
        # longueur d'un chemin
        lon = 0
        if len(chemin) >= 2:
            for i in range(len(chemin)-1):
                lon += self.longueur(chemin[i], chemin[i+1])
        return lon

    def shortest_path(self, depart, arrivee, chemin=[], chemin_trouve=[]):
        if depart not in chemin:
            nouveau_chemin = chemin + [depart]

            if self.longueur_chemin(chemin) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                # On explore les voisins
                for point in self.neighbours(depart):
                    point, on_sen_fout = point

                    if point == arrivee:  # Si on a trouvé l'arrivée
                        chemin_trouve = nouveau_chemin + [point]
                    else:  # Sinon on continue de chercher
                        exploration = self.shortest_path(point, arrivee, nouveau_chemin, chemin_trouve)
                        # On vérifie que l'exploration a donné un chemin optimal
                        if self.longueur_chemin(exploration) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                            chemin_trouve = exploration

        return chemin_trouve
