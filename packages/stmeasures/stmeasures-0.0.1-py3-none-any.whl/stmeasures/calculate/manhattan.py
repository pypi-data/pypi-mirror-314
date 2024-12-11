"""Manhattan algorithm class."""

import ctypes

from stmeasures.calculate.base import BaseAlgorithm

class Manhattan(BaseAlgorithm):
    """A manhattan instance that mainly computes the manhattan algorithm
    between two trajectories-like (`list[float]`).

    Parameters
    ----------
    libname : str, default: "libmanhattan"
        The file name of the compiled shared library.

    Examples
    --------
    Calculating the manhattan distance of Point 1 (1, 2) and Point 2 (3, 4)

    >>> manhattan = Manhattan() # Intializes object and loads shared library
    >>> manhattan.distance([1, 2], [3, 4]) # |1 - 3| + |2 - 4| = 4
    4.0
    """

    def __init__(self, libname="libmanhattan") -> None:
        super().__init__(libname)

    def distance(
            self,
            p: list[float],
            q: list[float]
        ) -> float:
        """Return the manhattan distance between two trajectories.

        Parameters
        ----------
        p : list[float]
            A first vector in n-space
        q : list[float]
            A second vector in n-space
        """
        len_p = len(p)

        # TODO: Validate in `validate` module

        doublearray = ctypes.c_double * len_p
        self.lib.m_distance.argtypes = [
            doublearray,
            doublearray,
            ctypes.c_size_t,
        ]
        self.lib.m_distance.restype = ctypes.c_double

        return self.lib.m_distance(doublearray(*p), doublearray(*q), len_p)
