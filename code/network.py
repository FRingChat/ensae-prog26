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

    # -------------------------------------------------------------------------------------------
    # Partie 2
    # -------------------------------------------------------------------------------------------

    def A_etoile(self, depart, arrivee):
        """
        Renvoie le chemin de temps minimal du départ à l'arrivée en tenant
        compte de la fatigue

        Nous avons implémenté dans ce script une methode de Pruning grâce au
        dictionnaire temps_min, qui catalogue uniquements les chemins qui sont
        intéressants.
        """

        a_visiter = [(0, 1, depart, [depart])]

        # On créé un dictionnaire pour connaitre tout les chemins les plus courts
        temps_min = {(depart, 1): 0}

        while len(a_visiter) > 0:  # Expolration des points à visiter

            # On regarde le chemin le plus court en premier
            a_visiter.sort(key=lambda x: x[0])
            temps_actuel, fatigue_actuelle, noeud_actuel, chemin = a_visiter.pop(0)

            if noeud_actuel == arrivee:
                # On arrête la boucle quand on atteind l'arrivée
                return chemin

            # Pruning : On ne continue que si on pas de meilleur chemin (grâce au dictionnaire)
            if temps_actuel <= temps_min.get((noeud_actuel, fatigue_actuelle), float('inf')):

                for point in self.neighbours(noeud_actuel):  # On explore les voisins
                    nom_voisin, longueur_arete, fatigue_arete = point

                    # On actualise la fatigue
                    nouveau_temps = temps_actuel + (longueur_arete * fatigue_actuelle)
                    nouvelle_fatigue = fatigue_actuelle + fatigue_arete

                    # Pruning : si on a mieux pour aller au même point, on passe (grâce au dictionnaire)
                    if nouveau_temps < temps_min.get((nom_voisin, nouvelle_fatigue), float('inf')):
                        # Si on trouve le meilleur chemin, on actualise le dictionaire et notre chemin
                        temps_min[(nom_voisin, nouvelle_fatigue)] = nouveau_temps
                        nouveau_chemin = chemin + [nom_voisin]
                        a_visiter.append((nouveau_temps, nouvelle_fatigue, nom_voisin, nouveau_chemin))

        return "Pas de chemin"

-------------------------------------------------- DEBUT DE LA PARTIE 3 ------------------------------------------------------------

"""
Alors du coup, j'ai choisi la première car c'est la plus simple. Le premier trouc à faire (le code suivant) c'est de remplacer la fonction A* de la 
partie 2 par la fonction suivante comme ca elle prend une entrée temps_init et fatigue_init et elle renvoie ces valeurs à la fin pour q'elle puisse 
les réutiliser à la missions suivante."""
 


def A_etoile(self, depart, arrivee, temps_init=0, fatigue_init=1):
        """
        Renvoie le chemin de temps minimal, ainsi que le temps final et la fatigue finale.
        
        Modification pour la Partie 3 : on ajoute des paramètres par défaut (temps_init et fatigue_init)
        pour permettre à un agent de commencer un trajet en étant déjà fatigué par une mission précédente.
        """

        # On initialise la liste à visiter avec le temps et la fatigue passés en paramètres
        a_visiter = [(temps_init, fatigue_init, depart, [depart])]

        # Le dictionnaire de pruning commence lui aussi avec le temps initial
        temps_min = {(depart, fatigue_init): temps_init}

        while len(a_visiter) > 0:  # Exploration des points à visiter

            # On regarde le chemin le plus court en premier
            a_visiter.sort(key=lambda x: x[0])
            temps_actuel, fatigue_actuelle, noeud_actuel, chemin = a_visiter.pop(0)

            if noeud_actuel == arrivee:
                # MODIFICATION IMPORTANTE : on renvoie aussi le temps et la fatigue 
                # pour pouvoir les conserver d'une mission à l'autre.
                return chemin, temps_actuel, fatigue_actuelle

            # Pruning : On ne continue que si on n'a pas de meilleur chemin
            if temps_actuel <= temps_min.get((noeud_actuel, fatigue_actuelle), float('inf')):

                for point in self.neighbours(noeud_actuel):  # On explore les voisins
                    nom_voisin, longueur_arete, fatigue_arete = point

                    # On actualise le temps et la fatigue pour ce voisin
                    nouveau_temps = temps_actuel + (longueur_arete * fatigue_actuelle)
                    nouvelle_fatigue = fatigue_actuelle + fatigue_arete

                    # Pruning : si on a mieux pour aller au même point, on passe
                    if nouveau_temps < temps_min.get((nom_voisin, nouvelle_fatigue), float('inf')):
                        temps_min[(nom_voisin, nouvelle_fatigue)] = nouveau_temps
                        nouveau_chemin = chemin + [nom_voisin]
                        a_visiter.append((nouveau_temps, nouvelle_fatigue, nom_voisin, nouveau_chemin))

        return "Pas de chemin", temps_init, fatigue_init


