import flask

def video_service(app, socketio, audio_dao, video_dao):

    def __merge_bandcamp_info(video):
        enchanced_video = video.copy()
        track = audio_dao.track_by_video(video['id'])
        if track:
            enchanced_video['bandcampTrack'] = track.id
            enchanced_video['bandcampAlbum'] = track.album
        return enchanced_video

    @app.route('/api/videos', methods=['GET'])
    def list_videos_json():
        return flask.jsonify(list(map(lambda v: \
                __merge_bandcamp_info(v._asdict()), \
                video_dao.list())))

