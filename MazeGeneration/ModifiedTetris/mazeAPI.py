from flask import Flask, request, jsonify, abort
import modifiedTetris as mazeGen
import mazeDB as db
import numpy as np
import os
import json

app = Flask(__name__)

# error global handler
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

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
    includeTile = request.args.getlist("includeTile") #includeTile=...&includeTile=...&includeTile=...
    show = request.args.get("show", "false").lower() == "true"

    #chargement tile
    inCell_dir = os.path.join(os.path.dirname(__file__), "inCell")
    if not includeTile:
        tileList = mazeGen.importTiles(inCell_dir)
    else:
        tileList = []
        for tile in includeTile:
            tile_name = os.path.basename(tile)
            tile_path = os.path.join(inCell_dir, f"{tile_name}.tile")
            if not os.path.exists(tile_path):
                raise FileNotFoundError(f"Tile file not found: {tile_path}")
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

    #result = mazeGen.exportToJSON(grid)
    result = mazeGen.exportToJSON(grid)
    if isinstance(result, str):
        result = json.loads(result)

    # ajout de l'id + options dans le JSON final
    result["options"] = {
        "seed": seed,
        "xSize": xSize,
        "ySize": ySize,
        "nStep": nStep,
        "maxBorderSpikeSize": maxBorderSpikeSize,
        "includeTile": includeTile,
        "show": show
    }

    if show:
        mazeGen.showGrid(grid)

    inserted_id = db.insert_maze(result)
    result["_id"] = str(inserted_id)

    return jsonify(result)

@app.route('/get', methods=['GET'])
def get_maze():
    # recup param dans l’URL
    maze_id = request.args.get("id")    

    if not maze_id:
        abort(400, description="ID missing in request")

    # recup doc dans MongoDB
    result = db.get_maze_by_id(maze_id)

    if not result:
        abort(404, description="No maze match this ID")

    result["_id"] = str(result["_id"])

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)