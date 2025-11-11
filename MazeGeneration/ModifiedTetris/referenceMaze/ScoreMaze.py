import metrics.MazeMetrics_Tetris as met
#import modifiedTetris as mazeGen
import numpy as np
import json
import os

from scipy.spatial.distance import euclidean

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
metric_ref_file = os.path.join(base_dir, "referenceMaze", "metricReference.json")

if not os.path.exists(metric_ref_file):
    refGrid = {"deadEnd":{"avg":0}, "straight":{"avg":0}, "turn":{"avg":0}, "junction":{"avg":0}, "crossroad":{"avg":0}, "pathProportion":{"avg":0}, "wallProportion":{"avg":0}}

    count = 0
    pacman_files = ["pacman1.json", "pacman2.json", "pacman3.json"]
    for key in pacman_files:
        with open(os.path.join(base_dir, "referenceMaze", key)) as file:
            refGrid["deadEnd"][key], refGrid["straight"][key], refGrid["turn"][key], refGrid["junction"][key], refGrid["crossroad"][key], refGrid["pathProportion"][key], refGrid["wallProportion"][key] = met.compute_maze_structure_metrics(np.array(json.load(file)["grid"])).values()
        
        for metric in refGrid.keys():
            if metric != "pacmanGrid":
                refGrid[metric]["avg"] = (count*refGrid[metric]["avg"]+refGrid[metric][key])/(count+1)
        count +=1
    with open(metric_ref_file, "w") as file:
        json.dump(refGrid, file)

else:
    with open(metric_ref_file) as file:
        refGrid = json.load(file)


def getScore(grid:np.ndarray, weights:np.ndarray[float] = np.array([1, 1, 1, 1, 1, 1, 1])) -> float:
    metricDict = met.compute_maze_structure_metrics(grid)
    gridToTestMetrics = np.array([
        metricDict["Dead-Ends%"],
        metricDict["Straights%"],
        metricDict["Turns%"],
        metricDict["Junctions%"],
        metricDict["Crossroads%"],
        metricDict["Path%"],
        metricDict["Wall%"]
    ])
    gridReferenceMetrics = np.array([
        refGrid["deadEnd"]["avg"],
        refGrid["straight"]["avg"],
        refGrid["turn"]["avg"],
        refGrid["junction"]["avg"],
        refGrid["crossroad"]["avg"],
        refGrid["pathProportion"]["avg"],
        refGrid["wallProportion"]["avg"]
    ])
    
    # Normalise between 0 and 1 and minor weight
    gridToTestMetrics /= 100
    gridReferenceMetrics /= 100
    weights = np.sqrt(weights)
    
    # If wall proportion is too much
    if gridToTestMetrics[-1] > 0.8:
        return 0
    
    # If path proportion is too much
    if gridToTestMetrics[-2] > 0.8:
        return 0
    
    # If crossroad proportion is too much
    if gridToTestMetrics[-3] > 0.15:
        return 0
    
    score = np.dot(weights*gridToTestMetrics, weights*gridReferenceMetrics)/(np.linalg.norm(weights*gridReferenceMetrics)*np.linalg.norm(weights*gridToTestMetrics))
    # Compute weighted euclidean similarity (1-euclidian)
    #score = 1-np.sqrt(np.sum(weights*(gridToTestMetrics-gridReferenceMetrics)**2))/np.sqrt(np.sum(weights))
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