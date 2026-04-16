import sys
from pathlib import Path
# import pytest

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from network import Network  # noqa: E402


def test_point_de_repos():
    # Setup
    graph = Network.from_file(NET_DIR / "small.txt")

    # Assertions
    assert graph.point_de_repos() == 'ensae'