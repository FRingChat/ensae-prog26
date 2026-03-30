import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402
from graph import Graph  # noqa: E402


def test_build_simple_graph():
    """ Teste la methode build_simple_graph de la classe Network """
    # Setup
    simple_graph = Network.from_file(NET_DIR / "small.txt")
    simple_graph = simple_graph.build_simple_graph()

    # Assertions
    assert isinstance(simple_graph, Graph)
    assert simple_graph.neighbours("lozere") == [('ensae', 10), ('guichet', 20)]
    assert simple_graph._edges() == {
        'lozere': [('ensae', 10), ('guichet', 20)],
        'ensae': [('saclay', 45)],
        'guichet': [('ensae', 15)],
        'saclay': []
    }
