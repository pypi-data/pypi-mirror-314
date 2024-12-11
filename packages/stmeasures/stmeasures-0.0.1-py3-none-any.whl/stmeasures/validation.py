"""Validation module.

This module provides validation functions for trajectory data, numeric lists,
scalars, and various distance calculation parameters.
"""

def validate_trajectory(trajectory: list[tuple[float, float]]):
    """
    Validate that the input is a non-empty list of coordinate tuples with valid
    latitude and longitude values.

    :param trajectory:
        A list of tuples representing coordinates (latitude, longitude).
    :type trajectory: list[tuple[float, float]]
    
    :raises ValueError:
        - if `trajectory` is not a non-empty list of coordinate tuples
        - if any tuple does not contain exactly two elements
        - if latitude or longitude are not numeric types
        - if latitude is not between -90 and 90, or longitude is not between
          -180 and 180
    """
    if not isinstance(trajectory, list) or not trajectory:
        raise ValueError("Expected a non-empty list of coordinate tuples.")
    for point in trajectory:
        if not isinstance(point, tuple) or len(point) != 2:
            raise ValueError(
                "Each coordinate must be a tuple with 2 elements (latitude," \
                " longitude)."
            )
        lat, lon = point
        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            raise ValueError("Latitude and longitude must be numeric.")
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError(
                "Latitude must be between -90 and 90, and longitude between" \
                "-180 and 180."
            )

def validate_numeric_list(sequence: list[float]):
    """
    Validate that the input is a non-empty list of numeric values.

    :param sequence: A list of numeric values.
    :type sequence: list[float]
    
    :raises ValueError: 
        - If `sequence` is not a non-empty list.
        - If any element in `sequence` is not a numeric type.
    """
    if not isinstance(sequence, list) or not sequence:
        raise ValueError("Expected a non-empty list of numbers.")
    for value in sequence:
        if not isinstance(value, (int, float)):
            raise ValueError("All elements must be numeric.")

def validate_scalar(value, name="value"):
    """
    Validate that the input value is a scalar (integer or float).

    :param value: The value to validate.
    :type value: int or float
    :param name:
        Name of the variable, used for error messages, defaults to "value".
    :type name: str, optional
    
    :raises ValueError: If `value` is not a numeric type.
    """
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a numeric type.")

def validate_positive_scalar(value: int | float, name="value"):
    """
    Validate that the input value is a positive scalar (integer or float).

    :param value: The value to validate.
    :type value: int or float
    :param name:
        Name of the variable, used for error messages, defaults to "value".
    :type name: str, optional
    
    :raises ValueError: If `value` is not a non-negative numeric type.
    """
    validate_scalar(value, name)
    if value < 0:
        raise ValueError(f"{name} must be a non-negative number.")

def validate_distance_parameters(
        p: list[float],
        q: list[float]
    ):
    """
    Validate that two numeric lists are provided and that they have the same
    length.

    :param p: First numeric list.
    :type p: list[float]
    :param q: Second numeric list.
    :type q: list[float]
    
    :raises ValueError: 
        - If either `p` or `q` is not a numeric list.
        - If `p` and `q` do not have the same length.
    """
    validate_numeric_list(p)
    validate_numeric_list(q)
    if len(p) != len(q):
        raise ValueError("The two sequences must have the same length.")

def validate_dtw(
        seq1: list[tuple[float, float]],
        seq2: list[tuple[float, float]]
    ):
    """
    Validate parameters for the Dynamic Time Warping (DTW) algorithm.

    :param seq1: First trajectory list.
    :type seq1: list[tuple[float, float]]
    :param seq2: Second trajectory list.
    :type seq2: list[tuple[float, float]]
    """
    validate_trajectory(seq1)
    validate_trajectory(seq2)

