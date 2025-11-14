import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json


def grid2Graph(grid:np.ndarray[int]) -> nx.Graph:
    """
    Convert a numpy encoded maze into NetworkX graph.
    
    - 0 = path
    - 1 or 2 = walls
    - 3 = teleporter: connects to opposite side of the same row
    """
    
    # Initialise the graph
    rows, cols = grid.shape
    G = nx.Graph()
    
    # If the cell at row and column is path, then get  it     
    def addIfWalkable(row, col):
        if 0 <= row < rows and 0 <= col < cols and grid[row, col] in (0, 3):
            return (row, col)
        return None

    # Add nodes
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] in (0, 3):
                G.add_node((row, col), isVisited = False)
                try:
                    if grid[row+1, col] == 2:
                        G.nodes[(row, col)]["toKeep"] = True
                    else:
                        G.nodes[(row, col)]["toKeep"] = False
                except:
                    G.nodes[(row, col)]["toKeep"] = False

    # Add normal adjacency edges (up, down, left, right)
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] not in (0, 3):
                continue
            for dr, dc in directions:
                neigh = addIfWalkable(row + dr, col + dc)
                if neigh:
                    G.add_edge((row, col), neigh)

    # Add teleporter edges (connect to opposite side)
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 3:
                opposite_col = cols - 1 - col
                if grid[row, opposite_col] in (0, 3):
                    G.add_edge((row, col), (row, opposite_col))
    
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
    
    # Check if a given node make a turn
    def isTurn(node):
        (startRow, startCol) = node
        neighbors = list(G.neighbors(node))
        if len(neighbors) != 2:
            return False

        (endRow1, endCol1), (endRow2, endCol2) = neighbors
        # direction vectors
        v1 = (endRow1 - startRow, endCol1 - startCol)
        v2 = (endRow2 - startRow, endCol2 - startCol)

        # straight if same row or same column (i.e., collinear)
        return not (v1[0] == v2[0] or v1[1] == v2[1])

    # Step 1 — build the compressed graph
    CG = nx.Graph()

    # Step 2 — identify important nodes
    important = set()
    for n in G.nodes:
        deg = G.degree[n]
        if G.nodes[n]["toKeep"]:
            important.add(n)
            CG.add_node(n, isVisited = True)
        elif deg != 2:
            important.add(n)
            CG.add_node(n, isVisited = False)
        elif isTurn(n):
            important.add(n)
            CG.add_node(n, isVisited = False)

    # Step 3 — explore corridors
    visited_edges = set()

    for start in important:
        for nextNode in G.neighbors(start):
            edgeKey = tuple(sorted([start, nextNode]))
            if edgeKey in visited_edges:
                continue

            path = [start, nextNode]
            visited_edges.add(edgeKey)

            current = nextNode
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

def importFromJSON(path:str) -> np.ndarray[int]:
    with open(path, "r") as file:
        dic = json.load(file)
    grid = np.array(dic["grid"], dtype=int)
    grid = np.reshape(grid, (dic["height"], dic["width"]))
    return grid

def showGraph(G:nx.Graph, showVisit:bool = True, showWeight:bool = False) -> None:
    pos = nx.spring_layout(G)
    if not showVisit:
        nx.draw(G, pos, with_labels = True, node_color = "lightblue", font_weight = "bold")
    else:
        nx.draw(G, pos, with_labels = True, node_color = [0 if G.nodes[i]["isVisited"] else 255 for i in G.nodes], font_weight = "bold", cmap=plt.cm.seismic)
    
    if showWeight:
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
    plt.show()

if __name__ == "__main__":
    grid = importFromJSON("test_maze3.json")
    graph = compress_maze_graph(grid2Graph(grid))
    showGraph(graph, showWeight=True)
    print(graph.nodes[(4,6)])