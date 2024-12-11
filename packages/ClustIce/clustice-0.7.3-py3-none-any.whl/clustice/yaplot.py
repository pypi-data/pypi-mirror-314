import numpy as np
import yaplotlib as yap


def render(
    g,
    layout: dict,
):
    s = ""

    # assume g is a nx.Graph
    s += yap.Color(2)
    s += yap.Layer(1)
    for i in g:
        s += yap.Text(layout[i], f"{i}")

    s += yap.Color(3)
    s += yap.Layer(2)
    for i, j in g.edges():
        s += yap.Line(layout[i], layout[j])
    return s
