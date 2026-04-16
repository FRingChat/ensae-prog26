# -------------------------------------------------------
# CONNEXION A NETWORK

import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402

# --------------------------------------------------------

# Load the network
network_file = NET_DIR / "medium-smallfatigue.txt"
network = Network.from_file(network_file)

# print(network.point_de_repos())

test1 = network.build_extended_graph()
test2 = network.build_simple_graph()
# print(network.longueur_chemin(['v10', 'v3', 'v12']))
# print(test1.shortest_path('v0', 'v5'))


# network_file = NET_DIR / "large-largefatigue.txt"
# network = Network.from_file(network_file)

test = Network.from_file("examples/medium-smallfatigue.txt")
# # print(test.A_etoile('v0', 'v12'))

missions = [('v0', 'v34'), ('v34', 'v99')]
# print(test.missions_multiples(missions))
