from pytest import fixture
from pytest import approx

from stmeasures.calculate.hausdorff import Hausdorff

@fixture(scope="module")
def hausdorff():
    return Hausdorff()

def test_lib(hausdorff):
    assert hausdorff.lib is not None

def test_basic(hausdorff):
    assert hausdorff.distance([(1, 2)], [(3, 4)]) == approx(2.0)
