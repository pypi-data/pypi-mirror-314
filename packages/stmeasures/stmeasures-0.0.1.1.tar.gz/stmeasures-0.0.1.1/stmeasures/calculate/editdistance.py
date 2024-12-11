"""Edit Distance algorithm class."""

import ctypes
import warnings

from stmeasures.validation import validate_ers, validate_erp, validate_trajectory
from stmeasures.calculate.base import BaseAlgorithm
# from stmeasures.objects.cstructures import Trajectory, Point # TODO: Implement

class EditDistance(BaseAlgorithm):
    """
    A class to compute edit distances between two trajectory-like lists of floats.

    :param libname: The file name of the compiled shared library.
    :type libname: str, optional, default is "libeditdist"

    :example:

    Calculating the Edit Distance with Real Penalty between two points, (1, 2) and (3, 4):

    >>> editdistance = EditDistance()  # Initializes object and loads shared library
    >>> editdistance.erp([(1, 2)], [(3, 4)])
    4.0
    """

    def __init__(self, libname="libeditdist") -> None:
        super().__init__(libname)

    def ers(
        self,
        r: list[tuple[float, float]],
        s: list[tuple[float, float]],
        sigma: float = 1.0,
        cost_deletion: float = 1.0,
        cost_insertion: float = 1.0,
        subcost_within_sigma: float = 0.0,
        subcost_outside_sigma: float = 1.0,
        validate: bool = False
    ) -> float:
        """
        Calculate the Edit Distance on Real Sequences (ERS).

        :param r: First trajectory, a list of (latitude, longitude) tuples.
        :type r: list[tuple[float, float]]
        :param s: Second trajectory, a list of (latitude, longitude) tuples.
        :type s: list[tuple[float, float]]
        :param sigma: Matching threshold (tolerance), defaults to 1.0.
        :type sigma: float, optional
        :param cost_deletion: Cost of deleting an element to match the sequence, defaults to 1.0.
        :type cost_deletion: float, optional
        :param cost_insertion: Cost of adding an element to match the sequence, defaults to 1.0.
        :type cost_insertion: float, optional
        :param subcost_within_sigma: Substitution cost when the threshold is matched, defaults to 0.0.
        :type subcost_within_sigma: float, optional
        :param subcost_outside_sigma: Substitution cost when the threshold is not matched, defaults to 1.0.
        :type subcost_outside_sigma: float, optional

        :raises ValueError: If the trajectories or parameters are invalid.
        :raises RuntimeError: If a ctypes error occurs.

        :return: The computed ERS distance between the two trajectories.
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

            validate_ers(
                _r,
                _s,
                sigma,
                cost_deletion,
                cost_insertion,
                subcost_within_sigma,
                subcost_outside_sigma
            )

            return self._ers(
                _r,
                _s,
                sigma,
                cost_deletion,
                cost_insertion,
                subcost_within_sigma,
                subcost_outside_sigma
            )
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

    def erp(
        self,
        r: list[tuple[float, float]],
        s: list[tuple[float, float]],
        g: float = 0.0,
        validate: bool = False
    ) -> float:
        """
        Calculate the Edit Distance with Real Penalty (ERP).

        :param r: First trajectory, a list of (latitude, longitude) tuples.
        :type r: list[tuple[float, float]]
        :param s: Second trajectory, a list of (latitude, longitude) tuples.
        :type s: list[tuple[float, float]]
        :param g: Gap constant for edit distance, defaults to 0.0.
        :type g: float, optional

        :raises ValueError: If the trajectories or gap constant are invalid.
        :raises RuntimeError: If a ctypes error occurs.

        :return: The computed ERP distance between the two trajectories.
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

            validate_erp(_r, _s, g)

            return self._erp(_r, _s, g)
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

    def _ers(
        self,
        r: list[float],
        s: list[float],
        sigma: float = 1.0,
        cost_deletion: float = 1.0,
        cost_insertion: float = 1.0,
        subcost_within_sigma: float = 0.0,
        subcost_outside_sigma: float = 1.0
    ) -> float:
        """
        Internal method to calculate the Edit Distance on Real Sequences (ERS).

        :param r: Flattened list representing the first trajectory.
        :type r: list[float]
        :param s: Flattened list representing the second trajectory.
        :type s: list[float]
        :param sigma: Matching threshold (tolerance), defaults to 1.0.
        :type sigma: float, optional
        :param cost_deletion: Cost of deleting an element to match the sequence, defaults to 1.0.
        :type cost_deletion: float, optional
        :param cost_insertion: Cost of adding an element to match the sequence, defaults to 1.0.
        :type cost_insertion: float, optional
        :param subcost_within_sigma: Substitution cost when the threshold is matched, defaults to 0.0.
        :type subcost_within_sigma: float, optional
        :param subcost_outside_sigma: Substitution cost when the threshold is not matched, defaults to 1.0.
        :type subcost_outside_sigma: float, optional

        :raises DeprecationWarning: If the method does not use cstructures.

        :return: The computed ERS distance between the two trajectories.
        :rtype: float
        """
        warnings.warn('Method not using cstructures', DeprecationWarning)

        len_r, len_s = len(r), len(s)

        r_array = ctypes.c_double * len_r
        s_array = ctypes.c_double * len_s

        self.lib.ers.argtypes = [
            r_array,
            s_array,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
        ]
        self.lib.ers.restype = ctypes.c_double

        return self.lib.ers(
            r_array(*r),
            s_array(*s),
            len_r,
            len_s,
            sigma,
            cost_deletion,
            cost_insertion,
            subcost_within_sigma,
            subcost_outside_sigma
        )

    def _erp(
        self,
        r: list[float],
        s: list[float],
        g: float = 0.0
    ) -> float:
        """
        Internal method to calculate the Edit Distance with Real Penalty (ERP).

        :param r: Flattened list representing the first trajectory.
        :type r: list[float]
        :param s: Flattened list representing the second trajectory.
        :type s: list[float]
        :param g: Gap constant for edit distance, defaults to 0.0.
        :type g: float, optional

        :raises DeprecationWarning: If the method does not use cstructures.

        :return: The computed ERP distance between the two trajectories.
        :rtype: float
        """
        warnings.warn('Method not using cstructures', DeprecationWarning)

        len_r, len_s = len(r), len(s)

        r_array = ctypes.c_double * len_r
        s_array = ctypes.c_double * len_s

        self.lib.erp.argtypes = [
            r_array,
            s_array,
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
        ]
        self.lib.erp.restype = ctypes.c_double

        return self.lib.erp(
            r_array(*r),
            s_array(*s),
            len_r,
            len_s,
            g
        )
