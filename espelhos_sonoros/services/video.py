import flask

BANDCAMP_ALBUM  = '3166918426'
BANDCAMP_TRACKS = {
    'pCRkeVJTgGg': '3530516134',
    'j2KRpsIOmaY': '1258749440',
    'PHFK5LD1DVM': '2695949178',
    '9PCZ-p75pKA': '3651184009',
    'y7m---RgDSc': '3925564775',
    'M3fJ1e-GYSA': None,
    'Kr-dLm1B2GI': None
}

def video_service(app, socketio, video_dao):

    def __merge_bandcamp_info(video):
        enchanced_video = video.copy()
        enchanced_video['bandcampTrack'] = BANDCAMP_TRACKS[enchanced_video['id']]
        enchanced_video['bandcampAlbum'] = BANDCAMP_ALBUM
        return enchanced_video

    @app.route('/api/videos', methods=['GET'])
    def list_videos_json():
        #return flask.jsonify(VIDEOS)
        #return flask.jsonify(list(map(lambda v: v._asdict(), video_dao.list())))
        return flask.jsonify(list(map(lambda v: \
                __merge_bandcamp_info(v._asdict()), \
                video_dao.list())))

