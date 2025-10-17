import sys
import modifiedTetris as mazeGen

_, *param = sys.argv
print(param)

paramDict = {
    "--xsize": 15,
    "--ysize": 15,
    "--seed": None,
    "--nstep": 20000,
    "--maxborderspikesize": 2,
    "--includespecialtile": None,
    "--excludeall": False,
    "--xsymmetric": True,
    "--ysymmetric": True,
    "--help": False,
    "--show": False,
}

if len(param) % 2 != 0:
    raise IndexError("Parameter not mod 2.")

for i in range(0, len(param), 2):
    index = param[i].lower()
    val = param[i+1]
    
    if index not in paramDict.keys():
        raise ValueError(f"Parmeter not recognised:{index}")
    
    if index in ["--xsize", "--ysize", "--seed", "--nstep", "--maxborderspikesize"]:
        paramDict[index] = int(val)
    elif index == "--includespecialtile":
        paramDict[index] = val.split()
    elif index in ["--help", "--show", "--excludeall", "--xsymmetric", "--ysymmetric"]:
        paramDict[index] = True if val.lower() == "true" else False

if paramDict["--help"]:
    print("No help available for now ;)")
    exit(0)

if not paramDict["--excludeall"]:
    tileList = mazeGen.importTiles("inCell\\")
else:
    tileList = []
if paramDict["--includespecialtile"] is not None:
    for tile in paramDict["--includespecialtile"]:
        tileList.append(mazeGen.readTiles(f"inCell\\{tile}.tile"))


if paramDict["--xsymmetric"] and paramDict["--ysymmetric"]:
    grid = mazeGen.placeInGrid(tileList, int.__ceil__(paramDict["--xsize"]//2)+1, int.__ceil__(paramDict["--ysize"]//2)+1, seed=paramDict["--seed"], nStep=paramDict["--nstep"])
    grid = mazeGen.extendGrid(grid)
elif paramDict["--xsymmetric"]:
    grid = mazeGen.placeInGrid(tileList, int.__ceil__(paramDict["--xsize"]//2)+1, paramDict["--ysize"], seed=paramDict["--seed"], nStep=paramDict["--nstep"])
    grid = mazeGen.symmetric(grid)
elif paramDict["--ysymmetric"]:
    grid = mazeGen.placeInGrid(tileList, paramDict["--xsize"], int.__ceil__(paramDict["--ysize"]//2)+1, seed=paramDict["--seed"], nStep=paramDict["--nstep"])
    grid = mazeGen.symmetric(grid, axis=1)
else: 
    grid = mazeGen.placeInGrid(tileList, paramDict["--xsize"], paramDict["--ysize"], seed=paramDict["--seed"], nStep=paramDict["--nstep"])

grid = mazeGen.removeBorderSpike(grid, maxLength=2)
grid = mazeGen.remove8connexity(grid, paramDict["--seed"])

print(mazeGen.exportToJSON(grid))

if paramDict["--show"]:
    mazeGen.showGrid(grid)