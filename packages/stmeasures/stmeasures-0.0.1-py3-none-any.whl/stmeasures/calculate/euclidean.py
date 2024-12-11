"""Euclidean algorithm class."""

import ctypes
import warnings

from stmeasures.validation import validate_euclidean, validate_trajectory
from stmeasures.calculate.base import BaseAlgorithm
# from stmeasures.objects.cstructures import Trajectory, Point # TODO: Implement

class Euclidean(BaseAlgorithm):
    """
    An instance for calculating the Euclidean distance between two lists of
    floats (trajectories).

    :param libname: 
        The file name of the compiled shared library.
    :type libname: str, default "libeuclidean"

    :example:
        Calculating the Euclidean distance between two points:

        >>> euclidean = Euclidean()  # Initializes object and loads shared library
        >>> euclidean.distance([(1, 2)], [(3, 4)])
        2.8284271247461903
    """

    def __init__(self, libname="libeuclidean") -> None:
        """
        Initializes the Euclidean distance calculator with a specified library
        name.

        :param libname: 
            The file name of the compiled shared library.
        :type libname: str, default "libeuclidean"
        """
        super().__init__(libname)

    def distance(
            self,
            p: list[tuple[float, float]],
            q: list[tuple[float, float]],
            validate: bool = False
        ) -> float:
        """
        Calculates the Euclidean distance between two trajectories.

        :param p:
            The first trajectory in Euclidean n-space.
        :type p: list[float]

        :param q:
            The second trajectory in Euclidean n-space.
        :type q: list[float]

        :return: The Euclidean distance between the two trajectories.
        :rtype: float

        :raises ValueError:
            - if `p` or `q` is not a valid trajectory
            - if `p` or `q` is not a list of floats or if they do not have the
              same length

        :raises RuntimeError:
            - if there is an error with the C library call
            - if an unexpected error occurs during execution

        :example:
            Calculating the Euclidean distance between two vectors:

            >>> euclidean = Euclidean()
            >>> euclidean.distance([(1.0, 2.0)], [(3.0, 4.0)])
            2.8284271247461903
        """
        try:
            if validate:
                validate_trajectory(p)
                validate_trajectory(q)
            else:
                warnings.warn("Args not validating", ResourceWarning)

            _p = [p_value for _tuple in p for p_value in _tuple]
            _q = [q_value for _tuple in q for q_value in _tuple]

            validate_euclidean(_p, _q)

            return self._distance(_p, _q)
        except ValueError as ve:
            print(ve)
            raise RuntimeError(
                f"Invalid parameters p:{p}, q:{q} in {self.__module__}"
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

    def _distance(self, p: list[float], q: list[float]) -> float:
        """
        Calculates the Euclidean distance between two vectors.

        :param p:
            The first vector in Euclidean n-space.
        :type p: list[float]

        :param q:
            The second vector in Euclidean n-space.
        :type q: list[float]

        :return: The Euclidean distance between the two input vectors.
        :rtype: float
        """
        warnings.warn('Method not using cstructures', DeprecationWarning)

        len_p = len(p)

        doublearray = ctypes.c_double * len_p
        self.lib.distance.argtypes = [
            doublearray,
            doublearray,
            ctypes.c_size_t,
        ]
        self.lib.distance.restype = ctypes.c_double

        return self.lib.distance(doublearray(*p), doublearray(*q), len_p)
