"""Calculate module for various distance algorithms."""

import stmeasures.calculate.rdp as _scrd
import stmeasures.calculate.dtw as _scdt
import stmeasures.calculate.lcss as _sclc
import stmeasures.calculate.frechet as _scfr
import stmeasures.calculate.hausdorff as _scha
import stmeasures.calculate.editdistance as _sced
import stmeasures.calculate.euclidean as _sceu
import stmeasures.calculate.sad as _scsa
from stmeasures._algorithms import Algorithms

_rdp = _scrd.RDP()
_dtw = _scdt.DTW()
_lcss = _sclc.LCSS()
_frechet = _scfr.Frechet()
_hausdorff = _scha.Hausdorff()
_editdistance = _sced.EditDistance()
_euclidean = _sceu.Euclidean()
_spad = _scsa.SAD()

def simplify(trajectory, tolerance):
    """
    Simplify a trajectory using the Ramer-Douglas-Peucker algorithm.

    Parameters
    ----------
    trajectory : list[tuple[float, float]]
        The trajectory points to simplify.
    tolerance : float
        The tolerance value that determines the degree of simplification.

    Returns
    -------
    list[tuple[float, float]]
        A simplified version of the input trajectory.
    """
    return _rdp.simplify(trajectory, tolerance)

def distance(a, b, algorithm=Algorithms.SPAD, *args):
    """
    Compute the distance between two trajectories using a specified algorithm.

    This function supports multiple distance metrics for comparing trajectories. 
    The algorithm used can be specified via the `algorithm` parameter. 
    Additional arguments required by specific algorithms can be passed via `*args`.

    Parameters
    ----------
    a : list[tuple[float, float]]
        The first trajectory, represented as a list of (x, y) coordinate tuples.
    b : list[tuple[float, float]]
        The second trajectory, represented as a list of (x, y) coordinate tuples.
    algorithm : Algorithms, optional
        The algorithm to use for computing the distance. Defaults to `Algorithms.SPAD`.
        Supported algorithms:
        - `Algorithms.EUCLIDEAN`: Euclidean distance.
        - `Algorithms.DTW`: Dynamic Time Warping.
        - `Algorithms.LCSS`: Longest Common Subsequence.
        - `Algorithms.FRECHET`: Frechet distance.
        - `Algorithms.HAUSDORFF`: Hausdorff distance.
        - `Algorithms.ERS`: Edit Distance on Real Sequences (ERS).
        - `Algorithms.ERP`: Edit Distance with Real Penalty (ERP).
        - `Algorithms.SPAD`: Spatial Aspects Distance (SPAD).
    `*args` : optional
        Additional arguments specific to the selected algorithm.

    Returns
    -------
    float
        The computed distance between the two trajectories.

    Raises
    ------
    ValueError
        If the specified `algorithm` is not supported.

    Examples
    --------
    Compute the Euclidean distance between two trajectories:

    >>> a = [(0, 0), (1, 1), (2, 2)]
    >>> b = [(0, 0), (2, 2), (3, 3)]
    >>> distance(a, b, algorithm=Algorithms.EUCLIDEAN)
    2.0
    """
    if algorithm == Algorithms.EUCLIDEAN:
        return _euclidean.distance(a, b, *args)
    elif algorithm == Algorithms.DTW:
        return _dtw.distance(a, b, *args)
    elif algorithm == Algorithms.LCSS:
        return _lcss.distance(a, b, *args)
    elif algorithm == Algorithms.FRECHET:
        return _frechet.distance(a, b)
    elif algorithm == Algorithms.HAUSDORFF:
        return _hausdorff.distance(a, b)
    elif algorithm == Algorithms.ERS:
        return _editdistance.ers(a, b, *args)
    elif algorithm == Algorithms.ERP:
        return _editdistance.erp(a, b, *args)
    elif algorithm == Algorithms.SPAD:
        return _spad.distance(a, b, *args)

    return ValueError(f"Algorithm '{algorithm}' not supported.")

def euclidean_distance(a, b):
    """
    Compute the Euclidean distance between two trajectories.

    The Euclidean distance is a simple metric that calculates the straight-line 
    distance between corresponding points in two trajectories. It assumes that 
    the trajectories are of the same length and aligned point-to-point.

    Parameters
    ----------
    a, b : list[tuple[float, float]]
        Trajectories represented as lists of (x, y) coordinate tuples.

    Returns
    -------
    float
        The Euclidean distance between the two trajectories.

    Notes
    -----
    - This metric is best suited for cases where trajectories are already 
      aligned and have the same length.
    - Euclidean distance is computationally efficient but does not handle 
      differences in trajectory lengths or misalignment well.

    Examples
    --------
    >>> a = [(0, 0), (1, 1), (2, 2)]
    >>> b = [(1, 1), (2, 2), (3, 3)]
    >>> stmeasures.euclidean_distance(a, b)
    2.449489742783178
    """
    return distance(a, b, Algorithms.EUCLIDEAN)


