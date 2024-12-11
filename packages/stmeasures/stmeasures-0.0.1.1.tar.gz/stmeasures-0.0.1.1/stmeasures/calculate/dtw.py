"""DTW algorithm class."""

import ctypes
# import warnings

# from stmeasures.validation import validate_dtw
from stmeasures.calculate.base import BaseAlgorithm
from stmeasures.objects.cstructures import Trajectory, Point

class DTW(BaseAlgorithm):
    """
    DTW (Dynamic Time Warping) algorithm class for calculating the similarity 
    between two sequences of geographical coordinates.

    Inherits from
    -------------
    BaseAlgorithm : stmeasures.calculate.base.BaseAlgorithm
        The base class for algorithms in the stmeasures library.

    Methods
    -------
    distance(seq1, seq2)
        Computes the DTW distance between two coordinate sequences.
    """

    def __init__(self, libname="libdtw") -> None:
        """
        Initializes the DTW class and loads the dynamic library for DTW computation.

        Parameters
        ----------
        libname : str, optional
            The name of the dynamic library to load (default is "libdtw").
        """
        super().__init__(libname)

        self.lib.dtw_execute.argtypes = [ctypes.POINTER(Trajectory), ctypes.POINTER(Trajectory)]
        self.lib.dtw_execute.restype = ctypes.c_double

    def distance(self, seq1: list[tuple[float, float]], seq2: list[tuple[float, float]]) -> float:
        """
        Computes the DTW distance between two sequences of coordinates.

        Parameters
        ----------
        seq1 : list of tuple of float
            The first sequence of (latitude, longitude) tuples.
        seq2 : list of tuple of float
            The second sequence of (latitude, longitude) tuples.

        Returns
        -------
        float
            The DTW distance between the two sequences of coordinates.
        """
        # warnings.warn('Args not validating')

        seq1_points = (Point * len(seq1))(*[Point(lat, lon) for lat, lon in seq1])
        seq2_points = (Point * len(seq2))(*[Point(lat, lon) for lat, lon in seq2])

        seq1_c = Trajectory(seq1_points, len(seq1))
        seq2_c = Trajectory(seq2_points, len(seq2))

        return self.lib.dtw_execute(ctypes.byref(seq1_c), ctypes.byref(seq2_c))
