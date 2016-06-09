import flask
import flask_socketio as socket
import flask_sqlalchemy as sql

import uuid
import math
from datetime import datetime

DEFAULT_VIDEO_ID = '1'

app = flask.Flask(__name__)
socketio = socket.SocketIO(app)
db = sql.SQLAlchemy(app)

class VideoPosition(db.Model):
    video_id = db.Column(db.String, primary_key=True)
    x_position = db.Column(db.Float)
    y_position = db.Column(db.Float)

    def __init__(self, video_id, x, y):
        self.video_id = str(video_id)
        self.x_position = float(x)
        self.y_position = float(y)

    def __json__(self):
        return {
            'x': self.x_position,
            'y': self.y_position
        }

    def __repr__(self):
        return "<app.service.VideoPosition, video_id: %s, x_position: %s, y_position: %s>" % \
            (self.video_id, self.x_position, self.y_position)

class ChatMessage(db.Model):
    uuid = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    date = db.Column(db.DateTime)
    message = db.Column(db.Text)

    def __init__(self, user_id, date, message):
        self.uuid = str(uuid.uuid4())
        self.user_id = user_id
        self.date = date
        self.message = message

    def __json__(self):
        return {
            'user': self.user_id,
            'date': self.date.isoformat(),
            'text': self.message
        }

class VideoPositionDAO(object):
    def __init__(self, db, video_class):
        self.video_class = video_class
        self.db = db

    def get(self, video_id):
        return self.video_class.query.get(video_id)

    def save(self, position):
        self.db.session.add(position)
        self.db.session.commit()

    def increment(self, video_id, movement):
        position = self.get(video_id)
        position.x_position += movement['x']
        position.y_position += movement['y']
        self.save(position)

class ChatMessageDAO(object):
    def __init__(self, db, chat_class):
        self.chat_class = chat_class
        self.db = db

    def save(self, chat_message):
        self.db.session.add(chat_message)
        self.db.session.commit()

    def list(self, limit=10):
        return self.chat_class.query.limit(limit).all()

chat_message_dao = ChatMessageDAO(db, ChatMessage)
video_position_dao = VideoPositionDAO(db, VideoPosition)

@app.route('/')
def root():
    return flask.render_template('index.html')

def anounce_position(video_id):
    position = video_position_dao.get(video_id).__json__()
    socket.emit('position', position, broadcast=True, namespace='/video')

@socketio.on('rotate', namespace='/video')
def rotate(movement):
    video_position_dao.increment(DEFAULT_VIDEO_ID, movement)
    anounce_position(DEFAULT_VIDEO_ID)

@socketio.on('position', namespace='/video')
def force_position(content):
    position = VideoPosition(DEFAULT_VIDEO_ID, content['x'], content['y'])
    video_position_dao.save(position)
    anounce_position(DEFAULT_VIDEO_ID)

@socketio.on('new-message', namespace='/chat')
def new_message(message):
    message = ChatMessage(message['user'], datetime.now(), message['text'])
    chat_message_dao.save(message)
    socket.emit('new-message', message.__json__(), broadcast=True)
