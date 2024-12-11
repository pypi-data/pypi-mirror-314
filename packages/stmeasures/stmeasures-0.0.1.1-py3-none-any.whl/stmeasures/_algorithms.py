from enum import Enum as _Enum

class Algorithms(str, _Enum):
    """
    Enum for distance algorithms, categorizing types based on application
    context (spatial, temporal, geometrical, sequential).

    Attributes
    ----------
    EUCLIDEAN : str
        Standard Euclidean distance, often used for spatial measurements.
    DTW : str
        Dynamic Time Warping, useful for time series alignment and measuring
        similarity in temporal sequences.
    LCSS : str
        Longest Common Subsequence on real sequences, applicable for matching
        patterns in sequential data.
    FRECHET : str
        Frechet distance, commonly used in geometrical contexts for comparing
        curves.
    HAUSDORFF : str
        Hausdorff distance, used for comparing geometrical shapes or spatial
        sets.
    ERS : str
        Edit Distance on Real Sequences, useful for sequential data comparison
        with real values.
    ERP : str
        Edit Distance with Real Penalty, used for sequence comparison with a
        penalty for gaps in sequences.

    Class Attributes
    ----------------
    SEQUENTIAL : list[Algorithms]
        Group of algorithms suitable for sequential data (ERP, ERS, LCSS).
    TEMPORAL : list[Algorithms]
        Group of algorithms suitable for temporal data, which includes DTW and
        sequential algorithms.
    GEOMETRICAL : list[Algorithms]
        Group of algorithms suitable for geometrical measurements (Hausdorff,
        Frechet).
    SPATIAL : list[Algorithms]
        Group of algorithms suitable for spatial measurements, including
        Euclidean and geometrical algorithms.

    Methods
    -------
    __str__() -> str
        Returns a formatted string representation of the algorithm with class,
        enum name, and value.
    """
    
    EUCLIDEAN = "euclidean"
    DTW = "dynamic_time_warping"
    LCSS = "longest_common_subsequence"
    FRECHET = "frechet"
    HAUSDORFF = "hausdorff"
    ERS = "edit_distance_real_sequence"
    ERP = "edit_distance_real_penalty"
    SPAD = "spatial_assembling_distance"

    SEQUENTIAL = [ERP, ERS, LCSS]
    TEMPORAL = [DTW, *SEQUENTIAL]
    GEOMETRICAL = [HAUSDORFF, FRECHET]
    SPATIAL = [EUCLIDEAN, *GEOMETRICAL, SPAD]

    def __str__(self) -> str:
        """
        Returns a string representation of the algorithm instance.

        Returns
        -------
        str
            A formatted string that includes the class name, enum name, and
            value.
        """
        _class = self.__class__.__name__
        _enum = self.name
        _value = super().__str__()
        return f"{_class}.{_enum} ({_value})"
