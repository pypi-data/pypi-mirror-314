import pytest
from stmeasures.calculate.dtw import DTW

@pytest.fixture(scope="module")
def dtw():
    return DTW()

def test_lib(dtw):
    assert dtw.lib is not None

def test_basic(dtw):

    seq1 = [(1.0, 1.0), (13.0, 3.0)]
    seq2 = [(1560.0, 1.0), (3.0, 3.0)]
    approx_val = 3128
    
    assert dtw.distance(seq1, seq2) == pytest.approx(approx_val)
    
