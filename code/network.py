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


test = Network.from_file("examples/small.txt")

test = test.build_extended_graph()

print(test.shortest_path('lozere', 'saclay'))
