import numpy as np
import matplotlib.pyplot as plt
import os

def readTiles(path:str) -> np.ndarray[int]:
    # Open and parse the tile format
    with open(path, "r") as file:
        tile = []
        while (row := file.readline()) != "":
            tile.append([int(i) for i in row.strip().split(" ")])
        return np.array(tile)

def importTiles(rootPath:str = "inCell\\") ->list[np.ndarray[int]]:
    # Retrieve and parse all the tiles in a folder
    tileList = []
    for inputFile in os.listdir(rootPath):
        tileList.append(readTiles(rootPath+inputFile))
    return tileList

def rotateTile(tile:np.ndarray[int], k:int = 1) -> np.ndarray[int]:
    # Rotate tile k times by +90°
    return np.rot90(tile, k)

def createFrame(shape:tuple[int], addTile:np.ndarray[int] = None) -> np.ndarray[int]:
    # A frame is a special matrix containing the tile in the middle and having a 1 border elsewhere (or just a 1 border if tile not provided)
    # Create the frame
    maxx = shape[0]+2
    maxy = shape[1]+2
    frame = np.zeros((maxx,maxy), dtype = int)
    
    # Add the border
    frame[0:, (0, maxy-1)] = 1
    frame[(0, maxx-1), 0:] = 1
    
    # Add tile in the middle if provided
    if addTile is not None:
        frame[1:maxx-1, 1:maxy-1] = addTile
    
    return frame

def placeInGrid(tileList:list[np.ndarray], X_MAX:int = 15, Y_MAX:int = 15, seed:int = 0, nStep = 20000) -> np.ndarray[int]:
    # Initialise a random number generator and create the grid
    rng = np.random.RandomState(seed)
    grid = np.zeros((X_MAX,Y_MAX), dtype=int)
    
    # Add tile at random position and rotation nStep times
    for _ in range(nStep):
        x = rng.randint(X_MAX)
        y = rng.randint(Y_MAX)
        
        # Select tile and rotation of the tile
        selectedTile:np.ndarray = tileList[rng.randint(len(tileList))]
        selectedTile = rotateTile(selectedTile, k=rng.randint(0,4))
        xmax_tile, ymax_tile = selectedTile.shape
        
        # Detection of tile at the border of other tiles while checking if out of the grid. If Out the grid, then only the part inside thee grid is placed
        subgrid = grid[max(x-1,0):min(x+xmax_tile+1, X_MAX), max(y-1,0):min(y+ymax_tile+1, Y_MAX)]
        frame = createFrame((xmax_tile, ymax_tile), selectedTile)[:subgrid.shape[0], :subgrid.shape[1]]
        
        # Add tile if no other tiles at the border
        if np.sum(subgrid*frame) == 0:
            grid[x:min(x+xmax_tile, X_MAX), y:min(y+ymax_tile, Y_MAX)] = selectedTile[:min(xmax_tile, X_MAX-x), :min(ymax_tile, Y_MAX-y)]
    return grid

def symmetric(grid:np.ndarray, axis:int = 0) -> np.ndarray[int]:
    #  Concatenate the grid and the symmetry of the grid, with the right axis
    symGrid = np.concatenate((grid, np.flip(grid, axis=axis)), axis=axis)
    
    # Remove the middle row to merge th grid completely
    if axis == 0:
        symGrid[grid.shape[0]-1:-1, :] = symGrid[grid.shape[0]:, :]
        symGrid = symGrid[:-1,:]
    elif axis == 1:
        symGrid[:, grid.shape[1]-1:-1] = symGrid[:, grid.shape[1]:]
        symGrid = symGrid[:,:-1]
    return symGrid

def extendGrid(grid:np.ndarray) -> np.ndarray[int]:
    # Return double symmetry of the grid
    return symmetric(symmetric(grid), axis=1)

def removeBorderSpike(grid:np.ndarray, maxLength:int=2) -> np.ndarray[int]:
    grid = grid.copy()
    spikeMask = np.ones(maxLength+1)
    for row in range(grid.shape[0]-1):
        if np.sum(grid[row, :maxLength+1] * spikeMask) == maxLength + 1:
            grid[row, 0] = 0
        if np.sum(grid[row, -maxLength-1:] * spikeMask) == maxLength + 1:
            grid[row, -1] = 0
    
    for col in range(grid.shape[1]-1):
        if np.sum(grid[:maxLength+1, col] * spikeMask) == maxLength + 1:
            grid[0, col] = 0
        if np.sum(grid[-maxLength-1:, col] * spikeMask) == maxLength + 1:
            grid[-1, col] = 0
    
    return grid

def showGrid(grid:np.ndarray) -> None:
    plt.matshow(grid, cmap="grey")
    plt.show()

if __name__ == "__main__":
    X_MAX = Y_MAX = 15
    tileList = importTiles("inCell\\")
    grid = placeInGrid(tileList, X_MAX, Y_MAX, seed=0, nStep=20000)
    grid = extendGrid(grid)
    grid = removeBorderSpike(grid, maxLength=2)
    showGrid(grid)