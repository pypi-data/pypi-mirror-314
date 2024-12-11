from pytest import fixture
from pytest import approx

from stmeasures.calculate.lcss import LCSS

@fixture(scope="module")
def lcss():
    return LCSS()

def test_lib(lcss):
    assert lcss.lib is not None

def test_lcss(lcss):
    r = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    s = [(11, 12), (13, 14), (15, 16), (17, 18), (19, 20)]

    assert lcss.distance(r, s) == approx(0.1)
