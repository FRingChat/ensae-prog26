from graph import Graph


class Network:
    """
    Class for a network that represents the environment (with length and fatigue on roads).
    """

    def __init__(self, roads={}, start=None, end=None):
        """
        Initializes the network from a dictionary roads.

        Parameters:
        -----------
        roads: dict
            A dictionary of the roads as an adjacency list, that is
            roads[u] = list of (v, length, fatigue)
            Ex: roads = {v0: [(v1, 21, 2), (v2, 12, 4)],
                        v1: [(v0, 74, 2), (v2, 32, 1)],
                        ...}
        start, end:
            Start and end nodes added as attributes
        """
        self._roads = roads
        self.start = start
        self.end = end

    def __str__(self):
        """
        Prints the network as text.
        """
        output = f"A network with {len(self._roads)} nodes and the following adjacency list:\n"
        return output+self._roads.__str__()

    @classmethod
    def from_file(cls, filename: str):
        """
        Creates a Network from an environment file.

        File format: one edge per line (start end length fatigue).
        """
        # Initialize adjacency list
        roads = {}

        with open(filename, "r") as testcase:
            nb, start, end = testcase.readline().strip().split()
            for _ in range(int(nb)):
                i, j, lo, f = testcase.readline().strip().split()
                lo, f = int(lo), int(f)
                roads.setdefault(i, []).append((j, lo, f))
                roads.setdefault(j, [])

        return cls(roads=roads, start=start, end=end)

    def neighbours(self, sommet):
        """ Renvoie les voisins d'un sommet sous forme de liste """
        if sommet not in self._roads:
            return []
        return self._roads[sommet]

    def build_simple_graph(self):
        """
        Builds an object of type Graph from the network, by ignoring the fatigue coefficient.
        """
        # TODO: implement the method
        # raise NotImplementedError

        # On enlève la fatigue des chemins
        roads = self._roads
        edges = {}
        for elt in roads.keys():
            edges[elt] = []

            for road in roads[elt]:
                arr, long, fatigue = road
                edges[elt].append((arr, long))

        simple_graph = Graph(edges)
        return simple_graph

    def build_extended_graph(self):
        """ Créé un Graph depuis Network qui prend en compte la fatigue """
        roads = self._roads
        edges = {}

        for elt in roads.keys():
            edges[elt] = []

            for road in roads[elt]:
                arr, long, fatigue = road
                # On met la fatigue avec la longueur, ainsi nous avons bien un graph
                # Il n'y a qu'à séparer la longueur de la fatigue dans la méthode
                # longueur() du module Graph pour adapter shortest_path
                edges[elt].append((arr, (long, fatigue)))

        extended_graph = Graph(edges)
        return extended_graph

    # -------------------------------------------------------------------------------------------
    # Partie 1.3 ( à notre sauce )
    # -------------------------------------------------------------------------------------------

    def longueur_chemin(self, chemin):
        """ Renvoie la longueur d'un chemin, en prennant en compte la fatigue s'il y en a """
        lon = 0
        fatigue = 1
        if len(chemin) >= 2:
            for i in range(len(chemin)-1):
                # longueur est de forme [ longueur du segement , fatigue sur ce segment]

                for arrivee in self.neighbours(chemin[i]):
                    nom, longueur_i, fatigue_i = arrivee
                    if nom == chemin[i+1]:
                        longueur, fat = longueur_i, fatigue_i
                    
                lon += longueur * fatigue

                # La fatigue arrive après avoir marché, on l'incrémente donc à la fin du segment
                fatigue += fat
        return lon

    def shortest_path(self, depart, arrivee, chemin=[], chemin_trouve=[]):
        """ Renvoie une liste de tous les points traversés pour aller le
        plus rapidement possible du départ à l'arrivée. Soit une liste de forme :
        [ Départ , Etape 1 , Etape 2 , ... , Etape N , Arrivée ]"""

        if depart not in chemin:
            nouveau_chemin = chemin + [depart]
            print(len(chemin))

            if self.longueur_chemin(chemin) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                # On explore les voisins s'ils sont plus courts que ceux qu'on a déjà trouvé
                for point in self.neighbours(depart):
                    point, _, _ = point

                    if point == arrivee:  # Si on a trouvé l'arrivée
                        chemin_trouve = nouveau_chemin + [point]
                    else:  # Sinon on continue de chercher
                        exploration = self.shortest_path(point, arrivee, nouveau_chemin, chemin_trouve)
                        # On vérifie que l'exploration a donné un chemin optimal
                        if self.longueur_chemin(exploration) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                            chemin_trouve = exploration

        return chemin_trouve


test = Network.from_file("examples/medium-largefatigue.txt")
# test1 = test.build_extended_graph()
# test2 = test.build_simple_graph()
# print(test2.shortest_path('lozere', 'saclay'))
# print(test1.shortest_path('lozere', 'saclay'))

print(test.shortest_path('v0', 'v7'))
