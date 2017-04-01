import flask

def video_service(app, socketio, video_dao):

    @app.route('/videos', methods=['GET'])
    def list_videos():
        videos = video_dao.list()
        return flask.render_template('videos.html', videos=videos)

    @app.route('/api/videos', methods=['GET'])
    def list_videos_json():
        return flask.jsonify(list(map(lambda v: v._asdict(), video_dao.list())))

