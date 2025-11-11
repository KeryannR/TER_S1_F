import numpy as np
import matplotlib.pyplot as plt
import os

import referenceMaze.ScoreMaze as score

import json

def readTiles(path:str) -> np.ndarray[int]:
    # Open and parse the tile format
    with open(path, "r") as file:
        tile = []
        while (row := file.readline()) != "":
            tile.append([int(i) for i in row.strip().split(" ")])
        return np.array(tile)

def importTiles(rootPath: str = None, excludeSpecial: bool = True) -> list[np.ndarray[int]]:
    # Retrieve and parse all the tiles in a folder
    if rootPath is None:
        rootPath = os.path.join(os.path.dirname(__file__), "inCell")
    tileList = []
    for inputFile in os.listdir(rootPath):
        if excludeSpecial and inputFile.startswith("special_"):
            continue
        tile_path = os.path.join(rootPath, inputFile)
        tileList.append(readTiles(tile_path))
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

def placeInGrid(tileList:list[np.ndarray], X_MAX:int = 15, Y_MAX:int = 15, seed:int = 0, nStep = 20000, pReplace:float = 0) -> np.ndarray[int]:
    # Initialise a random number generator and create the grid
    rng = np.random.RandomState(seed)
    if seed is not None:
        pReplaceRNG = np.random.RandomState(seed+1)
    else:
        pReplaceRNG = np.random.RandomState(seed)
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
        
        # Add tile if no other tiles at the border or if force place is active
        if np.sum(subgrid*frame) == 0 or pReplaceRNG.rand()<pReplace:
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
    for row in range(1, grid.shape[0]-1):
        if np.sum(grid[row, :maxLength+1] * spikeMask) == maxLength + 1 and grid[row-1, 0] != 1 and grid[row+1, 0] != 1:
            grid[row, 0] = 0
        if np.sum(grid[row, -maxLength-1:] * spikeMask) == maxLength + 1 and grid[row-1, -1] != 1 and grid[row+1, -1] != 1:
            grid[row, -1] = 0
    
    for col in range(1, grid.shape[1]-1):
        if np.sum(grid[:maxLength+1, col] * spikeMask) == maxLength + 1 and grid[0, col-1] != 1 and grid[0, col+1] != 1:
            grid[0, col] = 0
        if np.sum(grid[-maxLength-1:, col] * spikeMask) == maxLength + 1 and grid[-1, col-1] != 1 and grid[-1, col+1] != 1:
            grid[-1, col] = 0
    
    return grid

def remove8connexity(grid: np.ndarray, seed: int = None) -> np.ndarray:
    """
    Remove walls (set 1 -> 0) so that remaining walls are only 4-connected.
    Repeats passes until no diagonal-only adjacencies remain.

    Parameters
    ----------
    grid : np.ndarray
        2D integer array with 1 = wall, 0 = path.
    seed : int | None
        Seed for RNG to make removals reproducible.

    Returns
    -------
    np.ndarray
        New grid with diagonal-only wall adjacencies removed.
    """
    grid = grid.copy()
    rng = np.random.RandomState(seed)
    XMAX, YMAX = grid.shape

    changed = True
    while changed:
        changed = False
        # Optionally, randomize scanning order to avoid systematic bias:
        # create a list of all top-left coordinates for 2x2 windows and shuffle it.
        coords = [(row, col) for row in range(XMAX - 1) for col in range(YMAX - 1)]
        rng.shuffle(coords)

        for row, col in coords:
            # read the 2x2 block
            topLeft = grid[row, col]       
            topRight = grid[row, col+1]    
            bottomLeft = grid[row+1, col]  
            bottomRight = grid[row+1, col+1]

            # top-left & bottom-right diagonal-only
            if topLeft == 1 and bottomRight == 1 and topRight == 0 and bottomLeft == 0:
                # choose one to remove (randomly)
                if rng.rand() < 0.5:
                    grid[row, col] = 0    # remove top-left
                else:
                    grid[row+1, col+1] = 0  # remove bottom-right
                changed = True

            # top-right & bottom-left diagonal-only
            elif topRight == 1 and bottomLeft == 1 and topLeft == 0 and bottomRight == 0:
                if rng.rand() < 0.5:
                    grid[row, col+1] = 0  # remove top-right
                else:
                    grid[row+1, col] = 0  # remove bottom-left
                changed = True

        # loop repeats if any changes were made
    return grid




