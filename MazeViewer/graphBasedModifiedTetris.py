import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def grid2Graph(grid:np.ndarray[int]) -> nx.Graph:
    """
    Convert a maze array into a NetworkX graph.
    
    - 0 = path
    - 1 or 2 = walls
    - 3 = teleporter: connects to opposite side of the same row
    """
    rows, cols = grid.shape
    G = nx.Graph()

    def add_if_walkable(r, c):
        """Return (r,c) if inside grid and walkable, else None."""
        if 0 <= r < rows and 0 <= c < cols and grid[r, c] in (0, 3):
            return (r, c)
        return None

    # Add nodes
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in (0, 3):
                G.add_node((r, c))

    # Add normal adjacency edges (up, down, left, right)
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] not in (0, 3):
                continue
            for dr, dc in directions:
                neigh = add_if_walkable(r + dr, c + dc)
                if neigh:
                    G.add_edge((r, c), neigh)

    # Add teleporter edges (connect to opposite side)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                opposite_c = cols - 1 - c
                if grid[r, opposite_c] in (0, 3):
                    G.add_edge((r, c), (r, opposite_c))

    return G

def compress_maze_graph(G:nx.Graph) -> nx.Graph:
    """
    Compress the maze graph by keeping only:
    - endpoints (degree != 2)
    - junctions (degree != 2)
    - turns (degree == 2 but the direction changes)
    Teleporter nodes (value 3) are preserved automatically
    because they have degree != 2 or unusual connectivity.

    Straight segments are replaced by weighted edges.
    """
    def is_turn(node):
        """Check if a degree-2 node makes a geometric turn."""
        (r1, c1) = node
        neighbors = list(G.neighbors(node))
        if len(neighbors) != 2:
            return False

        (r2, c2), (r3, c3) = neighbors
        # direction vectors
        v1 = (r2 - r1, c2 - c1)
        v2 = (r3 - r1, c3 - c1)

        # straight if same row or same column (i.e., collinear)
        return not (v1[0] == v2[0] or v1[1] == v2[1])

    # Step 1 — identify important nodes
    important = set()
    for n in G.nodes:
        deg = G.degree[n]
        if deg != 2:
            important.add(n)
        elif is_turn(n):
            important.add(n)

    # Step 2 — build the compressed graph
    CG = nx.Graph()

    for n in important:
        CG.add_node(n)

    # Step 3 — explore corridors
    visited_edges = set()

    for start in important:
        for nxt in G.neighbors(start):
            edge_key = tuple(sorted([start, nxt]))
            if edge_key in visited_edges:
                continue

            path = [start, nxt]
            visited_edges.add(edge_key)

            current = nxt
            prev = start

            # walk until next important node
            while current not in important or current == start:
                neighbors = list(G.neighbors(current))
                # remove the previous node
                neighbors.remove(prev)

                if len(neighbors) == 0:
                    break  # dead end (should not happen)
                next_node = neighbors[0]

                visited_edges.add(tuple(sorted([current, next_node])))

                path.append(next_node)
                prev, current = current, next_node

            end = current

            if start != end:
                weight = len(path) - 1
                CG.add_edge(start, end, weight=weight)

    return CG

def showGraph(G:nx.Graph) -> None:
    nx.draw(G, with_labels = True, node_color = "lightblue", font_weight = "bold")
    plt.show()