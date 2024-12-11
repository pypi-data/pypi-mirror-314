"""GeoJSON class."""

class GeoJSON:
    """
    Represents a GeoJSON data structure for storing trajectories.

    This class is used to load, store, and process GeoJSON data representing multiple 
    trajectories. It can extract relevant features like the trajectory coordinates, 
    IDs, and timestamps from raw GeoJSON data.

    :param data: Raw GeoJSON data in a list format, where each item contains features with 
                 geometry and properties related to the trajectory.
    :type data: list[dict]
    """

    def __init__(self, data):
        """
        Initializes the GeoJSON object with the provided data and extracts trajectories.

        :param data: Raw GeoJSON data to be processed into trajectory data.
        :type data: list[dict]
        """
        self._data = data
        self._trajectories = self._extract_trajectories()

    @property
    def data(self):
        return self._data

    @property
    def trajectories(self):
        return self._trajectories

    @property
    def trajectories_list(self) -> list[list[tuple[float, float]]]:
        """Returns trajectories as a list of trajectories."""
        return [
            [tuple(coordinates) for coordinates in trajectory['coordinates']]
            for trajectory in self.trajectories
        ]

    def __getitem__(self, index):
        return self.trajectories_list[index]

    def __len__(self):
        return len(self.trajectories_list)

    def _extract_trajectories(self):
        """
        Extracts trajectories from the raw GeoJSON data.

        This method scans through the GeoJSON data, looking for features with 
        geometry type 'LineString'. For each such feature, it extracts the 
        coordinates, trajectory ID, and timestamp, and stores them in a list.

        :return: A list of trajectories, each represented by a dictionary containing 
                 its 'id', 'timestamp', and 'coordinates'.
        :rtype: list[dict]
        """
        trajectories = []
        for item in self._data:
            features = item.get('features', [])
            for feature in features:
                if feature['geometry']['type'] == 'LineString':
                    coordinates = feature['geometry']['coordinates']
                    trajectories.append({
                        'id': feature['properties'].get('name'),
                        'timestamp': feature['properties'].get('tiempo'),
                        'coordinates': coordinates
                    })
        return trajectories
