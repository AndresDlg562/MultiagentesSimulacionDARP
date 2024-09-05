from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Cargar datos iniciales
initial_positions = {}
tractor_paths = {}

@app.route('/initial_positions', methods=['GET'])
def get_initial_positions():
    """Endpoint para obtener las posiciones iniciales."""
    return jsonify(initial_positions)

@app.route('/tractor_paths', methods=['GET'])
def get_tractor_paths():
    """Endpoint para obtener los paths de los tractores."""
    return jsonify(tractor_paths)

@app.route('/tractor_paths', methods=['POST'])
def update_tractor_paths():
    """Endpoint para actualizar los paths de los tractores."""
    global tractor_paths
    tractor_paths = request.json
    with open('tractor_paths.json', 'w') as f:
        json.dump(tractor_paths, f, indent=4)
    return jsonify({"message": "Tractor paths updated successfully"}), 200

@app.route('/initial_positions', methods=['POST'])
def update_initial_positions():
    """Endpoint para actualizar las posiciones iniciales."""
    global initial_positions
    initial_positions = request.json
    with open('initial_positions.json', 'w') as f:
        json.dump(initial_positions, f, indent=4)
    return jsonify({"message": "Initial positions updated successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)