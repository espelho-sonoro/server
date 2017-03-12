from .queue import queue_service
from .video import video_service
from .oauth import oauth_service
from .control import control_service

import flask

def templates_service(app):
    @app.route('/')
    def root():
        return flask.render_template('index.html')

    @app.route('/googleb4967d0db6539668.html')
    def google_verify():
        return flask.render_template('googleb4967d0db6539668.html')