def placePhantomBase(grid:np.ndarray[int]) -> np.ndarray[int]:
    grid = grid.copy()
    phantomBase = np.array([
        [0,0,0,0,0,0,0],
        [0,1,1,2,1,1,0],
        [0,1,2,2,2,1,0],
        [0,1,1,1,1,1,0],
        [0,0,0,0,0,0,0]
    ])
    
    x, y = grid.shape[0]//2, grid.shape[1]//2
    dx, dy = phantomBase.shape[0]//2, phantomBase.shape[1]//2
    
    grid[x-dx:x+dx+1, y-dy:y+dy+1] = phantomBase
    return grid

def placePortal(grid:np.ndarray[int], quantity:int, voidBeforePortal:int = 2) -> np.ndarray[int]:
    grid = grid.copy()
    XMAX = grid.shape[0]
    YMAX = grid.shape[1]
    if quantity == 0:
        return grid
    for i in range(1, quantity+1):
        if i == 1:
            grid[max(XMAX//2-1,0), (0,1,YMAX-1,YMAX-2)] = 1
            grid[min(XMAX//2+1, XMAX-1), (0,1,YMAX-1, YMAX-2)] = 1
            grid[XMAX//2, 1:voidBeforePortal+1] = 0
            grid[XMAX//2, YMAX-voidBeforePortal-1:YMAX-1] = 0
            grid[XMAX//2, (0, YMAX-1)] = 3
        elif i%2 == 0:
            grid[max(XMAX//(2*i)-1,0), (0,1,YMAX-1,YMAX-2)] = 1
            grid[min(XMAX//(2*i)+1, XMAX-1), (0,1,YMAX-1, YMAX-2)] = 1
            grid[XMAX//(2*i), 1:voidBeforePortal+1] = 0
            grid[XMAX//(2*i), YMAX-voidBeforePortal-1:YMAX-1] = 0
            grid[XMAX//(2*i), (0, YMAX-1)] = 3
        elif i%2 == 1:
            grid[max(XMAX - XMAX//(2*i-1)-1,0), (0,1,YMAX-1,YMAX-2)] = 1
            grid[min(XMAX - XMAX//(2*i-1)+1, XMAX-1), (0,1,YMAX-1, YMAX-2)] = 1
            grid[XMAX-XMAX//(2*i-1), 1:voidBeforePortal+1] = 0
            grid[XMAX-XMAX//(2*i-1), YMAX-voidBeforePortal-1:YMAX-1] = 0
            grid[XMAX - XMAX//(2*(i-1)), (0, YMAX-1)] = 3
    
    return grid

def showGrid(grid:np.ndarray) -> None:
    plt.matshow(grid, cmap="grey")
    plt.show()

def exportToJSON(grid:np.ndarray[int], outPath:str = None) -> str|None:
    
    jsonVal = {
                "width": grid.shape[1],
                "height": grid.shape[0],
                "grid": grid.tolist(),
                "score": score.getScore(grid),
                "adjustedScore": score.getAdjustedScore(grid),
                "metrics": score.met.compute_maze_structure_metrics(grid),
                "legend": {
                    "0": "path",
                    "1": "wall",
                    "2": "phantom",
                    "3": "portal"
                }
    }
    
    if outPath is None:
        return json.dumps(jsonVal)
    
    
    with open(outPath, "w") as file:
        json.dump(
            jsonVal,      
            file
        )

if __name__ == "__main__":
    X_MAX = Y_MAX = 15
    tileList = importTiles("inCell\\")
    seed = 6
    grid = placeInGrid(tileList, X_MAX, Y_MAX, seed=seed, nStep=20000, pReplace=0)
    grid = extendGrid(grid)
    
    #grid = np.ones((31,31), dtype=int)
    #grid = np.zeros((31,31), dtype=int)
    
    #print(score.getScore(grid))
    #score.met.print_maze_structure_metrics(grid)
    #showGrid(grid)
    
    grid = placePhantomBase(grid)
    grid = removeBorderSpike(grid, maxLength=2)
    grid = remove8connexity(grid, seed=seed)
    grid = placePortal(grid, 1, voidBeforePortal=3)
    
    print(score.getScore(grid))
    #score.met.print_maze_structure_metrics(grid)
    showGrid(grid)
    
    exportToJSON(grid, "test.json")

