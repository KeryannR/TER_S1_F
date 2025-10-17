import sys
import modifiedTetris as mazeGen
import numpy as np

_, *param = sys.argv
print(param)

xSize = 15
ySize = 15
seed = 0
nStep = 20000
maxBorderSpikeSize = 2
includeTile = "inCell\\"
excludeTile = "U_cell longU_cell Z2_cell"
show = False
help = False

paramList = [
    "--xsize",
    "--ysize",
    "--seed",
    "--nstep",
    "--maxborderspkikesize",
    "--includetile",
    "--excludetile",
    "--help",
    "--show"
]

if len(param) % 2 != 0:
    raise IndexError("Parameter not mod 2.")

for i in range(0, len(param), 2):
    index = param[i].lower()
    val = param[i+1]
    
    if index not in paramList:
        raise ValueError("Parmeter not recognised")
    
    match index:
        case "--xsize":
            xSize = int(val)
        case "--ysize":
            ySize = int(val)
        case "--seed":
            seed = int(val)
        case "--nstep":
            nStep = int(val)
        case "--maxborderspikesize":
            maxBorderSpikeSize = int(val)
        case "--includetile":
            includeTile = val.split()
        case "--excludetile":
            excludeTile = val.split() if val.lower() != "none" else None
        case "--help":
            help = True if val.lower() == "true" else False
            break
        case "--show":
            show = True if val.lower() == "true" else False
        case _:
            raise ValueError("Parmeter not recognised")

if help:
    print("No help available for now ;)")
    exit(0)

if includeTile == "inCell\\":
    tileList = mazeGen.importTiles(includeTile)
else:
    tileList = []
    for tile in includeTile:
        tileList.append(mazeGen.readTiles(f"inCell\\{tile}.tile"))

if excludeTile is not None:
    tileList = set([tuple(map(tuple, arr)) for arr in tileList])
    
    for tile in excludeTile:
        tileArr:np.ndarray = tuple(mazeGen.readTiles(f"inCell\\{tile}.tile"))
        tileList.remove(tuple(map(tuple, tileArr)))
        
    tileList = [np.array(tup) for tup in tileList]


grid = mazeGen.placeInGrid(tileList, xSize, ySize, seed=seed, nStep=nStep)
grid = mazeGen.extendGrid(grid)
grid = mazeGen.removeBorderSpike(grid, maxLength=2)

print(mazeGen.exportToJSON(grid))

if show:
    mazeGen.showGrid(grid)