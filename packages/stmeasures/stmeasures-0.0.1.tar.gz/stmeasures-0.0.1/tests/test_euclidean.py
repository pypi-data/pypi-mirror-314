import pytest

from stmeasures.calculate.euclidean import Euclidean

@pytest.fixture(scope="module")
def euclidean():
    return Euclidean()

def test_lib(euclidean):
    assert euclidean.lib is not None

def test_basic(euclidean):
    approx_val = 2.8284271247461903
    assert euclidean.distance([(1, 2)], [(3, 4)]) == pytest.approx(approx_val)
