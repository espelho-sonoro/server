from app import socketio
from flask import jsonify, request
from flask_socketio import emit
import math

position = {'x': 0, 'y': math.pi / 2}

@socketio.on('rotate', namespace='/video')
def rotate(content):
    position['x'] += content['x']
    position['y'] += content['y']
    anounce_position(position)

@socketio.on('position', namespace='/video')
def force_position(content):
    position['x'] = content['x']
    position['y'] = content['y']
    anounce_position(position)

def anounce_position(position):
    emit('position', position, broadcast=True, namespace='/video')
