import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402
from graph import Graph  # noqa: E402


def test_missions_multiples():
    """ Teste la methode A_etoile de la classe Network """
    # Setup
    missions = [('v0', 'v34'), ('v40', 'v45'), ('v39', 'v45')] 
    test = Network.from_file(NET_DIR / "large-nofatigue.txt")

    # Assertions
    result = (['v0', 'v40', 'v123', 'v106', 'v115', 'v34', 'v113',
              'v66', 'v2', 'v0', 'v40', 'v123', 'v26', 'v29', 'v45',
              'v139', 'v221', 'v132', 'v39', 'v107', 'v52', 'v28',
              'v111', 'v87', 'v155', 'v233', 'v202', 'v123', 'v26',
              'v29', 'v45'], 3673)
    assert test.missions_multiples(missions) == result

print(test_missions_multiples())