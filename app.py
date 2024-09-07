from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Datos iniciales
initial_positions = {}
tractor_paths = {}
prepare_land_paths = {}
tractorLand_paths = {}

@app.route('/initial_positions', methods=['GET'])
def get_initial_positions():
    return jsonify(initial_positions)

@app.route('/tractor_paths', methods=['GET'])
def get_tractor_paths():
    return jsonify(tractor_paths)

@app.route('/tractorLand_paths', methods=['GET'])
def get_prepare_land_paths():
    """Endpoint para obtener los paths de preparación de la tierra de los tractores."""
    return jsonify(prepare_land_paths)

@app.route('/tractor_paths', methods=['POST'])
def update_tractor_paths():
    global tractor_paths
    tractor_paths = request.json
    with open('tractor_paths.json', 'w') as f:
        json.dump(tractor_paths, f, indent=4)
    return jsonify({"message": "Tractor paths updated successfully"}), 200

@app.route('/initial_positions', methods=['POST'])
def update_initial_positions():
    global initial_positions
    initial_positions = request.json
    with open('initial_positions.json', 'w') as f:
        json.dump(initial_positions, f, indent=4)
    return jsonify({"message": "Initial positions updated successfully"}), 200

@app.route('/tractorLand_paths', methods=['POST'])
def update_tractorLand_paths():
    global tractorLand_paths
    tractorLand_paths = request.json
    with open('tractorLand_paths.json', 'w') as f:
        json.dump(tractorLand_paths, f, indent=4)
    return jsonify({"message": "Tractor land paths updated successfully"}), 200

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5001)