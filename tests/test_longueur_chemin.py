import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402


def test_neighbours_network():
    """ Teste la méthode longueur_chemin de la classe network """
    # Setup
    network = Network.from_file(NET_DIR / "small.txt")

    # Assertions
    assert network.longueur_chemin(['lozere', 'guichet', 'ensae', 'saclay']) == 125
    assert network.neighbours([]) == 0
    assert network.neighbours(['ensae']) == 0
