from ghost import *
import numpy as np
import networkx as nx

from graphBasedModifiedTetris import grid2Graph, compress_maze_graph, showGraph, importFromJSON

class GhostAgent(Ghost):
    graph:nx.Graph = None
    
    def __init__(self, grid, cell_size, ghost_index=0):
        super().__init__(grid, cell_size, ghost_index)
    
    @classmethod
    def setGraph(cls, graph:nx.Graph) -> None:
        cls.graph = graph.copy()
    
    @classmethod
    def setVisit(cls, x:int, y:int) -> bool:
        """Update the visit status of a node if it is within the graph.

        Args:
            x (int): x-coordinate
            y (int): y-coordinate

        Returns:
            bool: True if the node was in the graph; False otherwise
        """
        if ((x,y) in graph.nodes):
            cls.graph.nodes[(x,y)]["isVisited"] = True
            return True
        return False
    
    def move(self) -> None:
        super().move()
        ...
    

if __name__ == "__main__":
    grid = importFromJSON("test_maze3.json")
    graph = compress_maze_graph(grid2Graph(grid))
    ghost = GhostAgent(grid, 1, 0)
    ghost.setGraph(graph)
    
    showGraph(ghost.graph)
    ghost.setVisit(4,1)
    showGraph(ghost.graph)
    
    print(graph.nodes)