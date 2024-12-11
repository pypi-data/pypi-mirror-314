"""LCSS algorithm class."""

import ctypes
import warnings

from stmeasures.validation import validate_lcss, validate_trajectory
from stmeasures.calculate.base import BaseAlgorithm
# from stmeasures.objects.cstructures import Trajectory, Point # TODO: Implement

class LCSS(BaseAlgorithm):
    """
    A class to compute the Longest Common Subsequences (LCSS) algorithm between 
    two trajectory-like lists of floats.

    :param libname: The file name of the compiled shared library.
    :type libname: str, optional, default is "liblcss"

    :example:

    Calculating the LCSS distance between two points, (1, 2) and (3, 4):

    >>> lcss = LCSS()  # Initializes object and loads shared library
    >>> lcss.distance([(1, 2)], [(3, 4)])
    0.5
    """

    def __init__(self, libname="liblcss") -> None:
        super().__init__(libname)

    def distance(
        self,
        r: list[tuple[float, float]],
        s: list[tuple[float, float]],
        sigma: float = 1,
        validate: bool = False
    ) -> float:
        """
        Calculate the LCSS distance between two trajectories.

        :param r: First trajectory, a list of (latitude, longitude) tuples.
        :type r: list[tuple[float, float]]
        :param s: Second trajectory, a list of (latitude, longitude) tuples.
        :type s: list[tuple[float, float]]
        :param sigma: Threshold to detect matching elements, defaults to 1.
        :type sigma: float, optional

        :raises ValueError: If the trajectories or sigma are invalid.
        :raises RuntimeError: If a ctypes error occurs.

        :return: LCSS distance between the two trajectories.
        :rtype: float
        """
        try:
            if validate:
                validate_trajectory(r)
                validate_trajectory(s)
            else:
                warnings.warn("Args not validating", ResourceWarning)

            _r = [r_value for _tuple in r for r_value in _tuple]
            _s = [s_value for _tuple in s for s_value in _tuple]

            validate_lcss(_r, _s, sigma)

            return self._distance(_r, _s, sigma)
        except ValueError as ve:
            print(ve)
            raise RuntimeError(
                f"Invalid parameters r:{r}, s:{s} in {self.__module__}"
            ) from ve
        except ctypes.ArgumentError as ae:
            print(ae)
            raise RuntimeError(
                f"Argument error in C shared library call {self._libpath}"
            ) from ae
        except Exception as e:
            print(e)
            raise RuntimeError(
                f"Unexpected error in {self.__module__}"
            ) from e

    def _distance(
        self,
        r: list[float],
        s: list[float],
        sigma: float = 1
    ) -> float:
        """
        Internal method to calculate the LCSS distance between two flattened 
        trajectories.

        :param r: Flattened list representing the first trajectory.
        :type r: list[float]
        :param s: Flattened list representing the second trajectory.
        :type s: list[float]
        :param sigma: Threshold to detect matching elements, defaults to 1.
        :type sigma: float, optional

        :raises DeprecationWarning: This method is deprecated since it's not
        using cstructures.

        :return: LCSS distance between the two trajectories.
        :rtype: float
        """
        warnings.warn('Method not using cstructures', DeprecationWarning)

        len_r, len_s = len(r), len(s)

        r_array = ctypes.c_double * len_r
        s_array = ctypes.c_double * len_s

        self.lib.distance.argtypes = [
            r_array,
            s_array,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
        ]
        self.lib.distance.restype = ctypes.c_double

        return self.lib.distance(
            r_array(*r),
            s_array(*s),
            len_r,
            len_s,
            sigma
        )
