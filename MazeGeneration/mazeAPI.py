from flask import Flask, request, jsonify
import modifiedTetris as mazeGen
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Maze Generator API is running!"})

@app.route('/generate', methods=['GET'])
def generate_maze():
    # recup param dans l’URL
    xSize = int(request.args.get("xSize", 15))
    ySize = int(request.args.get("ySize", 15))
    seed = request.args.get("seed", None)
    seed = int(seed) if seed is not None else None
    nStep = int(request.args.get("nStep", 20000))
    maxBorderSpikeSize = int(request.args.get("maxBorderSpikeSize", 2))
    includeTile = request.args.getlist("includeTile") or ["inCell\\"]
    show = request.args.get("show", "false").lower() == "true"

    #chargement tile
    inCell_dir = os.path.join(os.path.dirname(__file__), "inCell")
    if includeTile == ["inCell\\"]:
        tileList = mazeGen.importTiles(inCell_dir)
    else:
        tileList = []
        for tile in includeTile:
            tile_path = os.path.join(inCell_dir, f"{tile}.tile")
            tileList.append(mazeGen.readTiles(tile_path))

    # genere maze
    grid = mazeGen.placeInGrid(
        tileList,
        int(np.ceil(xSize // 2)) + 1,
        int(np.ceil(ySize // 2)) + 1,
        seed=seed,
        nStep=nStep
    )

    grid = mazeGen.extendGrid(grid)
    grid = mazeGen.removeBorderSpike(grid, maxLength=maxBorderSpikeSize)

    result = mazeGen.exportToJSON(grid)

    if show:
        mazeGen.showGrid(grid)

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)