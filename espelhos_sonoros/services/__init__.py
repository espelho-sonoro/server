from .chat import chat
from .video import video
from .oauth import oauth

import flask

def root(app):
    @app.route('/')
    def root():
        return flask.render_template('index.html')
