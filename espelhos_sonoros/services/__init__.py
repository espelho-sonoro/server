from .queue import queue_service
from .video import video_service
from .oauth import oauth_service
from .control import control_service

import flask

def templates_service(app, video_dao):
    @app.route('/')
    def root():
        video_dao.latest_broadcast()
        return flask.render_template('index.html')

    @app.route('/videos', methods=['GET'])
    def videos():
        return flask.render_template('videos.html')

    @app.route('/about', methods=['GET'])
    def about():
        return flask.render_template('about.html')
