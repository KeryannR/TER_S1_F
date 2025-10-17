import sys
import modifiedTetris as mazeGen
import numpy as np

_, *param = sys.argv
print(param)

xSize = 15
ySize = 15
seed = None
nStep = 20000
maxBorderSpikeSize = 2
includeTile = "inCell\\"
show = False
help = False

paramList = [
    "--xsize",
    "--ysize",
    "--seed",
    "--nstep",
    "--maxborderspkikesize",
    "--includetile",
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
        case "--help":
            help = True if val.lower() == "true" else False
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

grid = mazeGen.placeInGrid(tileList, int.__ceil__(xSize//2)+1, int.__ceil__(ySize//2)+1, seed=seed, nStep=nStep)
grid = mazeGen.extendGrid(grid)
grid = mazeGen.removeBorderSpike(grid, maxLength=2)

print(mazeGen.exportToJSON(grid))

if show:
    mazeGen.showGrid(grid)