import metrics.MazeMetrics_Tetris as met
#import modifiedTetris as mazeGen
import numpy as np
import json
import os

#from modifiedTetris import showGrid
if not os.path.exists(os.path.join("referenceMaze", "metricReference.json")):
    refGrid = {"deadEnd":{"avg":0}, "straight":{"avg":0}, "turn":{"avg":0}, "junction":{"avg":0}, "crossroad":{"avg":0}}

    count = 0
    for key in [os.path.join("referenceMaze", "pacman1.json"), os.path.join("referenceMaze", "pacman2.json"), os.path.join("referenceMaze", "pacman3.json")]:
        with open(key) as file:
            refGrid["deadEnd"][key], refGrid["straight"][key], refGrid["turn"][key], refGrid["junction"][key], refGrid["crossroad"][key] = met.compute_maze_structure_metrics(np.array(json.load(file)["refGrid"])).values()
        
        for metric in refGrid.keys():
            if metric != "pacmanGrid":
                refGrid[metric]["avg"] = (count*refGrid[metric]["avg"]+refGrid[metric][key])/(count+1)
        count +=1
    with open(os.path.join("referenceMaze", "metricReference.json"), "w") as file:
        json.dump(refGrid, file)

else:
    with open(os.path.join("referenceMaze", "metricReference.json")) as file:
        refGrid = json.load(file)



def getScore(grid:np.ndarray) -> float:
    gridToTestMetrics = np.array(list(met.compute_maze_structure_metrics(grid).values()), dtype=float)
    gridReferenceMetrics = np.array([refGrid["deadEnd"]["avg"], refGrid["straight"]["avg"], refGrid["turn"]["avg"], refGrid["junction"]["avg"], refGrid["crossroad"]["avg"]]    )
    score = np.dot(gridToTestMetrics, gridReferenceMetrics)/(np.linalg.norm(gridReferenceMetrics)*np.linalg.norm(gridToTestMetrics))
    return score*5

def getAdjustedScore(grid:np.ndarray) -> int:
    gridScore = getScore(grid)
    if gridScore < 2:
        return 0
    if gridScore < 2.5:
        return 1
    if gridScore < 3:
        return 2
    if gridScore < 3.5:
        return 3
    if gridScore < 4:
        return 4
    return 5

if __name__ == "__main__":
    ...
    # tileList = mazeGen.importTiles("inCell\\", excludeSpecial=False)
    # count = 0
    # while True:
    #   grid = mazeGen.placeInGrid(tileList, 15, 15, None, nStep=1000)
    #   grid = mazeGen.extendGrid(grid)
    #   grid = mazeGen.removeBorderSpike(grid, maxLength=2)
    #   grid = mazeGen.remove8connexity(grid)
    #   score = getScore(grid)
    #   if not count % 10:
    #       print(f"mazeGenerated: {count}, {score=}")
    #   if score > 3.5:
    #       showGrid(grid)
    #       print(score)
    #       break
    #   count += 1