def hausdorff_distance(a, b):
    """
    Compute the Hausdorff distance between two trajectories.

    The Hausdorff distance measures the greatest distance from a point in one 
    trajectory to the closest point in the other trajectory. It quantifies the 
    "maximum mismatch" between two trajectories.

    Parameters
    ----------
    a, b : list[tuple[float, float]]
        Trajectories represented as lists of (x, y) coordinate tuples.

    Returns
    -------
    float
        The Hausdorff distance between the two trajectories.

    Notes
    -----
    - Suitable for applications where the maximum deviation between trajectories 
      is critical, such as detecting outliers or evaluating the worst-case alignment.
    - It is sensitive to noise and outliers, as it focuses on the largest discrepancy.

    Examples
    --------
    >>> a = [(0, 0), (1, 1), (2, 2)]
    >>> b = [(1, 1), (2, 2), (3, 3)]
    >>> stmeasures.hausdorff_distance(a, b)
    1.4142135623730951
    """
    return distance(a, b, Algorithms.HAUSDORFF)


def frechet_distance(a, b):
    """
    Compute the Frechet distance between two trajectories.

    The Frechet distance considers the location and ordering of points, making 
    it suitable for comparing the shapes of trajectories. It is often visualized 
    as the shortest leash needed for a person and a dog to walk along two curves 
    without retracing steps.

    Parameters
    ----------
    a, b : list[tuple[float, float]]
        Trajectories represented as lists of (x, y) coordinate tuples.

    Returns
    -------
    float
        The Frechet distance between the two trajectories.

    Notes
    -----
    - Ideal for shape-based trajectory comparisons, such as analyzing similar 
      movement patterns.
    - Handles trajectory misalignment but assumes continuous traversal.

    Examples
    --------
    >>> a = [(0, 0), (1, 1), (2, 2)]
    >>> b = [(0, 0), (1, 2), (2, 2)]
    >>> stmeasures.frechet_distance(a, b)
    1.0
    """
    return distance(a, b, Algorithms.FRECHET)


def lcss_distance(a, b, sigma=1.0):
    """
    Compute the Longest Common Subsequence (LCSS) distance between two trajectories.

    The LCSS distance measures the similarity between trajectories by finding the 
    longest subsequence of matching points within a given tolerance `sigma`. It 
    handles noise and trajectory misalignment well.

    Parameters
    ----------
    a, b : list[tuple[float, float]]
        Trajectories represented as lists of (x, y) coordinate tuples.
    sigma : float, optional
        The tolerance for matching points. Defaults to 1.0.

    Returns
    -------
    float
        The LCSS distance between the two trajectories.

    Notes
    -----
    - Effective for scenarios with noisy or incomplete data, such as GPS tracking.
    - Robust to outliers, as it focuses on subsequences rather than point-by-point comparison.

    Examples
    --------
    >>> a = [(0, 0), (1, 1), (2, 2)]
    >>> b = [(0, 0), (1, 2), (2, 2)]
    >>> stmeasures.lcss_distance(a, b, sigma=1.0)
    1.0
    """
    return distance(a, b, Algorithms.LCSS, sigma)


def spatial_assembling_distance(a, b, epsilon=1.0):
    """
    Compute the Spatial Assembling Distance (SPAD) between two trajectories.

    The SPAD distance evaluates the spatial similarity of trajectories based on 
    assembling smaller spatial segments. It is particularly useful for analyzing 
    highly fragmented or irregular trajectories.

    Parameters
    ----------
    a, b : list[tuple[float, float]]
        Trajectories represented as lists of (x, y) coordinate tuples.
    epsilon : float, optional
        The threshold for assembling segments. Defaults to 1.0.

    Returns
    -------
    float
        The SPAD distance between the two trajectories.

    Notes
    -----
    - Useful for comparing irregular or complex trajectory shapes.
    - Balances global and local trajectory characteristics through its segment-based approach.

    Examples
    --------
    >>> a = [(0, 0), (1, 1), (2, 4)]
    >>> b = [(0, 0), (1, 2), (0, 1)]
    >>> stmeasures.spatial_assembling_distance(a, b)
    0.5
    """
    return distance(a, b, Algorithms.SPAD, epsilon)
