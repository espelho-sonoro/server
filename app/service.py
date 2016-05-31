import flask
import flask_socketio as socket
import math

app = flask.Flask(__name__)
socketio = socket.SocketIO(app)

@app.route('/')
def root():
    return flask.render_template('index.html')

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

@socketio.on('new-message', namespace='/chat')
def new_message(message):
    socket.emit('new-message', message, broadcast=True)

def anounce_position(position):
    socket.emit('position', position, broadcast=True, namespace='/video')

