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

    # -------------------------------------------------------------------------------------------
    # Partie 1.1
    # -------------------------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------------------------
    # Partie 1.2
    # -------------------------------------------------------------------------------------------

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

    def neighbours(self, sommet):
        """ Renvoie les voisins d'un sommet sous forme de liste """
        if sommet not in self._roads:
            return []
        return self._roads[sommet]

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

    def shortest_path_network(self, depart, arrivee, chemin=[], chemin_trouve=[]):
        """ Renvoie une liste de tous les points traversés pour aller le
        plus rapidement possible du départ à l'arrivée. Soit une liste de forme :
        [ Départ , Etape 1 , Etape 2 , ... , Etape N , Arrivée ]"""

        if depart not in chemin:
            nouveau_chemin = chemin + [depart]
            # print(len(chemin))

            if self.longueur_chemin(chemin) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                # On explore les voisins s'ils sont plus courts que ceux qu'on a déjà trouvé
                for point in self.neighbours(depart):
                    point, _, _ = point

                    if point == arrivee:  # Si on a trouvé l'arrivée
                        chemin_trouve = nouveau_chemin + [point]
                    else:  # Sinon on continue de chercher
                        exploration = self.shortest_path_network(point, arrivee, nouveau_chemin, chemin_trouve)
                        # On vérifie que l'exploration a donné un chemin optimal
                        if self.longueur_chemin(exploration) <= self.longueur_chemin(chemin_trouve) or chemin_trouve == []:
                            chemin_trouve = exploration

        return chemin_trouve

    # -------------------------------------------------------------------------------------------
    # Partie 2
    # -------------------------------------------------------------------------------------------

    def A_etoile(self, depart, arrivee, temps_init=0, fatigue_init=1, extension_repos = ''):
        """
        Renvoie le chemin de temps minimal, ainsi que le temps final et la fatigue finale.

        Nous avons implémenté dans ce script une methode de Pruning grâce au
        dictionnaire temps_min, qui catalogue uniquements les chemins qui sont
        intéressants.

        Extensions : pour adapter ce script aux missions intermédiaires, nous 
        avons rajouté les paramêtres temps_init et fatigue_init et modifié A* pour 
        les implémenter, ainsi que le paramêtre point_repos
        """

        # On initialise la liste de points à visiter avec le temps et la 
        # fatigue passés en paramètres
        a_visiter = [(temps_init, fatigue_init, depart, [depart])]

        # On créé un dictionnaire qui rescense les chemins les plus courts entre le
        # point de départ et les autres points 
        # (Extension) On rajoute le paramêtre de fatigue dans le dictionnaire car il fait varier 
        # la rapidité des chemins
        prunning = {(depart, fatigue_init): temps_init}
        
        # (Extension) On rajoute les chemins qu'on a déjà exploré dans le 
        # programme point de repos pour accélerer le processus (c'était super
        # long sinon)
        if extension_repos != '':
            point_repos, dico_repos = extension_repos
            prunning.update(dico_repos)

        while len(a_visiter) > 0:

            # On regarde le chemin le plus court en premier
            a_visiter.sort(key=lambda x: x[0])
            temps_actuel, fatigue_actuelle, noeud_actuel, chemin = a_visiter.pop(0)

            if noeud_actuel == arrivee: 
                # Si on est arrivés
                if extension_repos == '':
                    return chemin, temps_actuel, fatigue_actuelle
                else:
                    # On récupère les chemins découverts 
                    return chemin, temps_actuel, fatigue_actuelle, prunning

            if noeud_actuel == point_repos:
                # Extension du point de repos
                fatigue_actuelle = 1

            # Grace au dictionnaire de prunning, on ne continue que si on n'a pas de meilleur chemin
            if temps_actuel <= prunning.get((noeud_actuel, fatigue_actuelle), float('inf')):

                for point in self.neighbours(noeud_actuel):  # On explore les voisins
                    nom_voisin, longueur_arete, fatigue_arete = point

                    # On actualise le temps et la fatigue pour ce voisin
                    nouveau_temps = temps_actuel + (longueur_arete * fatigue_actuelle)
                    nouvelle_fatigue = fatigue_actuelle + fatigue_arete

                    # Prunning : on ne s'intéresse à un chemin que s'il est encore intéressant
                    if nouveau_temps < prunning.get((nom_voisin, nouvelle_fatigue), float('inf')):
                        prunning[(nom_voisin, nouvelle_fatigue)] = nouveau_temps
                        nouveau_chemin = chemin + [nom_voisin]
                        a_visiter.append((nouveau_temps, nouvelle_fatigue, nom_voisin, nouveau_chemin))

        if extension_repos == '':
            return "Pas de chemin", temps_init, fatigue_init
        else:
            return "Pas de chemin", temps_init, fatigue_init, prunning

    # -------------------------------------------------------------------------------------------
    # Partie 3 - Extensions
    # -------------------------------------------------------------------------------------------

    def missions_multiples(self, liste_missions):
        """
        Nous avons choisi de faire la première extension, qui gère 
        plusieurs missions à la suite pour un seul agent.
        
        Prend en entrée une liste de missions sous forme de tuples : 
        Exemple : [('A', 'B'), ('C', 'D')] (Aller de A à B, puis de C à D).
        Renvoie le chemin global complet et le temps total d'arrivée.
        """
        
        # L'agent commence tout au début avec un temps de 0 et une fatigue de 1
        temps_courant = 0
        fatigue_courante = 1
        chemin_global = []

        for i in range(len(liste_missions)):
            depart_mission, arrivee_mission = liste_missions[i]

            # On appelle A* qui va prendre en compte la fatigue déjà accumulée
            chemin_mission, temps_courant, fatigue_courante = self.A_etoile(
                depart_mission, arrivee_mission, temps_courant, fatigue_courante
            )
            
            if chemin_global == []:  
                # Si c'est le tout premier trajet, on ajoute tout le chemin.
                chemin_global.extend(chemin_mission)
            else:
                # Sinon, on omet le premier point car c'est le même que le
                # dernier point du trajet précédent (risque de doublons)
                chemin_global.extend(chemin_mission[1:])

            if i < len(liste_missions) - 1:
                # S'il reste des missions après celle-ci, l'agent doit se déplacer
                # de l'arrivée de la mission actuelle vers le départ de la mission suivante.
                prochain_depart = liste_missions[i+1][0]
                
                if arrivee_mission != prochain_depart:
                    # Si l'agent n'est pas déjà sur place, on cherche un chemin 
                    # allant de l'arrivée actuelle au prochain départ
                    chemin_transition, temps_courant, fatigue_courante = self.A_etoile(
                        arrivee_mission, prochain_depart, temps_courant, fatigue_courante
                    )
                    
                    # On ajoute ce trajet de transition au chemin global (toujours en évitant le doublon du 1er point)
                    chemin_global += chemin_transition[1:]

        return chemin_global, temps_courant

    def point_de_reposV1(self): # Première version qui est très lente
        """ Dans cette extension, on suppose qu'un point réinitialise la fatigue.
        L'objectif est de calculer l'endroit optimal pour placer le point de repos.

        Nous avons choisit de considérer optimal le point qui réduit le plus le 
        temps de chaque chemin. Ainsi, pour chaque chemin on détermine quel serait le
        meilleur point de repos, et à la fin, on élit celui qui a le plus de votes."""

        points_optimaux = {}

        # On va tester tous les chemins possibles du graph
        liste_sommets = self._roads.keys()
        for depart in liste_sommets:
            for arrivee in liste_sommets:
                
                # On enlève tous les cas qui ne sont pas intéressants 
                if arrivee == depart or arrivee in self.neighbours(depart):
                    continue

                dico_repos = {}
                for point_repos in liste_sommets:
                    # Pour chaque point de repos possible on regarde le temps minimal 
                    # pour aller du départ à l'arrivée
                    _ , temps, _, _ = self.A_etoile(depart, arrivee, 0, 1, (point_repos, {}))
                    dico_repos[point_repos] = temps

            # On regarde quel a été le point de repos pour lequel le chemin à été le plus rapide
            # S'il y en a plusieurs, alors tantpis, un seul sera choisit (à améliorer)
            point_repos_optimal = min(dico_repos, key=dico_repos.get)

            if point_repos_optimal in points_optimaux.keys():
                # On ajoute un vote au meilleur point pour ce chemin ...
                points_optimaux[point_repos_optimal] += 1
            else:
                # ... ou on l'ajoute au dictionnaire si il n'a pas encore de vote
                points_optimaux[point_repos_optimal] = 1

        # Le point qui a le plus de vote est 'élu' point de repos optimal pour ce graph
        point_optimal_graph = max(points_optimaux, key=points_optimaux.get)
        return point_optimal_graph

    def point_de_repos(self):
        """ Dans cette extension, on suppose qu'un point réinitialise la fatigue.
        L'objectif est de calculer l'endroit optimal pour placer le point de repos.

        Cette fois ci, nous ne regardons pas quel point optimise le plus de chemin,
        mais quel point optimise le plus le graph. Pour chaque point de repos, on
        on évalue le temps cumulé de tous les chemins optimisés possibles grâce à A*,
        et on en fait la somme. Le point qui aura le plus petit score sera considéré
        comme étant le meilleur."""

        temps_points_repos = []
        liste_points = self._roads.keys()
        for point_repos in liste_points:
            temps_cumule = 0
            # On créé un dictionnaire de prunning global pour tout le graph, 
            # qui prend en compte le point de repos. Ce dictionnaire rend cette
            # extension point de repos bien plus rapide que la première version
            prunning = {}

            for depart in liste_points:
                for arrivee in liste_points:

                    if depart == arrivee or arrivee in self.neighbours(depart):
                        # Si le chemin n'est pas intéressant, on le passe
                        continue

                    _, temps, _, dico_A = self.A_etoile(depart, arrivee, 0, 1, (point_repos, prunning))
                    temps_cumule += temps
                    prunning.update(dico_A)
            
            # On range tous les scores des points candidats et leurs noms dans une liste
            temps_points_repos.append((temps_cumule, point_repos))
        
        # On prend le meilleur point, celui qui a le plus petit temps cumulé
        _, point_repos_optimal = min(temps_points_repos)
        return point_repos_optimal
