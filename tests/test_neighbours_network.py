import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402


def test_neighbours_network():
    """ Teste la méthode neighbours de la classe network """
    # Setup
    network = Network.from_file(NET_DIR / "small.txt")
    network_bis = Network.from_file(NET_DIR / "medium-largefatigue.txt")

    # Assertions
    assert network.neighbours("ensae") == [('saclay', 45, 0)]
    assert network.neighbours("saclay") == []
    assert network_bis.neighbours('v9') == [('v7', 689, 986), 
        ('v9', 309, 89), ('v10', 14, 195), ('v11', 16, 712), 
        ('v14', 664, 148), ('v16', 641, 878), ('v18', 308, 788), 
        ('v19', 485, 432)]
