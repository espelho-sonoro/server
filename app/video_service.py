from app import app
from flask import jsonify, request
import math

position = {'x': 0, 'y': math.pi / 2}

@app.route('/api/video/position', methods=['POST'])
def rotate():
    content = request.get_json()
    position['x'] += content['x']
    position['y'] += content['y']
    return jsonify(position)

@app.route('/api/video/position', methods=['GET'])
def retrieve_position():
    return jsonify(position)

@app.route('/api/video/position', methods=['PUT'])
def force_position():
    content = request.get_json()
    position['x'] = content['x']
    position['y'] = content['y']
    return jsonify(position)
