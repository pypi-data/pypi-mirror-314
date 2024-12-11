import networkx as nx
import numpy as np
from pairlist import pairs_iter


def _create_graph(coords, threshold=0.35):
    # Initialize graph
    g = nx.Graph()

    # Add nodes to the graph
    for i in range(len(coords)):
        ## MM: set coord of the node when it is added.
        g.add_node(i, pos=coords[i])

    # Compute pairwise distances and add edges when distance < threshold
    for i, j, L in pairs_iter(coords, maxdist=threshold):
        g.add_edge(i, j)

    return g


def great_icosahedron(ns=1, separation=0.27):
    """
    The `great_icosahedron` function generates the coordinates of atoms in a great icosahedron structure
    based on the specified parameters.

    Args:
      ns: The parameter `ns` represents the size of the icosahedron. It determines the number of
    subdivisions made on each face of the icosahedron. The higher the value of `ns`, the more
    subdivisions and smaller the resulting structure will be. Defaults to 1
      separation: The "separation" parameter represents the distance between atoms in the icosahedron
    structure, measured in nanometers (nm).

    Returns:
      a graph object.
    """

    def compute_vertices():
        phi = float((1 + np.sqrt(5)) / 2)  # 1.618
        return np.array(
            [
                [1, 1, 1],
                [1, 1, -1],
                [1, -1, 1],
                [1, -1, -1],
                [-1, 1, 1],
                [-1, 1, -1],
                [-1, -1, 1],
                [-1, -1, -1],
                [0, phi, 1 / phi],
                [0, phi, -1 / phi],
                [0, -phi, 1 / phi],
                [0, -phi, -1 / phi],
                [phi, 1 / phi, 0],
                [phi, -1 / phi, 0],
                [-phi, 1 / phi, 0],
                [-phi, -1 / phi, 0],
                [1 / phi, 0, phi],
                [1 / phi, 0, -phi],
                [-1 / phi, 0, phi],
                [-1 / phi, 0, -phi],
            ]
        )

    def compute_faces():
        return np.array(
            [
                [0, 1, 8, 9, 12],
                [0, 4, 8, 16, 18],
                [0, 2, 12, 13, 16],
                [1, 3, 12, 13, 17],
                [1, 5, 9, 17, 19],
                [2, 6, 10, 16, 18],
                [2, 3, 10, 11, 13],
                [6, 7, 10, 11, 15],
                [4, 6, 14, 15, 18],
                [5, 7, 14, 15, 19],
                [4, 5, 8, 9, 14],
                [3, 7, 11, 17, 19],
            ]
        )

    def compute_vertices_to_faces(vertices, faces):
        vertices_to_faces = []  # which 3 faces a vertice is among
        for i in range(len(vertices)):
            face_list = []
            for j in range(len(faces)):
                if i in faces[j]:
                    face_list.append(j)
            vertices_to_faces.append(face_list)
        return np.array(vertices_to_faces)

    def compute_scaled_vertices(vertices, scale_factor):
        return vertices * scale_factor

    def compute_face_vectors(faces, vertices_scaled):
        face_vectors = []
        for face in faces:
            centroid = np.mean(vertices_scaled[face], axis=0)
            normal = centroid / np.linalg.norm(centroid)
            face_vectors.append(normal)
        return np.array(face_vectors)

    def mk_coords(
        num, vertices_scaled, face_vectors, vertices_to_faces, ns, dff, vscale
    ):
        coords = []
        for i in range(len(vertices_scaled)):
            vec1 = face_vectors[vertices_to_faces[i][0]] * dff
            vec2 = face_vectors[vertices_to_faces[i][1]] * dff
            vec3 = face_vectors[vertices_to_faces[i][2]] * dff
            basepoint = vertices_scaled[i]
            for j in range(ns + 1):
                for k in range(ns + 1):
                    for l in range(ns + 1):
                        if j + k + l <= ns:
                            coord = basepoint + j * vec1 + k * vec2 + l * vec3
                            coords.append(coord)
            basepoint = vertices_scaled[i] * vscale
            for j in range(ns):
                for k in range(ns):
                    for l in range(ns):
                        if j + k + l < ns:
                            coord = basepoint + j * vec1 + k * vec2 + l * vec3
                            coords.append(coord)
        return np.array(coords)

    # Function to compute Euclidean distance
    def compute_distance(coord1, coord2):
        return np.sqrt(np.sum((coord1 - coord2) ** 2))

    vertices = compute_vertices()
    faces = compute_faces()
    vertices_to_faces = compute_vertices_to_faces(vertices, faces)

    # separation = 0.27 # atom-atom in nm
    scale_factor = separation / np.linalg.norm(
        vertices[0] - vertices[8]
    )  # 0.27/1.236=0.218
    vertices_scaled = compute_scaled_vertices(vertices, scale_factor)

    face_vectors = compute_face_vectors(faces, vertices_scaled)

    # size of icosahedron #
    # ns = 2

    num = (ns + 1) * (ns + 2) * (2 * ns + 3) // 6 * 20
    vscale = (2.7 + 3.78) / 3.78
    dff = separation * 2 * np.sin(109.5 / 2 / 180 * np.pi)

    coords = mk_coords(
        num, vertices_scaled, face_vectors, vertices_to_faces, ns, dff, vscale
    )
    g = _create_graph(coords)
    return g


