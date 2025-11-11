import numpy as np

def compute_maze_structure_metrics(grid: np.ndarray) -> dict:
    #calculate % of deadends, straights, turns, junctions, and crossroads

    X_MAX, Y_MAX = grid.shape
    walls = [(x, y) for x in range(X_MAX) for y in range(Y_MAX) if grid[x, y] == 1]
    free_cells = [(x, y) for x in range(X_MAX) for y in range(Y_MAX) if grid[x, y] == 0]
    
    wallsProportion = len(walls)/(X_MAX*Y_MAX)
    pathPropotion = len(free_cells)/(X_MAX*Y_MAX)

    dead_ends = straights = turns = junctions = crossroads = 0

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    for (x, y) in free_cells:
        neighbours = [
            (x + dx, y + dy)
            for dx, dy in directions
            if 0 <= x + dx < X_MAX and 0 <= y + dy < Y_MAX and grid[x + dx, y + dy] == 0
        ]
        count = len(neighbours)

        if count == 1:
            dead_ends += 1
        elif count == 2:
            vecs = [(nx - x, ny - y) for nx, ny in neighbours]
            if ((-1, 0) in vecs and (1, 0) in vecs) or ((0, -1) in vecs and (0, 1) in vecs):
                straights += 1
            else:
                turns += 1
        elif count == 3:
            junctions += 1
        elif count == 4:
            crossroads += 1

    total = len(free_cells)
    if total == 0:
        toReturn = {k: 0 for k in ["Dead-Ends%", "Straights%", "Turns%", "Junctions%", "Crossroads%"]}
        toReturn["Path%"] = 100 * pathPropotion
        toReturn["Wall%"] = 100 * wallsProportion
        return toReturn

    return {
        "Dead-Ends%": 100 * dead_ends / total,
        "Straights%": 100 * straights / total,
        "Turns%": 100 * turns / total,
        "Junctions%": 100 * junctions / total,
        "Crossroads%": 100 * crossroads / total,
        "Path%": 100 * pathPropotion,
        "Wall%": 100 * wallsProportion
    }


def print_maze_structure_metrics(grid: np.ndarray):
    print("=== METRICS ===")
    metrics = compute_maze_structure_metrics(grid)
    for k, v in metrics.items():
        print(f"{k}: {v:.2f}%")
