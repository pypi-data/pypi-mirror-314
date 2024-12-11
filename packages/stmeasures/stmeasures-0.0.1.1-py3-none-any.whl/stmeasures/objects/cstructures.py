import ctypes
class Point(ctypes.Structure):
    """
    Represents a geographical point with latitude and longitude coordinates.

    Attributes
    ----------
    latitude : ctypes.c_double
        Latitude of the point.
    longitude : ctypes.c_double
        Longitude of the point.
    """
    _fields_ = [("latitude", ctypes.c_double), ("longitude", ctypes.c_double)]


class Trajectory(ctypes.Structure):
    """
    Represents a sequence of geographical points.

    Attributes
    ----------
    points : ctypes.POINTER(Point)
        A pointer to an array of `Point` structures.
    size : ctypes.c_size_t
        The size of the coordinate sequence (number of points).
    """
    _fields_ = [("points", ctypes.POINTER(Point)), ("size", ctypes.c_size_t)]
    
    @classmethod
    def from_list(cls, points: list[tuple[float, float]]):
        """
        Convert a list of (latitude, longitude) tuples into a Trajectory instance.

        :param points: List of tuples containing latitude and longitude.
        :type points: list[tuple[float, float]]
        :return: A Trajectory instance with the points converted to Point objects.
        :rtype: Trajectory
        """
        
        point_array = (Point * len(points))(*[Point(latitude=lat, longitude=lon) for lat, lon in points])

        trajectory = cls(points=ctypes.cast(point_array, ctypes.POINTER(Point)), size=len(points))
        return trajectory