""" Ensuite, toujours dans network a la suite de la nouvelle A*, on crée la methode suivante (le code en dessous), c'est ca qui gère l'enchaînement des missions et normalement c'est expliqué dans le code"""

def missions_multiples(self, liste_missions):
        """
        Extension 1 : Gère plusieurs missions à la suite pour un seul agent.
        
        Prend en entrée une liste de missions sous forme de tuples : 
        Exemple : [('A', 'B'), ('C', 'D')] (Aller de A à B, puis de C à D).
        Renvoie le chemin global complet et le temps total d'arrivée.
        """
        
        # L'agent commence tout au début avec un temps de 0 et une fatigue de 1
        temps_courant = 0
        fatigue_courante = 1
        chemin_global = []

        # On boucle sur chaque mission (en utilisant l'index pour savoir si c'est la dernière)
        for i in range(len(liste_missions)):
            depart_mission, arrivee_mission = liste_missions[i]

            # --- ETAPE 1 : RÉALISER LA MISSION ---
            # On appelle notre A* modifié qui va prendre en compte la fatigue déjà accumulée
            chemin_mission, temps_courant, fatigue_courante = self.A_etoile(
                depart_mission, arrivee_mission, temps_courant, fatigue_courante
            )

            # Pour l'affichage du chemin global, on évite les doublons.
            # Si c'est le tout premier trajet, on ajoute tout le chemin.
            if not chemin_global:
                chemin_global.extend(chemin_mission)
            else:
                # Sinon, on omet le premier point (car c'est le même que le dernier point du trajet précédent)
                chemin_global.extend(chemin_mission[1:])

            # --- ETAPE 2 : TRANSITION VERS LA MISSION SUIVANTE ---
            # S'il reste des missions après celle-ci, l'agent doit se déplacer
            # de l'arrivée de la mission actuelle vers le départ de la mission suivante.
            if i < len(liste_missions) - 1:
                prochain_depart = liste_missions[i+1][0]
                
                # On vérifie si l'agent n'est pas déjà sur place
                if arrivee_mission != prochain_depart:
                    # Nouveau trajet : de l'arrivée actuelle au prochain départ
                    chemin_transition, temps_courant, fatigue_courante = self.A_etoile(
                        arrivee_mission, prochain_depart, temps_courant, fatigue_courante
                    )
                    
                    # On ajoute ce trajet de transition au chemin global (toujours en évitant le doublon du 1er point)
                    chemin_global.extend(chemin_transition[1:])

        # Une fois toutes les missions et transitions effectuées, on renvoie le résultat final
        return chemin_global, temps_courant


""" Enfin, ca m'a produit un test automatiquement à mettre dans le main je le cope colle juste en dessous"""

print("\n--- TEST EXTENSION 1 : MISSIONS MULTIPLES ---")
# On invente une suite de missions (assure-toi que ces noeuds existent dans ton fichier texte)
mes_missions = [('v0', 'v3'), ('v4', 'v12')] 

chemin_final, temps_final = test.missions_multiples(mes_missions)
print(f"Le chemin complet de l'agent est : {chemin_final}")
print(f"Le temps total pour accomplir toutes les missions est de : {temps_final}")
