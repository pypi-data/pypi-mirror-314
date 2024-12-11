# ClustIce

A tool to generate exotic ice clusters.

version 0.7.1

## Requirements

* python
* numpy
* networkx
* scikit-learn
* cycless


## Installation

ClustIce is registered to [PyPI (Python Package Index)](https://pypi.python.org/pypi/GenIce).
Install with pip3.

    pip3 install clustice

## Uninstallation

    pip3 uninstall clustice

## API

API manual is [here](https://clustice.github.io/ClustIce).

## Examples

Make an icosahedral ice cluster.

```python
import numpy as np
import networkx as nx

import genice_core
from clustice.geometry import make_layout
from clustice.gromacs import render
from clustice.water import tip4p
from clustice import graph

# O-O distance
L = 0.27

# note: g must be a graph whose labels start from 0.
# g = graph.great_icosahedron(12, separation=L)
g = graph.great_decahedron(12)
# g = graph.small_barrelan()
# g = graph.large_barrelan()
# g = graph.twistane()
# g = graph.adamantane()
# g = nx.cycle_graph(6) # hexagon
# g = nx.cycle_graph(7) # heptagon
# g = nx.cubical_graph() # cubic octamer
# g = nx.dodecahedral_graph()


if "pos" in g.nodes[0]:
    # extract the embedded coords in g
    layout = np.array([g.nodes[v]["pos"] for v in g])
else:
    # estimate of the positions of the nodes
    layout = make_layout(g, edgelen=L)

# set orientations of the hydrogen bonds.
# if vertexPositions is given, the net dipole moment is minimized.
dg = genice_core.ice_graph(g, vertexPositions=layout, dipoleOptimizationCycles=100)

# put water molecules
gro = render(dg, layout, watermodel=tip4p)
with open("sample.gro", "w") as f:
    f.write(gro)
```
