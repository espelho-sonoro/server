import flask

def video_service(app, socketio):

    @app.route('/api/videos', methods=['GET'])
    def list_videos():
        return flask.jsonify([])
