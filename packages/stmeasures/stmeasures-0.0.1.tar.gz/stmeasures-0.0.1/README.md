# Similar Trajectories Measurements (`stmeasures`)

`stmeasures` is a Python library designed to provide researchers in Geographic Information Systems (GIS) and related fields with simple and efficient tools for measuring the similarity between trajectories. This library supports a variety of use cases, scenarios, and contexts, depending on where, how, and why the trajectories were collected or analyzed.

## Installation

Install it through PyPI:

```sh
pip install stmeasures
```

## Usage

Once installed you can use all functionalites provided by this package.

```py
import stmeasures

dataset = stmeasures.read_file("trajectories.json")
spad_metric = stmeasures.distance(dataset[4], dataset[53]) # Will get you the Spatial Assembling Distance between trajectories
```

### Visualization

Data can be visualized using [`geojsonio`](https://github.com/jwass/geojsonio.py) package.

```py
import stmeasures
import geojsonio

dataset = stmeasures.read_file("trajectories.json")
geojsonio.display(geojsonio.display(stmeasures.geojsonio_contents(trajectories=dataset[50:56]))) # Will display a map with the given trajectories in geojson.io
```

## Key Features

- **Diverse Algorithms:** Includes multiple algorithms such as Hausdorff, Frechet, DTW, LCSS, Euclidean, and SPAD to suit different similarity measurement needs.
- **Flexible Integration:** Offers modular functions and customizable parameters for specific trajectory analysis tasks.
- **Scalable Design:** Suitable for individual comparisons, clustering, and pattern discovery in trajectory datasets.

## Library Overview

The following diagram illustrates the structure and main components of the library:

![Library Structure](https://github.com/user-attachments/assets/cff1f913-684e-4fdb-9ca1-68eb275b6594)

## Use Cases

`stmeasures` can be used in a variety of applications, including:

1. **Trajectory Clustering:** Grouping similar movement patterns, such as vehicle paths or animal migrations.
2. **Outlier Detection:** Identifying unusual trajectories in a dataset.
3. **Pattern Matching:** Finding trajectories that follow a specific path or trend.
4. **Path Optimization Analysis:** Comparing planned and actual paths to optimize logistics or urban planning.

## About the Project

This project is part of a final bachelor's degree research initiative at IPN University (Mexico City, 2024). It aims to support GIS and data science communities with tools for trajectory similarity analysis. While still under development, the library is designed with extensibility and research-focused applications in mind.
