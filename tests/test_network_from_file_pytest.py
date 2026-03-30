import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # cette ligne print 0 jsp pq  # noqa: E402

"""
Le module Pytest n'est pas installé, mais il n'est pas utile dans
les tests, je l'ai donc mis en commentaire
"""


def test_network_small():
    # Setup
    natwork = Network.from_file(NET_DIR / "small.txt")

    # Assertions
    assert natwork.start == "lozere"
    assert natwork.end == "saclay"
    assert natwork._roads == {
        'lozere': [('ensae', 10, 2), ('guichet', 20, 0)],
        'ensae': [('saclay', 45, 0)],
        'guichet': [('ensae', 15, 1)],
        'saclay': []
    }
