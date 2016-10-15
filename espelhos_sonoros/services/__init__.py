from .chat  import chat
from .queue import queue
from .video import video
from .oauth import oauth

import flask

def root(app):
    @app.route('/')
    def root():
        return flask.render_template('index.html')