def great_decahedron(nk=2, separation=0.27):
    """
    The function `great_decahedron` generates a graph representing a great decahedron structure based on
    given parameters.

    Args:
      nk: The parameter `nk` represents the number of layers of pentagons in the great decahedron
    structure. It determines the size and complexity of the structure. The default value is 2, which
    means there are 2 layers of pentagons. Defaults to 2
      separation: The "separation" parameter represents the distance between atoms in nanometers. It is
    used to calculate the distances between the vertices and edges of the great decahedron structure.

    Returns:
      The function `great_decahedron` returns a graph object `g`.
    """

    # pentagon vertices (5 in total)
    def compute_vertices():
        return np.array(
            [
                [0.8507, 0, 0],  # 0
                [0.2629, 0.8090, 0],  # 1
                [-0.6882, 0.5, 0],  # 2
                [-0.6882, -0.5, 0],  # 3
                [0.2629, -0.8090, 0],  # 4
            ]
        )

    def compute_edges():
        return np.array(
            [
                [1.144, 0.831, 0],  # 0
                [-0.437, 1.345, 0],  # 1
                [-1.414, 0, 0],  # 2
                [-0.437, -1.345, 0],  # 3
                [1.144, -0.831, 0],  # 4
            ]
        )

    def compute_vbt():
        return np.array(
            [
                [4, 0],
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
            ]
        )

    # nk=1
    ns = int(2 * nk + 1)
    num = (ns) * (ns + 1) * (2 * ns + 1) // 6 * 5
    # separation = 0.27 # atom-atom in nm
    dff = separation * 1.633  # pentagon-pentagon

    vertices = compute_vertices()
    edges = compute_edges()
    vbt = compute_vbt()
    edges = edges * separation
    vpent = vertices * separation  # vertices of pentagon

    vervec = np.array([0, 0, dff / 2])

    coords = []
    for i in range(len(vertices)):
        vec1 = edges[vbt[i][0]]
        vec2 = edges[vbt[i][1]]
        vec3 = vervec
        basepoint = vpent[i]
        for j in range(ns + 1):
            for k in range(ns + 1):
                for l in range(int(-2 * nk), ns):
                    if (j + k + np.abs(l)) <= ns and ((j + k + np.abs(l)) % 2 == 0):
                        coord = basepoint + j * vec1 + k * vec2 + l * vec3
                        coords.append(coord)
        basepoint = vpent[i] * 1.6789
        for j in range(ns):
            for k in range(ns):
                for l in range(int(-2 * nk + 1), int(2 * nk)):
                    if (j + k + np.abs(l)) < ns and ((j + k + np.abs(l)) % 2 == 1):
                        coord = basepoint + j * vec1 + k * vec2 + l * vec3
                        coords.append(coord)

    g = _create_graph(coords)
    return g


def small_barrelan():
    """
    a unit of hexagonal ice I with 8 molecules

    * Figure 7a, Stillinger, F. H. Water revisited. Science 209, 451–457 (1980).
    """
    return nx.Graph(
        [
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 4],
            [2, 5],
            [3, 6],
            [4, 7],
            [5, 7],
            [6, 7],
        ]
    )  # small barrelan


def twistane():
    """
    a small chiral unit made of 6-cycles.

    * Sadoc, J.-F. & Mosseri, R. Geometrical Frustration. (1999).
    * http://dx.doi.org/10.1039/c3ob42152j
    """
    return nx.Graph(
        [
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 4],
            [2, 5],
            [3, 6],
            [4, 7],
            [5, 7],
            [6, 7],
            [1, 8],
            [8, 9],
            [9, 5],
        ]
    )  # twistane


def adamantane():
    """
    a unit of cubic ice I with 10 molecules.

    * Figure 7b, Stillinger, F. H. Water revisited. Science 209, 451–457 (1980).
    """
    return nx.Graph(
        [
            [0, 1],
            [0, 2],
            [0, 3],
            [1, 4],
            [2, 5],
            [3, 6],
            [4, 7],
            [7, 5],
            [5, 8],
            [8, 6],
            [6, 9],
            [9, 4],
        ]
    )


def large_barrelan():
    """
    Large barrelan.

    * Figure 7c, Stillinger, F. H. Water revisited. Science 209, 451–457 (1980)
    *
    """
    return nx.Graph(
        [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 0],
            [0, 5],
            [1, 6],
            [2, 7],
            [3, 8],
            [4, 9],
            [5, 10],
            [6, 11],
            [7, 12],
            [8, 13],
            [9, 14],
            [10, 11],
            [11, 12],
            [12, 13],
            [13, 14],
            [14, 10],
        ]
    )  # Large barrelan


def hex_ice():
    """The larger fragment of the hexagonal ice. The smaller one is the small barrelan."""
    return nx.Graph(
        [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 0],
            [0, 6],
            [2, 8],
            [4, 10],
            [6, 7],
            [7, 8],
            [8, 9],
            [9, 10],
            [10, 11],
            [11, 6],
        ]
    )


# g = nx.cycle_graph(6) # hexagon
# g = nx.cubical_graph() # cubic octamer
