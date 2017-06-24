from .queue import queue_service
from .video import video_service
from .oauth import oauth_service
from .control import control_service

import flask

def templates_service(app):
    @app.route('/')
    def root():
        video_id = app.config['INDEX_VIDEO']
        return flask.render_template('index.html', video_id=video_id)

    @app.route('/soundMapping', methods=['GET'])
    def videos():
        return flask.render_template('sound_mapping.html')

    @app.route('/about', methods=['GET'])
    def about():
        return flask.render_template('about.html')
