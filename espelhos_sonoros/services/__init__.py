from .queue import queue_service
from .video import video_service
from .oauth import oauth_service
from .control import control_service

import flask

def templates_service(app):
    @app.route('/')
    def root():
        return flask.render_template('index.html')

    @app.route('/videos', methods=['GET'])
    def videos():
        return flask.render_template('videos.html')
