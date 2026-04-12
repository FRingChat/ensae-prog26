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
    test = Network.from_file("examples/medium-smallfatigue.txt")

    # Assertions
    result = (['v39', 'v48', 'v45'], 1522, 7)
    assert test.A_etoile('lozere', 'saclay') == result