def validate_ers(
        r: list[float],
        s: list[float],
        sigma: float = 1.0,
        cost_deletion: float = 1.0,
        cost_insertion: float = 1.0,
        subcost_within_sigma: float = 0.0,
        subcost_outside_sigma: float = 1.0
    ):
    """
    Validate parameters for the Edit Distance on Real Sequences (ERS)
    algorithm.

    :param r: First numeric list.
    :type r: list[float]
    :param s: Second numeric list.
    :type s: list[float]
    :param sigma: Threshold for matching.
    :type sigma: float
    :param cost_deletion: Cost for deletion operations.
    :type cost_deletion: float
    :param cost_insertion: Cost for insertion operations.
    :type cost_insertion: float
    :param subcost_within_sigma: Substitution cost within sigma range.
    :type subcost_within_sigma: float
    :param subcost_outside_sigma: Substitution cost outside sigma range.
    :type subcost_outside_sigma: float
    
    :raises ValueError:
        - if any list parameter is not a numeric list
        - if any cost parameter is not a positive scalar
    """
    validate_numeric_list(r)
    validate_numeric_list(s)
    validate_positive_scalar(sigma, "sigma")
    validate_scalar(cost_deletion, "cost_deletion")
    validate_scalar(cost_insertion, "cost_insertion")
    validate_scalar(subcost_within_sigma, "subcost_within_sigma")
    validate_scalar(subcost_outside_sigma, "subcost_outside_sigma")

def validate_erp(
        r: list[float],
        s: list[float],
        g: float
    ):
    """
    Validate parameters for the Edit Distance with Real Penalty (ERP)
    algorithm.

    :param r: First numeric list.
    :type r: list[float]
    :param s: Second numeric list.
    :type s: list[float]
    :param g: Gap constant.
    :type g: int or float
    
    :raises ValueError:
        - if `r` or `s` is not a numeric list
        - if `g` is not a scalar
    """
    validate_numeric_list(r)
    validate_numeric_list(s)
    validate_scalar(g, "gap constant (g)")

def validate_euclidean(
        p: list[float],
        q: list[float]
    ):
    """
    Validate parameters for Euclidean distance calculation between two numeric
    lists.

    :param p: First numeric list.
    :type p: list[float]
    :param q: Second numeric list.
    :type q: list[float]
    
    :raises ValueError:
        - if `p` or `q` is not a numeric list
        - if `p` and `q` do not have the same length
    """
    validate_distance_parameters(p, q)

def validate_frechet(p: list[float], q: list[float]):
    """
    Validate parameters for Fréchet distance calculation between two numeric
    lists.

    :param p: First numeric list.
    :type p: list[float]
    :param q: Second numeric list.
    :type q: list[float]
    
    :raises ValueError:
        - if `p` or `q` is not a numeric list
    """
    validate_numeric_list(p)
    validate_numeric_list(q)

def validate_hausdorff(p: list[float], q: list[float]):
    """
    Validate parameters for Hausdorff distance calculation between two numeric
    lists.

    :param p: First numeric list.
    :type p: list[float]
    :param q: Second numeric list.
    :type q: list[float]
    
    :raises ValueError:
        - if `p` or `q` is not a numeric list
    """
    validate_numeric_list(p)
    validate_numeric_list(q)

def validate_lcss(
        r: list[float],
        s: list[float],
        sigma: float
    ):
    """
    Validate parameters for Longest Common Subsequence Similarity (LCSS)
    calculation.

    :param r: First numeric list.
    :type r: list[float]
    :param s: Second numeric list.
    :type s: list[float]
    :param sigma: Matching threshold.
    :type sigma: float
    
    :raises ValueError:
        - if `r` or `s` is not a numeric list
        - if `sigma` is not a positive scalar
    """
    validate_numeric_list(r)
    validate_numeric_list(s)
    validate_positive_scalar(sigma, "sigma")

def validate_rdp(sequence: list[tuple[float, float]], tolerance: float):
    """
    Validate parameters for the Ramer-Douglas-Peucker (RDP) simplification
    algorithm.

    :param sequence: List of coordinate tuples (latitude, longitude).
    :type sequence: list[tuple[float, float]]
    :param tolerance: Tolerance value for simplification.
    :type tolerance: float
    
    :raises ValueError:
        - if `sequence` is not a valid trajectory list
        - if `tolerance` is not a positive scalar
    """
    validate_trajectory(sequence)
    validate_positive_scalar(tolerance, "tolerance")
