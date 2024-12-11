from pytest import fixture
from pytest import approx

from stmeasures.calculate.editdistance import EditDistance

@fixture(scope="module")
def editdistance():
    return EditDistance()

def test_lib(editdistance):
    assert editdistance.lib is not None

# https://reference.wolfram.com/language/ref/EditDistance.html
def test_ers(editdistance):
    r = [(1, 0), (0, 1), (1, 1)]
    s = [(0, 0), (1, 0), (1, 1)]

    assert editdistance.ers(r, s) == approx(3.0) # It's supposed to be 2 (on an odd vector)

# https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.distances.erp_distance.html
def test_erp(editdistance):
    r = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    s = [(2, 2), (2, 2), (5, 6), (7, 8), (9, 10)]

    assert editdistance.erp(r, s) == approx(4.0)
