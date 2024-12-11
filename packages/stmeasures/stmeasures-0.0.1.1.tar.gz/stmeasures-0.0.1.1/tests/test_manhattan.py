from pytest import fixture
from pytest import approx

from stmeasures.calculate.manhattan import Manhattan

@fixture(scope="module")
def manhattan():
    return Manhattan()

def test_lib(manhattan):
    assert manhattan.lib is not None

def test_basic(manhattan):
    assert manhattan.distance([1, 2], [3, 4]) == approx(4.0)
