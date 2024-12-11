"""Visualize module."""

import json
import random
from warnings import warn as _warn

def _swap_coordinates(coords):
    """
    Swap latitude and longitude for each coordinate tuple in a trajectory.

    This function takes a list of coordinates, where each coordinate is represented 
    as a tuple of (latitude, longitude), and returns the list with the order swapped 
    to (longitude, latitude). This is often required for proper visualization in 
    some mapping libraries that expect coordinates in the (longitude, latitude) order.

    :param coords: List of coordinate tuples in (latitude, longitude) format.
    :type coords: list[list[float, float]]
    :return: List of coordinates in (longitude, latitude) format.
    :rtype: list[list[float, float]]
    """
    return [[lon, lat] for lat, lon in coords]

def _random_color() -> str:
    """
    Generates a random color in hexadecimal format.

    :return: A string representing a random color in the format `#RRGGBB`.
    :rtype: str
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def geojsonio_contents(**kwargs) -> str:
    """
    Generate a GeoJSON string for visualization with geojson.io from input trajectory data.

    :param kwargs: Keyword arguments to specify trajectory data. Must include one of the following:
    
        - `trajectories` (list): A list of trajectories, where each trajectory is a list of 
          coordinates (each coordinate is a 2-element list of floats).
          
        - `trajectory` (list): A single trajectory, represented as a list of coordinates 
          (each coordinate is a tuple of two floats).

        - `swapcoords` (bool): A flag to swap latitudes with longitudes.
    
    :type kwargs: dict
    :return: A GeoJSON string formatted as either a FeatureCollection (for multiple trajectories) 
             or a LineString (for a single trajectory).
    :rtype: str

    :raises ValueError: If no arguments are provided or if the provided arguments do not 
                        match the expected format.

    **Examples**

    .. code-block:: python

        get_geojsonio_contents(
            trajectories=[[[19.603914, -99.01801], [19.60482, -99.016198]]]
        )
        # Output:
        # '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": 
        # {"type": "LineString", "coordinates": [[-99.01801, 19.603914], [-99.016198, 
        # 19.60482]]}, "properties": {}}]}'

        get_geojsonio_contents(
            trajectory=[(19.603914, -99.01801), (19.60482, -99.016198)]
        )
        # Output:
        # '{"type": "LineString", "coordinates": [[-99.01801, 19.603914], [-99.016198, 
        # 19.60482]]}'

    .. note::
        This function expects coordinates to be in the format [latitude, longitude] for 
        `trajectories` or (latitude, longitude) for `trajectory`. The `_swap_coordinates` 
        helper function is used to adjust coordinates to the required [longitude, latitude] 
        order for GeoJSON output.
    """
    if not kwargs:
        raise ValueError("No argument provided")

    trajectories = kwargs.get("trajectories") or [kwargs.get("trajectory") or None]
    swapcoords = kwargs.get("swapcoords") or True

    if isinstance(trajectories, list) and isinstance(trajectories[0], list):
        dt = [-1 for _ in trajectories]
        indexes = kwargs.get("indexes") or []
        indexes = indexes if len(indexes) == len(trajectories) else dt

        return json.dumps({
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": _swap_coordinates(trajectories[i])\
                        if swapcoords else trajectories[i]
                    },
                    "properties": {
                        "index": indexes[i],
                        "stroke": _random_color(),
                        "stroke-width": 2,
                        "stroke-opacity": 1
                    }
                }
                for i in range(len(trajectories))
            ]
        })

    raise ValueError("No valid argument provided")

def get_geojsonio_trajectory(trajectory_data, swapcoords=True):
    """
    Convert a single trajectory to a GeoJSON LineString format.

    This function converts a single trajectory, represented as a dictionary with 
    trajectory details, into the GeoJSON format. The resulting GeoJSON is in the 
    form of a `LineString`, with coordinates swapped to (longitude, latitude) format.

    :param trajectory_data: A dictionary with trajectory details, including 'coordinates'.
    :type trajectory_data: dict
    :return: GeoJSON dictionary for the trajectory in LineString format.
    :rtype: dict
    """
    _warn("Use get_geojsonio_contents instead.")

    coords = trajectory_data['coordinates']
    if swapcoords:
        coords = _swap_coordinates(coords)

    geojson = {
        "type": "LineString",
        "coordinates": coords
    }
    return geojson

def get_geojson_trajectories(geojson_obj):
    """
    Convert all trajectories to GeoJSON FeatureCollection format.

    This function takes a `GeoJSON` object containing multiple trajectories and 
    converts them into a GeoJSON `FeatureCollection` format. Each trajectory is 
    represented as a `Feature` with a `LineString` geometry and properties such as 
    the trajectory's 'id' and 'timestamp'.

    :param geojson_obj: GeoJSON object containing multiple trajectories.
    :type geojson_obj: GeoJSON
    :return: GeoJSON FeatureCollection for all trajectories.
    :rtype: dict
    """
    _warn("Use get_geojsonio_contents instead.")

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for trajectory_data in geojson_obj.trajectories:
        geojson['features'].append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": (trajectory_data['coordinates'])
            },
            "properties": {
                "id": trajectory_data['id'],
                "timestamp": trajectory_data['timestamp']
            }
        })
    return geojson
