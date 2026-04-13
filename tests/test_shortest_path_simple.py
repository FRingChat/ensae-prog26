import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402


def test_shortest_path_simple():
    """ Teste la méthode shortest_path de la classe Graph pour un graph simple sans fatigue """
    # Setup
    simple_graph = Network.from_file(NET_DIR / "small.txt")
    simple_graph = simple_graph.build_simple_graph()
    test = Network.from_file(NET_DIR / "medium-smallfatigue.txt")

    # Assertions
    assert simple_graph.shortest_path('lozere', 'saclay') == ['lozere', 'ensae', 'saclay']
    assert simple_graph.shortest_path('guichet', 'saclay') == ['guichet', 'ensae', 'saclay']
    assert test.shortest_path('v0', 'v3') == ['v0', 'v3']
