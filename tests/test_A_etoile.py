import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402
from graph import Graph  # noqa: E402


def test_A_etoile():
    """ Teste la methode A_etoile de la classe Network """
    # Setup
    graph = Network.from_file(NET_DIR / "small.txt")

    # Assertions
    assert isinstance(graph, Graph)
    chemin = ['lozere', 'guichet', 'ensae', 'saclay']
    assert graph.A_etoile('lozere', 'saclay') == chemin
