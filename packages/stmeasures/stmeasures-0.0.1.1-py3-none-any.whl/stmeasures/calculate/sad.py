"""SAD algorithm class."""

import ctypes

from stmeasures.validation import validate_trajectory
from stmeasures.calculate.base import BaseAlgorithm
from stmeasures.objects.cstructures import Trajectory

class SAD(BaseAlgorithm):
    """
    A class to compute the Spatial Assembling Distance (SAD) algorithm 
    between two trajectory-like lists of floats.

    :param libname: The file name of the compiled shared library.
    :type libname: str, optional, default is "libsad"

    :example:

    Calculating the SAD distance between two trajectories:

    >>> sad = SAD()  # Initializes object and loads shared library
    >>> sad.distance([(1, 2), (3, 4)], [(5, 6), (7, 8)], epsilon=1.0)
    0.8
    """

    def __init__(self, libname="libsad") -> None:
        super().__init__(libname)

    def distance(
        self,
        r: list[tuple[float, float]],
        s: list[tuple[float, float]],
        epsilon: float = 1.0
    ) -> float:
        """
        Calculate the SAD distance between two trajectories.

        :param r: First trajectory, a list of (latitude, longitude) tuples.
        :type r: list[tuple[float, float]]
        :param s: Second trajectory, a list of (latitude, longitude) tuples.
        :type s: list[tuple[float, float]]
        :param epsilon: Threshold to cluster points, defaults to 1.0.
        :type epsilon: float, optional

        :raises ValueError: If the trajectories or epsilon are invalid.
        :raises RuntimeError: If a ctypes error occurs.

        :return: SAD distance between the two trajectories.
        :rtype: float
        """
        try:
            validate_trajectory(r)
            validate_trajectory(s)

            trajectory1 = Trajectory.from_list(r)
            trajectory2 = Trajectory.from_list(s)

            return self._distance(trajectory1, trajectory2, epsilon)
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
        trajectory1: Trajectory,
        trajectory2: Trajectory,
        epsilon: float
    ) -> float:
        """
        Internal method to calculate the SAD distance using ctypes.

        :param trajectory1: First trajectory as a C structure.
        :type trajectory1: Trajectory
        :param trajectory2: Second trajectory as a C structure.
        :type trajectory2: Trajectory
        :param epsilon: Threshold to cluster points, defaults to 1.0.
        :type epsilon: float, optional

        :return: SAD distance between the two trajectories.
        :rtype: float
        """

        self.lib.spatial_assembling_distance.argtypes = [
            ctypes.POINTER(Trajectory),
            ctypes.POINTER(Trajectory),
            ctypes.c_double
        ]
        self.lib.spatial_assembling_distance.restype = ctypes.c_double


        result = self.lib.spatial_assembling_distance(
            ctypes.byref(trajectory1),
            ctypes.byref(trajectory2),
            epsilon
        )

        return result

