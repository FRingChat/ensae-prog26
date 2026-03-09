import sys
from pathlib import Path
import pytest
from network import Network

"""
Problème dans ce script !
Python ne trouve pas le module 'network'

Message d'erreur :
Traceback (most recent call last):
    File "/home/onyxia/work/ensae-prog26/tests/test_network_from_file_pytest.py", line 4, in <module>
    from network import Network
ModuleNotFoundError: No module named 'network'
"""

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"


def test_network_small():
    # Setup
    network = Network.from_file(NET_DIR / "small.txt")

    # Assertions
    assert network.start == "lozere"
    assert network.end == "saclay"
    assert network._roads == {
        'lozere': [('ensae', 10, 2), ('guichet', 20, 0)],
        'ensae': [('saclay', 45, 0)],
        'guichet': [('ensae', 15, 1)],
        'saclay': []
    }


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


def test_shortest_path_simple():
    """ Teste la méthode shortest_path de la classe Graph pour un graph simple sans fatigue """
    # Setup
    simple_graph = Network.from_file(NET_DIR / "small.txt")
    simple_graph = simple_graph.build_simple_graph()

    # Assertions
    assert simple_graph.shortest_path('lozere', 'saclay') == ['lozere', 'ensae', 'saclay']
    assert simple_graph.shortest_path('guichet', 'saclay') == ['guichet', 'ensae', 'saclay']


def test_shortest_path_extended():
    """ Teste la méthode shortest_path de la classe Graph pour un graph étendu avec fatigue """
    # Setup
    extended_graph = Network.from_file("examples/small.txt")
    extended_graph = extended_graph.build_extended_graph()

    # Assertions
    assert isinstance(extended_graph, Graph)
    assert extended_graph.shortest_path('lozere', 'saclay') == ['lozere', 'guichet', 'ensae', 'saclay']


def test_neighbours_network():
    """ Teste la méthode neighbours de la classe network """
    # Setup
    network = Network.from_file(NET_DIR / "small.txt")

    # Assertions
    assert network.neighbours("ensae") == [('saclay', 45, 0)]
    assert network.neighbours("saclay") == []z