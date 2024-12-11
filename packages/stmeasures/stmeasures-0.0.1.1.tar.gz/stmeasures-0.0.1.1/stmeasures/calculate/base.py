"""Base algorithm class and utilities."""

import ctypes

from stmeasures.calculate import _libpath

class BaseAlgorithm():
    """Base class for distance calculation algorithms.

    Provides a simple way to load shared libraries (`.so` files) implemented
    and built in C.

    Parameters
    ----------
    libname : str
        The library name (i.e.: the file name without the file extension).

    Attributes
    ----------
    lib : ctypes.CDLL
        A loaded shared library that implements the algorithm in C.
    """

    def __init__(self, libname: str) -> None:
        self._libpath = _libpath(libname)
        self._lib = None

        self._load_library()

    @property
    def lib(self) -> ctypes.CDLL:
        """Return loaded shared library."""
        if hasattr(self, '_lib') and isinstance(self._lib, ctypes.CDLL):
            return self._lib
        else:
            raise RuntimeError(
                f"Shared library '{self._libpath}' is not loaded"
            )

    def _load_library(self) -> None:
        """Load shared library."""
        try:
            self._lib = ctypes.CDLL(self._libpath)
        except OSError as ose:
            raise RuntimeError(
                f"Failed to load the shared library '{self._libpath}':\n"
                + f"{ose}"
            )
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while loading '{self._libpath}'"
                + f":\n{e}"
            )
