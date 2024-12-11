"""Calculation algorithms."""

import os

def _libpath(libname: str):
    clibpath = f"../../stmeasures-clib/{libname}.so"
    pkgpath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pkgpath, clibpath)
