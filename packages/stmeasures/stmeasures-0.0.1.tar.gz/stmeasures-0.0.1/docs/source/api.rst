Library API
===========

The `stmeasures` library is organized into modules that provide specialized functionality for trajectory similarity measurement. To ensure ease of use, the primary functions from these modules are exposed directly in the library's top-level interface. This means users can access the most essential features without delving into the internal module structure.

.. code-block:: python

    import stmeasures
    # Calculate the Hausdorff distance between two trajectories
    distance = stmeasures.hausdorff_distance(trajectory_a, trajectory_b)
    # Load trajectories from a GeoJSON file
    geojson_data = stmeasures.read_geojson("trajectories.geojson")
    # Get contents that can be visualized
    geojsonio.display(stmeasures.geojsonio_contents(trajectories=geojson_data[50:56]))
    
.. toctree::

   calculates
   read
   visualize
