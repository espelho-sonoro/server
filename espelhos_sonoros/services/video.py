import flask

def video_service(app, socketio, video_dao):

    @app.route('/api/videos', methods=['GET'])
    def list_videos_json():
        return flask.jsonify(list(map(lambda v: v._asdict(), video_dao.list())))

