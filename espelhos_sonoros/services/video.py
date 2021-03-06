import flask

def video_service(app, socketio, video_dao, video_info_dao):

    def __enchance_video_info__(video):
        enchanced_video = video.copy()
        video_info = video_info_dao.get(video['id'])
        if video_info:
            if video_info.bandcamp_track_id and video_info.bandcamp_album_id:
                enchanced_video['bandcampTrack'] = video_info.bandcamp_track_id
                enchanced_video['bandcampAlbum'] = video_info.bandcamp_album_id
            if video_info.rec_latitude and video_info.rec_longitude:
                enchanced_video['lat'] = video_info.rec_latitude
                enchanced_video['lng'] = video_info.rec_longitude
        return enchanced_video

    @app.route('/api/videos', methods=['GET'])
    def list_videos_json():
        return flask.jsonify(list(map(lambda v: \
                __enchance_video_info__(v._asdict()), \
                video_dao.list())))

