from .video import video_service
from .oauth import oauth_service
from .twitter import TwitterService

import flask

def templates_service(app, twitter_service):
    @app.route('/')
    def root():
        video_id = app.config['INDEX_VIDEO']
        image = twitter_service.get_last_status_image()
        return flask.render_template('index.html', image=image)

    @app.route('/soundMapping', methods=['GET'])
    def videos():
        return flask.render_template('sound_mapping.html')

    @app.route('/about', methods=['GET'])
    def about():
        return flask.render_template('about.html')
