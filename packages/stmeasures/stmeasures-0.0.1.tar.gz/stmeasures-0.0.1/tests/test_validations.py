import pytest

from stmeasures.validation import (
    validate_trajectory,
    validate_numeric_list,
    validate_scalar,
    validate_positive_scalar,
    validate_distance_parameters,
    validate_dtw,
    validate_ers,
    validate_erp,
    validate_euclidean,
    validate_frechet,
    validate_hausdorff,
    validate_lcss,
    validate_rdp,
)

def test_validate_trajectory():
    valid_trajectory = [(34.05, -118.25), (40.71, -74.01)]
    validate_trajectory(valid_trajectory)

    with pytest.raises(ValueError, match="Expected a non-empty list of coordinate tuples"):
        validate_trajectory([])

    with pytest.raises(ValueError, match="Each coordinate must be a tuple with 2 elements"):
        validate_trajectory([(34.05, -118.25), (40.71,)])

    with pytest.raises(ValueError, match="Latitude and longitude must be numeric"):
        validate_trajectory([(34.05, "not_a_lon")])

    with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
        validate_trajectory([(100, -118.25)])

def test_validate_numeric_list():
    validate_numeric_list([1.0, 2.0, 3.5])

    with pytest.raises(ValueError, match="Expected a non-empty list of numbers"):
        validate_numeric_list([])

    with pytest.raises(ValueError, match="All elements must be numeric"):
        validate_numeric_list([1.0, "not_a_number"])

def test_validate_scalar():
    validate_scalar(5)
    validate_scalar(3.14)

    with pytest.raises(ValueError, match="must be a numeric type"):
        validate_scalar("not_a_number")

def test_validate_positive_scalar():
    validate_positive_scalar(5)
    validate_positive_scalar(3.14)

    with pytest.raises(ValueError, match="must be a non-negative number"):
        validate_positive_scalar(-5)

def test_validate_distance_parameters():
    validate_distance_parameters([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])

    with pytest.raises(ValueError, match="The two sequences must have the same length"):
        validate_distance_parameters([1.0, 2.0], [4.0, 5.0, 6.0])

def test_validate_dtw():
    validate_dtw([(34.05, -118.25)], [(40.71, -74.01)])

def test_validate_ers():
    validate_ers(
        [1.0, 2.0],
        [3.0, 4.0],
        sigma=1.0,
        cost_deletion=1.0,
        cost_insertion=1.0,
        subcost_within_sigma=0.5,
        subcost_outside_sigma=1.5,
    )

def test_validate_erp():
    validate_erp([1.0, 2.0], [3.0, 4.0], g=0.0)

def test_validate_euclidean():
    validate_euclidean([1.0, 2.0], [3.0, 4.0])

def test_validate_frechet():
    validate_frechet([1.0, 2.0], [3.0, 4.0])

def test_validate_hausdorff():
    validate_hausdorff([1.0, 2.0], [3.0, 4.0])

def test_validate_lcss():
    validate_lcss([1.0, 2.0], [3.0, 4.0], sigma=0.5)

def test_validate_rdp():
    validate_rdp([(34.05, -118.25), (40.71, -74.01)], tolerance=0.1)
