from collections import namedtuple

BANDCAMP_ALBUM = '3166918426'
BANDCAMP_TRACKS = {
    'pCRkeVJTgGg': '3530516134',
    'j2KRpsIOmaY': '1258749440',
    'PHFK5LD1DVM': '2695949178',
    '9PCZ-p75pKA': '3651184009',
    'y7m---RgDSc': '3925564775',
    'M3fJ1e-GYSA': None,
    'Kr-dLm1B2GI': None,
    'UJtCkf9La1Y': '430903402',
    'POQlpC6Hjxs': None
}

TrackInfo = namedtuple('TrackInfo', ['id', 'album'])

class AudioDAO(object):
    def __init__(self, config):
        pass

    def track_by_video(self, video_id):
        track_id = BANDCAMP_TRACKS[video_id]
        if track_id != None:
            return TrackInfo(track_id, BANDCAMP_ALBUM)
        else:
            return None

    def list(self):
        track_ids = filter(BANDCAMP_TRACKS.values(), lambda v: v != None)
        return map(track_ids, lambda t: TrackInfo(t, BANDCAMP_ALBUM))
