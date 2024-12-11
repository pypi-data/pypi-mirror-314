import pytest
from stmeasures.calculate.rdp import RDP

@pytest.fixture(scope="module")
def rdp():
    """Fixture to create an instance of the RDP class."""
    return RDP()

def test_lib(rdp):
    """Test that the RDP library is properly loaded."""
    assert rdp.lib is not None

def test_basic_simplification(rdp):
    """Test the basic RDP simplification algorithm with a fixed input sequence."""

    sequence = [
        (0.0, 0.0),
        (1.0, 0.1),
        (2.0, -0.1),
        (3.0, 5.0),
        (4.0, 6.0),
        (5.0, 7.0),
        (6.0, 8.0),
        (7.0, 7.0)
    ]

    tolerance = 5.0

    expected_result = [
        (0.0, 0.0),
        (7.0, 7.0)
    ]

    simplified_sequence = rdp.simplify(sequence, tolerance)

    assert simplified_sequence == pytest.approx(expected_result)


