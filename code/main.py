# -------------------------------------------------------
# CONNEXION A NETWORK

import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network

# --------------------------------------------------------

# Load the network
network_file = NET_DIR / "small.txt"
network = Network.from_file(network_file)


test1 = network.build_extended_graph()
test2 = network.build_simple_graph()
# print(network.longueur_chemin(['lozère']))
# print(test1.shortest_path('lozere', 'saclay'))


network_file = NET_DIR / "large-largefatigue.txt"
network = Network.from_file(network_file)

test = Network.from_file("examples/large-largefatigue.txt")
# print(test.A_etoile('v0', 'v12'))

missions = [('v0', 'v12'), ('v14', 'v19'), ('v39', 'v45')]
print(test.missions_multiples(missions))
