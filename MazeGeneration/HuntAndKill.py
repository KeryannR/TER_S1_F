import numpy as np
from Grid import Grid

class HuntAndKill():
    def __init__(self, seed:int=None):
        self.rng = np.random.RandomState(seed)

    def on(self, grid:Grid):
        # Choose a random cell
        current = grid.randomCell()
        
        # While there is remaining nodes
        while current:
            # Find the neighbours of the current point (neighbours are not necesserally connected)
            unvisitedNeighbour = [n for n in current.neighbours() if not n.links]
            
            # If there is unvisited neighbour
            if unvisitedNeighbour:
                # Choose a random neighbour and link it 
                neighbour = self.rng.choice(unvisitedNeighbour)
                current.link(neighbour)
                
                # Pass on the next neighbour
                current = neighbour
            
            # If all the neighbour are connected 
            else:
                current = None
                
                # For all cells on the grid
                for cell in grid.eachCell():
                    
                    # Retrieve connected neigbour
                    visitedNeighbour = [n for n in cell.neighbours() if n.links]
                    
                    # If the ceel has no links, but has visited neighbour
                    if not cell.links and visitedNeighbour:
                        # Update the current cell
                        current = cell
                        
                        # Choose a cell among the visited neighbour and link it to the current one 
                        neighbour = self.rng.choice(visitedNeighbour)
                        current.link(neighbour)
                        break
        return grid

if __name__ == "__main__":
    hak = HuntAndKill()
    g = Grid(10,10)
    g2 = hak.on(g)
    
    g2.braid(0.5)
    print(g2)