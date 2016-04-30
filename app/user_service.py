from app import socketio
from flask_socketio import emit

sessions = {}
messages = []

@socketio.on('new-message', namespace='/chat')
def new_message(message):
    emit('new-message', message, broadcast=True)
