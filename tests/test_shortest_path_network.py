import sys
from pathlib import Path
# import pytest


ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402
from graph import Graph  # noqa: E402


def test_shortest_path_network():
    """ Teste la méthode shortest_path de la classe Network
    pour un graph étendu avec fatigue """
    # Setup
    extended_graph = Network.from_file("examples/small.txt")
    extended_graph = extended_graph.build_extended_graph()

    # Assertions
    assert isinstance(extended_graph, Graph)
    chemin = ['lozere', 'guichet', 'ensae', 'saclay']
    assert extended_graph.shortest_path_network('lozere', 'saclay') == chemin
